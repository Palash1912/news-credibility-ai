# 📢 News Credibility AI

News Credibility AI is an AI-powered fact-checking system that verifies the authenticity of news and claims. It leverages **FastAPI**, **Perplexity AI (Sonar LLM)**, and **Twilio WhatsApp API** to provide fact-checking services via a REST API and WhatsApp bot.

## 🚀 Features

- ✅ **Fact-Checking API**: Accepts user queries and evaluates their authenticity.
- 🔍 **Credibility Scoring**: Assigns a confidence score (1-10) based on verified sources.
- 📖 **Reasoning & Sources**: Provides explanations with supporting evidence.
- 🤖 **WhatsApp Integration**: Users can send news queries via WhatsApp for verification.
- 🌍 **Cross-Platform Availability**: Accessible via REST API and messaging platforms.

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python
- **LLM**: Perplexity AI (Sonar LLM)
- **Messaging**: Twilio WhatsApp API
- **Deployment**: Render (FastAPI backend), Ngrok (for local testing)
- **Environment Variables**: Managed via `.env` file

## 🔧 Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/news-credibility-ai.git
cd news-credibility-ai
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate    # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables

Create a `.env` file in the root directory and add:

```env
PERPLEXITY_API_KEY=your_perplexity_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
```

### 5️⃣ Run the FastAPI Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 6️⃣ Expose the API Publicly (For WhatsApp Integration)

```bash
ngrok http 8000
```

Copy the **ngrok** HTTPS URL and update it in Twilio's Webhook settings.

## 🎯 Usage

### 🔹 Using the API

#### **Endpoint:** `/news-check`

```bash
curl -X POST "https://your-api-url.com/news-check" -H "Content-Type: application/json" -d '{"news": "Did DC defeat RCB in WPL?"}'
```

#### **Response Format:**

```json
{
  "is_authentic": true,
  "authenticity_score": 8.5,
  "reasoning": "The claim is verified by multiple news sources, including ESPN and BBC.",
  "sources": ["https://espn.com/news", "https://bbc.com/sports"]
}
```

### 🔹 Using WhatsApp Bot

- Send a message to **Twilio WhatsApp number** with a news query.
- Receive an authenticity check in response.
