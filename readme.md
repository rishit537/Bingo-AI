# 🤖 BingoAI

An AI assistant built using OpenAI API

---

## 🛠️ Setup & Installation

### 1. Clone the Repository

```
git clone https://github.com/rishit537/Bingo-AI.git
cd Bingo-AI
```

### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to keep project dependencies isolated

```
# Create the virtual environment (e.g., named `venv`)
python -m venv venv
```

Before installing dependencies, you must **activate it**:

- **On Windows (Command Prompt):**
  ```
  .\venv\Scripts\activate
  ```

* **On macOS / Linux (Bash):**
  ```
  source venv/bin/activate
  ```

You'll know it's active when you see (venv) at the beginning of your terminal prompt.

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Get Your API Keys

You must get credentials for the three services Bingo uses.

#### 🔑 A. OpenAI API Key

1. Go to the [OpenAI Platform](https://platform.openai.com/api-keys) and sign in.
2. Navigate to the `API Keys` section.
3. Click `Create new secret key`.
4. Copy the key and note it down somewhere.

#### 🔑 B. Spotify API Credentials (Client ID & Secret)

1. Go to the Spotify Developer Dashboard and log in.
2. Click `Create App`.
3. Enter any name and description.
4. Copy the Client ID and Client Secret.
5. Click `Edit Settings`.
6. In the `Redirect URIs` section, add a local URL. (e.g. `http://127.0.0.1:9000`)
7. Click `Add` and then `Save`.
8. Copy the credentials and note them down somewhere.

#### 🔑 C. NewsAPI Key

1. Go to [NewsAPI.org](https://newsapi.org/).
2. Click `Get API Key` and register.
3. Your API key will be on your account dashboard.
4. Copy the key and note it down somewhere.

### 5. Create Your Environment File

This file stores your secret keys.

1. In the main Bingo-AI folder, create a new file named exactly .env

2. Open this file and add your keys in the following format. Do not use quotes.

   ```
   OPENAI_API=your-OpenAI-API
   NEWS_API=your-NewsAPI
   SPOTIFY_USERNAME=your-spotify-user-id
   SPOTIFY_CLIENT_ID=your-client-id
   SPOTIFY_CLIENT_SECRET=your-client-secret
   SPOTIFY_REDIRECT_URI=your-redirect-uri
   ```

## 🚀 How to Run

Once your .env file is set up and your virtual environment is active, run the main script:

```
python main.py
```

**Note:** The first time you use a Spotify command, a browser window will open to ask for your permission. This only happens once.
