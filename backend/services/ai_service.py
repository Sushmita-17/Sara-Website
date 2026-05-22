import re
from pathlib import Path

import google.generativeai as genai

from ..config import GEMINI_API_KEY, AI_MODEL_NAME

genai.configure(api_key=GEMINI_API_KEY)

_BACKEND = Path(__file__).resolve().parent.parent
_KNOWLEDGE_PATH = _BACKEND / "data" / "website_knowledge.txt"
_MAX_KNOWLEDGE_CHARS = 95_000


def _load_website_knowledge() -> str:
    if not _KNOWLEDGE_PATH.is_file():
        return ""
    text = _KNOWLEDGE_PATH.read_text(encoding="utf-8").strip()
    if len(text) > _MAX_KNOWLEDGE_CHARS:
        return (
            text[:_MAX_KNOWLEDGE_CHARS]
            + "\n\n[Catalog document continues — ask about a specific product name for details.]"
        )
    return text


def _build_system_prompt() -> str:
    knowledge = _load_website_knowledge()
    knowledge_block = (
        f"\n\n--- Official product & website knowledge (from catalog document) ---\n{knowledge}"
        if knowledge
        else ""
    )
    return f"""You are Sara AI, the official customer support assistant for Sara Worldwide Business Pvt. Ltd. (retail brand: Sara Foods).
You are professional, warm, and expert in organic and natural Himalayan products.

Company:
- Name: Sara Worldwide Business Pvt. Ltd. / Sara Foods
- Address: Kalanki-14, Kathmandu, Nepal
- CEO: Shanker Pandey — pandeyshanker@yahoo.com, 9808500141
- Phone: +977 1 5225181 | Mobile: +977 9851105234
- Email: info@saraworldwide.com.np
- Website: https://saraworldwide.com.np/
- Hours: Sunday–Friday 9am–6pm, Saturday closed
- Featured products: Moringa Powder, Shilajit, Ginseng, Wild Honey

Categories:
- A Food: seeds, powders, oils, honey, shilajit, juices, millets, dehydrated foods
- B Natural Cosmetics: oils, soaps, gels, hair & skin care
- C Spirituals: rudraksha, gems, stones
- D Sara Nursery: herbal & fruit plants

Rules:
1. Answer using the catalog knowledge below when the customer asks about products, benefits, usage, or categories.
2. Keep replies concise (2–5 short paragraphs max). Use simple HTML only: <strong>, <br>, <ul>, <li>, <a href="...">.
3. For location questions, mention Kalanki-14 store and suggest Google Maps / calling +977 9851105234.
4. Encourage browsing products.html on this site or saraworldwide.com.np.
5. If unsure, ask them to call +977 9851105234 or WhatsApp.
6. Reply in the same language the customer uses (Nepali or English).
{knowledge_block}
"""


_HIGHLIGHT_PRODUCTS = (
    "Moringa powder",
    "Shilajit",
    "Ginseng",
    "Wild Honey",
    "Chia seed",
    "Ashwagandha powder",
    "Spirulina powder",
)


def _fallback_knowledge_reply(user_query: str) -> str | None:
    """Answer from Website For Sara Foods.docx when Gemini is unavailable."""
    text = _load_website_knowledge()
    if not text:
        return None

    q = user_query.lower().strip()
    best_name = None
    best_score = 0

    for name in _HIGHLIGHT_PRODUCTS:
        nl = name.lower()
        if nl in q:
            best_name = name
            break
        tokens = [t for t in re.split(r"\W+", nl) if len(t) >= 4]
        score = sum(1 for t in tokens if t in q)
        if score > best_score:
            best_score = score
            best_name = name

    if not best_name:
        for line in text.splitlines():
            ln = line.strip()
            if 3 < len(ln) < 60 and ln.lower() in q:
                best_name = ln
                break

    if not best_name:
        return None

    pattern = re.compile(
        re.escape(best_name) + r"\s*\n([\s\S]*?)(?=\n[A-Z][^\n]{2,50}\n|\Z)",
        re.IGNORECASE,
    )
    match = pattern.search(text)
    body = match.group(1).strip() if match else ""
    if not body:
        idx = text.lower().find(best_name.lower())
        if idx >= 0:
            body = text[idx + len(best_name) : idx + len(best_name) + 900].strip()

    if not body:
        return None

    body = body[:900].replace("\n", "<br>")
    return (
        f"<strong>{best_name}</strong><br><br>{body}<br><br>"
        f'<a href="products.html">Browse shop</a> · '
        f'<a href="https://saraworldwide.com.np/" target="_blank" rel="noopener">saraworldwide.com.np</a>'
    )


_model = None


def _get_model():
    global _model
    if _model is None:
        _model = genai.GenerativeModel(
            model_name=AI_MODEL_NAME,
            system_instruction=_build_system_prompt(),
        )
    return _model


def get_ai_response(user_query: str) -> str:
    offline = _fallback_knowledge_reply(user_query)
    try:
        if not GEMINI_API_KEY or "YOUR_GEMINI" in (GEMINI_API_KEY or ""):
            if offline:
                return offline
            return (
                "I'm in catalog mode (AI key not set). "
                "Call +977 9851105234 or visit Sara Worldwide Business, Kalanki-14. 🌿"
            )

        response = _get_model().generate_content(user_query)
        text = (response.text or "").strip()
        if not text:
            return offline or "Please try again or call +977 9851105234."
        return text
    except Exception as e:
        print(f"AI Error: {e}")
        if offline:
            return offline
        return (
            "I'm using our product catalog offline right now. "
            "Try asking about <strong>Moringa powder</strong>, <strong>Shilajit</strong>, "
            "<strong>Ginseng</strong>, or <strong>Wild Honey</strong> — or call +977 9851105234."
        )
