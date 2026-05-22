import time
import mysql.connector
from mysql.connector import errorcode
from config import DB_CONFIG


# ── Product catalog ─────────────────────────────────────────────────────────
CATALOG = {
    "Category A: Food": {
        "Seeds": [
            "Chia seed",
            "Pumpkin seed",
            "Quinoa seed",
            "Sunflower seed",
            "Flax seed",
            "Basil seed",
            "Watermelon seed",
        ],
        "Powder": [
            "Moringa powder",
            "GymnemaSylvestre powder",
            "Milk thistle powder",
            "Jamun Seed powder",
            "Maca powder",
            "Isabgol",
            "Mucuna powder",
            "Ashwagandha powder",
            "Asparagus powder",
            "Spirulina powder",
            "Arjuna powder",
            "Beet root powder",
            "Amala Powder",
            "Aleovera powder",
            "Hibiscus power",
            "Licorice powder",
            "Senna powder",
            "Giloypowder",
            "Saw palmetto powder",
            "Bahedapowder",
            "Brahmi Powder",
            "Triphalapowder",
            "Harad powder",
            "Stevia powder",
            "Turmeric powder",
            "Ritha powder",
            "Shikakai powder",
            "Protein powder",
            "Jaggery powder",
            "Brown sugar",
        ],
        "Oil": [
            "Black seed oil",
            "Hemp seed oil",
            "Fenugreekseed oil",
            "Fennelseed oil",
            "Dilseed oil",
            "Sesameseed oil",
            "Black grapeseed oil",
            "Chiaseed oil",
            "Flaxseed oil",
            "Coconut oil",
            "Castorseed oil",
            "Neemseed oil",
            "Almond oil",
            "Walnut oil",
            "Onion seed oil",
            "Moringa seed oil",
            "Thyme seed oil",
            "Pumpkin seed oil",
            "Rose oil",
            "Mustard oil",
        ],
        "Essential Oil": [
            "Lemon grass oil",
            "Orange peel oil",
            "Tea Tree oil",
            "Clove oil",
            "Lavender oil",
            "Jojoba oil",
            "Jasmine oil",
            "Rosemary oil",
            "Basil seed oil",
            "Camphor oil",
            "Peppermint oil",
            "Timmur oil",
            "Jatamansi oil",
        ],
        "Medicinal Oil": [
            "Natural Hair growth oil",
            "Mosquito Repellent oil",
            "Pain relief oil",
            "Body massage oil",
        ],
        "Medicinal Herbs": [
            "Giloya",
            "Mint",
            "Gymnema",
            "Licorice",
            "Milk thistle",
            "Brahmi",
            "Shankhapushpi",
            "Punarnava",
            "Chirayata",
            "Neem",
            "Moringa",
            "Hibiscus",
            "Rose",
            "Jasmine",
            "Lavender",
            "Spirulina",
            "Tulsi",
        ],
        "Himali Products (Wildly Collected)": [
            "Shilajit",
            "Yarsagumba",
            "Honey",
            "Moringa Honey",
            "Jamun Honey",
            "Wild Honey",
            "Mushroom",
            "Gucche Mushroom",
            "Red Mushroom",
            "Ginseng",
            "BudhaChitta",
            "Turmeric",
            "Pink Salt",
            "Cinnamon Stick",
            "Red Rice",
            "Brown Rice",
            "Black Rice",
            "Taichin Rice",
        ],
        "Mix Herbs": [
            "Gastric and piles relief",
            "Triphalapowder",
            "Heart and diabetes care",
            "Sugar control",
            "Healthy drinks",
            "Good Sleep",
        ],
        "Juices & Detox Water": [
            "Aloevera fresh juice",
            "Aloeveraamala fresh juice",
            "Amala fresh juice",
            "Noni fresh juice",
            "Giloy fresh juice",
            "Apple cider vinegar",
            "Jamun cider vinegar",
            "Black Strap Molasses",
        ],
        "Freshly Grown Microgreens": [
            "Broccoli",
            "Radish",
            "Pea Shoots",
            "Sunflower",
            "Kale",
            "Basil",
            "Beetroot",
            "Cabbage",
            "Cauliflower",
            "Mustard",
            "Spinach",
            "Swiss Chard",
            "Carrot",
            "Fenugreek",
            "Thyme",
            "Flax",
            "Arugula",
            "Chia",
            "Fennel",
            "Celery",
        ],
        "Dehydrated Vegetables": [
            "Dehydrated Cabbage",
            "Dehydrated Potatoes",
            "Dehydrated Kale",
            "Dehydrated Onions",
            "Dehydrated Carrots",
            "Dehydrated Spinach",
            "Dehydrated Tomatoes",
            "Dehydrated Beans",
            "Dehydrated Bell pepper",
            "Dehydrated Celery",
            "Dehydrated Beetroot",
            "Dehydrated Bitter Gourd",
            "Dehydrated Bottle Gourd",
            "Dehydrated Peas",
            "Dehydrated Sweet potatoes",
            "Dehydrated Brussels sprouts",
            "Dehydrated Green beans",
            "Dehydrated Mushrooms",
            "Dehydrated Butternut Squash",
            "Dehydrated Corn",
            "Dried Wild Garlic",
            "Dried Kasmiri Garlic",
        ],
        "Dehydrated Fruits": [
            "Amala whole",
            "Rhita whole",
            "Dried blueberries",
            "Dried Cranberries",
            "Shikakai whole",
            "Almonds",
            "Walnuts",
            "Cashew nuts",
            "Pistachios",
            "Raisins",
            "Figs",
            "Dried Bananas",
            "Dried Papayas",
            "Coconut Flakes",
            "Date Palm",
            "Dried Pears",
            "Dried Kiwis",
            "Dried Pineapples",
            "Dried Apples",
        ],
        "Millets": [
            "Foxtail Millet",
            "Finger Millet",
            "Kodo Millet",
            "Jowar",
            "Pearl Millet",
            "Barnyard Millet",
            "Little Millet",
            "Buckwheat",
            "Proso Millet",
            "Amaranth Grain",
            "Naked Barley",
        ],
        "Organic Fresh Vegetable": [
            "Bell peppers",
            "Tomatoes",
            "Potatoes",
            "Spinach",
            "Carrots",
            "Cucumber",
            "Yellow Squash",
            "Cauliflower",
            "Green Kale",
            "Sweet Potatoes",
            "Green Cabbage",
            "Celery",
        ],
    },
    "Category B: Natural Cosmetics": {
        "Oil": [
            "Almond Oil",
            "Walnut oil",
            "Onion seed oil",
            "Rose oil",
            "Coconut oil",
            "Black seed oil",
            "Hemp seed oil",
            "Fenugreekseed oil",
            "Fennelseed oil",
            "Dilseed oil",
            "Sesameseed oil",
            "Black grapeseed oil",
            "Chiaseed oil",
            "Flaxseed oil",
            "Castorseed oil",
            "Neemseed oil",
            "Moringa seed oil",
            "Thyme seed oil",
            "Pumpkin seed oil",
            "Mustard oil",
        ],
        "Essential Oils": ["Rosemary oil"],
        "Medicated Oils": [
            "Coconut Oil",
            "Almond Oil",
            "Onion Oil",
            "Walnut Oil",
        ],
        "Peels": ["Orange peel powder"],
        "Powders": [
            "Sandal powder",
            "MultaniMutti powder",
            "Indigo powder",
            "Henna powder",
            "Hibiscus Powder",
            "Beet root powder",
        ],
        "Water": [
            "Rose water",
            "Jasmine water",
            "Vetiver water",
            "Kewada water",
            "Sandal water",
            "Neem water",
        ],
        "Attars": [
            "Musk",
            "Oud",
            "Rose",
            "Jasmine",
            "Lavender",
            "Jojoba",
            "Jatamansi",
        ],
        "Perfumes": ["Sandal", "Rosemary", "Musk", "Oud", "Jasmine"],
        "Colours": [
            "Henna Powder",
            "Indigo Powder",
            "Amala Powder",
            "Bhringraj Powder",
            "Hibiscus Powder",
            "Shikakai Powder",
            "Ritha Powder",
            "Fenugreek Powder",
            "Brahmi Powder",
        ],
        "Soaps": ["MoringaMultaniMitti soap", "Moringa Neem soap"],
        "Shampoos": [],
        "Face Wash": [],
        "Body wash": [],
        "Mosquito Repllents": ["Spray", "Cream", "Oils"],
        "Hair Care": ["Indigo powder", "Henna powder", "Coconut oil", "Hair growth oil"],
        "Skin Care": [
            "Aleovera gel",
            "MultaniMitti",
            "Sandal Powder",
            "Orange peel powder",
            "Rose water",
            "Vetiver water",
            "Kewada water",
            "Wild turmeric",
            "Black turmeric",
        ],
    },
    "Category C: Spirituals": {
        "Spirutuals": [
            "Rudrakcha",
            "BudhaChitta",
            "Sphatik",
            "Gems",
            "Stones",
            "Shaligram",
            "Shivalinga",
            "Natural Astrilogy Gem Stone",
            "Coins (God & Goddess)",
            "Idols/Stutue(d\"lt{)",
        ],
    },
    "Category D: Sara Nursery": {
        "Herbal and Medicinal Pants": [
            "Insulin Plant",
            "Sindur Plant",
            "Moringa Plant",
            "Ashwagandha",
            "Asparagus",
            "Serpentine",
            "Chirayata",
            "Neem Plant",
        ],
        "Fruit Plants": ["Guava", "Papaya", "Apple Ber", "Dragon Fruit", "Custard Apple", "Mango", "Litchi", "Lemon"],
    },
}


BENEFITS = {
    "Moringa powder": "Rich in vitamins A, C, and E. Supports immunity, energy, and skin health.",
    "Ashwagandha powder": "Adaptogen that reduces stress, improves sleep and boosts stamina.",
    "Chia seed": "High in omega-3, fiber and protein. Great for heart and digestive health.",
    "Wild Honey": "Natural antibacterial. Boosts immunity and soothes sore throats.",
    "Shilajit": "Powerful Himalayan mineral resin. Enhances energy, strength and longevity.",
    "Turmeric powder": "Anti-inflammatory and antioxidant. Supports joint and liver health.",
    "Spirulina powder": "Complete plant protein. Excellent for detox and immune support.",
    "Aloe vera fresh juice": "Soothes digestion, improves skin and supports liver detox.",
}


def get_benefits(name: str) -> str:
    for k, v in BENEFITS.items():
        if k.lower() in name.lower():
            return v
    return f"A natural organic product. {name} is carefully sourced for purity and effectiveness."


def get_price(name: str) -> int:
    name_l = name.lower()
    if any(x in name_l for x in ["shilajit", "yarsagumba", "ginseng"]):
        return 2500
    if any(x in name_l for x in ["honey", "essential", "attar", "perfume"]):
        return 850
    if any(x in name_l for x in ["oil"]):
        return 650
    if any(x in name_l for x in ["plant", "seed"]):
        return 350
    return 450


def setup():
    base_cfg = {k: v for k, v in DB_CONFIG.items() if k != "database"}

    host = base_cfg.get("host")
    user = base_cfg.get("user")
    db_name = DB_CONFIG.get("database")
    port = base_cfg.get("port")

    max_retries = 5
    retry_delay_sec = 2

    conn = None
    last_err = None

    for attempt in range(1, max_retries + 1):
        try:
            print(f"[DB SEED] Connecting to MySQL (attempt {attempt}/{max_retries}) host={host!r} user={user!r} port={port!r} db={db_name!r}...")
            conn = mysql.connector.connect(**base_cfg)
            break
        except mysql.connector.Error as e:
            last_err = e
            print("[DB SEED] Cannot connect to MySQL server.")
            print(f"[DB SEED] Tried host={host!r}, user={user!r}, port={port!r}")
            print(f"[DB SEED] Error: {e}")
            if attempt < max_retries:
                print(f"[DB SEED] Retrying in {retry_delay_sec}s...")
                time.sleep(retry_delay_sec)

    if conn is None:
        print("\n[DB SEED] Connection failed after retries.")
        print("[DB SEED] Fix DB_HOST/DB_USER/DB_PASSWORD, ensure MySQL is installed and running, and that MySQL listens on the expected host/port.")
        print(f"[DB SEED] Active DB_CONFIG: {DB_CONFIG}")
        raise last_err

    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} DEFAULT CHARACTER SET 'utf8mb4'")
    cur.execute(f"USE {DB_CONFIG['database']}")
    conn.close()
    print(f"Database '{DB_CONFIG['database']}' ready.")

    # Reconnect to specific DB for schema + seeding
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(200),
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255),
            google_id VARCHAR(255),
            role VARCHAR(20) DEFAULT 'customer',
            is_verified TINYINT(1) DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # If a previous run created the users table without `role`, add it so seeding doesn't fail.
    cur.execute("SHOW COLUMNS FROM users LIKE 'role'")
    if not cur.fetchone():
        cur.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'customer'")

    cur.execute("SHOW COLUMNS FROM users LIKE 'is_verified'")
    if not cur.fetchone():
        cur.execute("ALTER TABLE users ADD COLUMN is_verified TINYINT(1) DEFAULT 0")
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            token VARCHAR(255) NOT NULL,
            expires_at DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            parent_id INT NULL,
            FOREIGN KEY (parent_id) REFERENCES categories(id)
        )
    """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category_id INT,
            name VARCHAR(255) NOT NULL,
            benefits TEXT,
            effects TEXT,
            price INT DEFAULT 450,
            image_url VARCHAR(500),
            in_stock TINYINT(1) DEFAULT 1,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            total_amount DECIMAL(10, 2) NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            payment_method VARCHAR(50),
            transaction_uuid VARCHAR(255) UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        )
    """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS company_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            info_key VARCHAR(100) UNIQUE,
            info_value TEXT
        )
    """
    )
    conn.commit()
    print("Tables created.")

    # Company info
    info = [
        ("name", "Sara World Business Pvt. Ltd."),
        ("location", "Kalanki-14, Kathmandu, Nepal"),
        ("phone", "+977 1 5225181, +977 9851105234, 9808500141"),
        ("email", "info@saraworldwide.com.np"),
        ("website", "https://saraworldwide.com.np/saraworldwide"),
        ("facebook", "https://www.facebook.com/saraworldwide.com.np/"),
    ]
    for k, v in info:
        cur.execute(
            "INSERT INTO company_info (info_key, info_value) VALUES (%s,%s) ON DUPLICATE KEY UPDATE info_value=%s",
            (k, v, v),
        )

    # Seed categories and products (idempotent via lookup-by-name)
    # Keyword map: product-name fragments -> Unsplash search term
    PRODUCT_IMAGE_KEYWORDS = {
        # Seeds
        "chia seed": "chia+seeds", "pumpkin seed": "pumpkin+seeds", "quinoa": "quinoa",
        "sunflower seed": "sunflower+seeds", "flax seed": "flaxseed", "basil seed": "basil+seeds",
        "watermelon seed": "watermelon+seeds",

        # Powders
        "moringa": "moringa+powder", "gymnema": "herbal+powder", "milk thistle": "milk+thistle",
        "jamun": "jamun+fruit", "maca": "maca+powder", "isabgol": "psyllium+husk",
        "mucuna": "herbal+powder", "ashwagandha": "ashwagandha+powder", "asparagus": "asparagus",
        "spirulina": "spirulina+powder", "arjuna": "herbal+powder", "beet root": "beetroot+powder",
        "amala": "amla+fruit", "aleovera": "aloe+vera", "aloe vera": "aloe+vera",
        "hibiscus": "hibiscus+flower", "licorice": "licorice+root", "senna": "herbal+leaves",
        "giloy": "giloy+plant", "giloypowder": "giloy",
        "saw palmetto": "herbal+supplement", "baheda": "dried+herbs", "bahedapowder": "baheda",
        "brahmi": "brahmi+herb",
        "triphala": "herbal+powder", "triphala powder": "triphala+powder", "triphalapowder": "triphala",
        "harad": "dried+fruit",
        "stevia": "stevia+plant", "turmeric": "turmeric+powder", "ritha": "soapnut",
        "shikakai": "shikakai+powder", "protein powder": "protein+powder",
        "jaggery": "jaggery", "brown sugar": "brown+sugar",

        # Oils
        "black seed oil": "black+seed+oil", "hemp seed oil": "hemp+oil",
        "fenugreek seed oil": "fenugreek", "fenugreekseed oil": "fenugreek",
        "fennel seed oil": "fennel", "fennelseed oil": "fennel",
        "dil seed oil": "dill+herb", "dilseed oil": "dill",
        "sesame seed oil": "sesame+oil", "sesameseed oil": "sesame",
        "black grape seed oil": "grape+seed+oil", "black grapeseed oil": "grape+seed+oil",
        "chia seed oil": "chia+seeds", "chiaseed oil": "chia+seeds",
        "flaxseed oil": "flaxseed+oil", "flaxseed oil": "flaxseed+oil",
        "castor seed oil": "castor+oil", "castorseed oil": "castor+oil",
        "neem seed oil": "neem+leaves", "neemseed oil": "neem+leaves",
        "almond oil": "almond+oil", "walnut oil": "walnut", "onion seed oil": "onion+seeds",
        "moringa seed oil": "moringa", "thyme seed oil": "thyme+herb",
        "pumpkin seed oil": "pumpkin+seeds", "rose oil": "rose+oil", "mustard oil": "mustard",

        # Essential Oils
        "lemon grass oil": "lemongrass", "orange peel oil": "orange+peel",
        "tea tree oil": "tea+tree", "clove oil": "cloves", "lavender oil": "lavender",
        "jojoba oil": "jojoba", "jasmine oil": "jasmine+flower", "rosemary oil": "rosemary",
        "basil seed oil": "basil", "camphor oil": "camphor", "peppermint oil": "peppermint",
        "timmur oil": "spices", "jatamansi oil": "herbal+oil",

        # Medicinal / Cosmetics
        "hair growth oil": "hair+oil", "mosquito repellent oil": "mosquito+repellent",
        "mosquito repellent spray": "mosquito+repellent", "mosquito repellent cream": "mosquito+cream",
        "pain relief oil": "massage+oil", "body massage oil": "body+massage",
        "Mosquito Repllents": "mosquito+repellent",

        # Herbs
        "mint": "mint+leaves", "neem": "neem+leaves", "rose": "rose+flower",
        "jasmine": "jasmine+flower", "lavender": "lavender+field", "tulsi": "tulsi+plant",
        "shankhapushpi": "herbal+plant", "punarnava": "herbal+plant", "chirayata": "herbal+plant",

        # Himali
        "shilajit": "shilajit", "yarsagumba": "cordyceps+mushroom", "honey": "honey+jar",
        "moringa honey": "honey+moringa", "jamun honey": "honey+jar", "wild honey": "wild+honey",
        "gucche mushroom": "mushroom", "red mushroom": "red+mushroom", "mushroom": "mushroom",
        "ginseng": "ginseng+root", "budhachitta": "himalayan+herb", "budhaChitta": "himalayan+herb",
        "pink salt": "pink+salt",
        "cinnamon": "cinnamon+sticks", "red rice": "red+rice", "brown rice": "brown+rice",
        "black rice": "black+rice", "taichin rice": "organic+rice",

        # Mix Herbs
        "gastric": "herbal+medicine", "heart and diabetes": "herbal+supplement",
        "sugar control": "herbal+tea", "healthy drinks": "herbal+drink", "good sleep": "chamomile+tea",

        # Juices
        "fresh juice": "fresh+juice", "cider vinegar": "apple+cider+vinegar",
        "black strap molasses": "molasses", "noni": "noni+juice", "giloy fresh": "herbal+juice",

        # Microgreens
        "microgreens": "microgreens", "broccoli": "broccoli+microgreens",
        "radish": "radish", "pea shoots": "pea+shoots", "kale": "kale",
        "cabbage": "cabbage", "cauliflower": "cauliflower", "mustard": "mustard+greens",
        "spinach": "spinach", "swiss chard": "swiss+chard", "carrot": "carrots",
        "arugula": "arugula", "fennel": "fennel", "celery": "celery",

        # Dehydrated Veg
        "dehydrated cabbage": "dried+cabbage", "dehydrated potato": "dehydrated+vegetables",
        "dehydrated kale": "dried+kale", "dehydrated onion": "dried+onion",
        "dehydrated carrot": "dried+carrots", "dehydrated spinach": "dried+spinach",
        "dehydrated tomato": "dried+tomatoes", "dehydrated bean": "dried+beans",
        "dehydrated bell pepper": "dried+bell+pepper", "dehydrated celery": "dried+celery",
        "dehydrated beetroot": "dried+beetroot", "dehydrated bitter gourd": "bitter+gourd",
        "dehydrated bottle gourd": "bottle+gourd", "dehydrated peas": "dried+peas",
        "dehydrated sweet potato": "sweet+potato", "dehydrated brussels": "brussels+sprouts",
        "dehydrated green bean": "green+beans", "dehydrated mushroom": "dried+mushroom",
        "dehydrated butternut": "butternut+squash", "dehydrated corn": "dried+corn",
        "dried wild garlic": "wild+garlic", "dried kashmiri garlic": "garlic",

        # Dehydrated Fruits
        "amala whole": "amla+fruit", "rhita whole": "soapnut",
        "dried blueberries": "dried+blueberries", "dried cranberries": "dried+cranberries",
        "shikakai whole": "shikakai", "almonds": "almonds", "walnuts": "walnuts",
        "cashew": "cashew+nuts", "pistachios": "pistachios", "raisins": "raisins",
        "figs": "dried+figs", "dried bananas": "dried+bananas", "dried papayas": "dried+papaya",
        "coconut flakes": "coconut+flakes", "date palm": "dates+fruit",
        "dried pears": "dried+pears", "dried kiwis": "kiwi+fruit",
        "dried pineapples": "dried+pineapple", "dried apples": "dried+apples",

        # Millets
        "foxtail millet": "millet+grain", "finger millet": "finger+millet",
        "kodo millet": "millet", "jowar": "sorghum+grain", "pearl millet": "pearl+millet",
        "barnyard millet": "millet+grain", "little millet": "millet",
        "buckwheat": "buckwheat", "proso millet": "millet",
        "amaranth": "amaranth+grain", "naked barley": "barley",

        # Fresh Veg
        "bell pepper": "bell+peppers", "tomato": "tomatoes", "potato": "potatoes",
        "cucumber": "cucumber", "yellow squash": "yellow+squash",
        "green kale": "kale+leaves", "sweet potato": "sweet+potatoes",
        "green cabbage": "green+cabbage",

        # Cosmetic
        "sandal powder": "sandalwood+powder", "multani": "clay+powder",
        "indigo powder": "indigo+powder", "henna": "henna+powder",
        "rose water": "rose+water", "jasmine water": "jasmine+flower",
        "vetiver water": "vetiver", "kewada water": "kewra+flower",
        "sandal water": "sandalwood", "neem water": "neem+leaves",
        "musk": "musk+perfume", "oud": "oud+perfume",
        "attar": "perfume+bottle", "perfume": "luxury+perfume",
        "bhringraj": "herbal+powder", "soaps": "natural+soap",
        "moringa multani mitti soap": "natural+soap", "moringa neem soap": "natural+soap",
        "shampoo": "shampoo+bottle", "face wash": "face+wash",
        "body wash": "body+wash", "aloevera gel": "aloe+vera+gel",
        "wild turmeric": "turmeric+root", "black turmeric": "black+turmeric",

        # Spirituals
        "rudraksha": "rudraksha+beads", "sphatik": "crystal+ball",
        "gems": "gemstone", "stones": "healing+crystals",
        "shaligram": "shaligram+stone", "shivalinga": "shivling",
        "gem stone": "gemstone+jewelry", "coins": "gold+coins",
        "idols": "hindu+idol", "statues": "religious+statue",

        # Nursery
        "insulin plant": "medicinal+plant", "sindur plant": "herbal+plant",
        "moringa plant": "moringa+tree", "neem plant": "neem+tree",
        "serpentine": "medicinal+herb",
        "guava": "guava+fruit+plant", "papaya": "papaya+tree",
        "apple ber": "apple+fruit+tree", "dragon fruit": "dragon+fruit+plant",
        "custard apple": "custard+apple", "mango": "mango+tree",
        "litchi": "lychee+tree", "lemon": "lemon+tree",

    }

    # Optional overrides for specific products (set to your provided image URLs)
    PRODUCT_IMAGE_OVERRIDES = {
        "Chia seed": "https://thfvnext.bing.com/th/id/OIP.KYZ3HZu-ogCAZr7ELozdVAHaHa?w=184&h=184&c=7&r=0&o=7&cb=thfvnext&dpr=1.3&pid=1.7&rm=3",
        "Moringa powder": "https://img.drz.lazcdn.com/static/np/p/8118f5d263b4ef4ae98ef9dc261d1b00.jpg_720x720q80.jpg",
        "Wild Honey": "https://sarafoods.co.in/wp-content/uploads/2023/07/01-HONEY-500-250-120-GM.jpg",
    }

    def get_image_url(product_name: str, cat_name: str) -> str:
        # Exact-name overrides first
        if product_name in PRODUCT_IMAGE_OVERRIDES:
            return PRODUCT_IMAGE_OVERRIDES[product_name]

        name_lower = product_name.lower()
        for keyword, unsplash_term in PRODUCT_IMAGE_KEYWORDS.items():
            if keyword in name_lower:
                return f"https://source.unsplash.com/400x400/?{unsplash_term}"
        # fallback by category
        cat_fallbacks = {
            "Category A: Food": "organic+food",
            "Category B: Natural Cosmetics": "natural+cosmetics",
            "Category C: Spirituals": "spiritual+meditation",
            "Category D: Sara Nursery": "herbal+plant",
        }
        term = cat_fallbacks.get(cat_name, "natural+organic")
        return f"https://source.unsplash.com/400x400/?{term}"

    def get_or_create_category(name: str, parent_id):
        cur.execute("SELECT id FROM categories WHERE name=%s AND parent_id <=> %s LIMIT 1", (name, parent_id))
        row = cur.fetchone()
        if row:
            return row[0]
        cur.execute("INSERT INTO categories (name, parent_id) VALUES (%s, %s)", (name, parent_id))
        return cur.lastrowid

    def get_product_id_by_name(name: str):
        cur.execute("SELECT id FROM products WHERE name=%s LIMIT 1", (name,))
        row = cur.fetchone()
        return row[0] if row else None

    for cat_name, subcats in CATALOG.items():
        parent_id = get_or_create_category(cat_name, None)

        for sub_name, products in subcats.items():
            sub_id = get_or_create_category(sub_name, parent_id)
            for pname in products:
                benefits = get_benefits(pname)
                price = get_price(pname)
                effects = "Natural and safe for regular use. Consult a healthcare provider for medicinal use."
                img_url = get_image_url(pname, cat_name)

                existing_pid = get_product_id_by_name(pname)
                if existing_pid:
                    cur.execute(
                        "UPDATE products SET category_id=%s, benefits=%s, effects=%s, price=%s, image_url=%s WHERE id=%s",
                        (sub_id, benefits, effects, price, img_url, existing_pid),
                    )
                else:
                    cur.execute(
                        "INSERT INTO products (category_id, name, benefits, effects, price, image_url) VALUES (%s,%s,%s,%s,%s,%s)",
                        (sub_id, pname, benefits, effects, price, img_url),
                    )

    # Seed admin user
    # When running this file directly inside Docker, `backend` isn't a package.
    # Import from the local `services/` directory instead.
    from services.auth_service import hash_password
    admin_email = "admin@saraworldwide.com.np"
    cur.execute("SELECT id FROM users WHERE email=%s", (admin_email,))
    if not cur.fetchone():
        # Keep within bcrypt limits and avoid bcrypt backend issues during docker startup
        # Use a short password to avoid bcrypt/passlib edge-cases during container startup
        hashed = hash_password("Admin")
        cur.execute("INSERT INTO users (full_name, email, password_hash, role, is_verified) VALUES (%s,%s,%s,%s,%s)",
                    ("System Admin", admin_email, hashed, "admin", 1))
        print(f"Seeded default admin: {admin_email}")

    conn.commit()
    conn.close()
    print("Catalog seeded/updated successfully!")


if __name__ == "__main__":
    setup()

