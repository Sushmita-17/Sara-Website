# Sara Worldwide Chatbot 🌿

Full-stack e-commerce platform and AI Chatbot for **Sara World Business Pvt. Ltd.**

## Features
- **AI Chatbot**: Integrated with Google Gemini for natural product inquiries.
- **E-commerce**: Full product catalog, filtering, and cart functionality.
- **Authentication**: JWT-based login/register + **Continue with Google**.
- **Direct Messaging**: Quick links to WhatsApp, Messenger, Instagram, and TikTok.

## Local Setup (VS Code)

### 1. Backend Setup
1. Open terminal in `backend/` folder.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in `backend/` and add your keys:
   ```env
   DB_HOST=127.0.0.1
   DB_USER=root
   DB_PASSWORD=
   DB_NAME=sara_chatbot_db
   GEMINI_API_KEY=your_gemini_api_key
   GOOGLE_CLIENT_ID=your_google_id
   GOOGLE_CLIENT_SECRET=your_google_secret
   ```

### 2. Database Setup
1. Ensure MySQL is running.
2. Run the seeding script:
   ```bash
   python setup_db.py
   ```

### 3. Run the App
- **VS Code**: Press `F5` or go to the "Run and Debug" tab and select "FastAPI: Run Backend".
- **Manual**: Run `uvicorn main:app --reload` from the `backend/` directory.

The website will be available at [http://localhost:8000](http://localhost:8000).

## Tech Stack
- **Backend**: FastAPI, MySQL, Google Generative AI (Gemini).
- **Frontend**: HTML5, Vanilla CSS, Vanilla JavaScript.
- **Tools**: Docker, VS Code.

