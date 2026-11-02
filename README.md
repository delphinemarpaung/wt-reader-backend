# ⚙️ WT Reader — Backend

The **WT Reader Backend** is the RESTful API and core processing engine powering the WT Reader application. It handles user data, vocabulary lists, and the complex pipeline of extracting and translating Chinese text from comic images.

> 🔗 **Looking for the Client Web Application?** Check out the [WT Reader Frontend Repository](https://github.com/delphinemarpaung/wt-reader-frontend).

---

## 🎯 Project Background

Learning a new language can be daunting, but reading native material like comics makes it engaging and fun. **WT Reader** is built specifically to help users learn Mandarin by reading raw Chinese manga/comics. 

The frontend app provides the UI, but this backend acts as the brain. It takes uploaded or requested comic images and passes them through an **OCR (Optical Character Recognition)** pipeline to extract the raw Chinese text. It then utilizes natural language processing (NLP) to **tokenize** the text into individual words, fetches translations for both the full sentence and distinct tokens, and generates **Pinyin**. Finally, it manages user accounts, allowing learners to save specific words to a **Vocabulary List** and serves up panel data for an interactive **Memory Game** where users type the correct Mandarin word.

---

## 📑 Table of Contents

* [Features](#-features)
* [Tech Stack](#-tech-stack)
* [Related Repositories](#-related-repositories)
* [Getting Started](#-getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Environment Variables](#environment-variables)
  * [Running Locally](#running-locally)
* [API Architecture & Endpoints](#-api-architecture--endpoints)
* [Connecting with Frontend](#-connecting-with-frontend)
* [Contributing](#-contributing)
* [License](#-license)

---

## ✨ Features

* 🔍 **OCR Pipeline:** Processes comic images to accurately extract raw Chinese text.
* 🧩 **Tokenization & Translation:** Breaks down extracted text into individual Mandarin words/tokens, generates accurate Pinyin, and fetches context-aware translations.
* 📚 **Vocabulary Management:** Database structure to allow users to save, organize, and retrieve their personal vocabulary lists.
* 🎮 **Memory Game State:** Endpoints dedicated to serving isolated comic panels and validating user inputs for the context-based memory typing game.
* 🔐 **User Authentication:** JWT-based user login, registration, and session security.
* 🌐 **CORS Support:** Configurable cross-origin policies for seamless integration with the frontend.

---

## 🛠 Tech Stack

* **Runtime:** Node.js / Express (or Python / FastAPI for heavy NLP/OCR tasks)
* **Database:** MongoDB / PostgreSQL
* **Processing APIs:** Integrations for OCR (e.g., Google Cloud Vision, Tesseract) and Translation/Dictionary APIs.
* **Authentication:** JSON Web Tokens (JWT) / bcrypt
* **Middleware:** CORS, Morgan, dotenv

---

## 🔗 Related Repositories

| Repository | Role | Link | 
| ----- | ----- | ----- | 
| **`wt-reader-backend`** | REST API & Core Services | *(This Repo)* | 
| **`wt-reader-frontend`** | Web Client UI | [github.com/delphinemarpaung/wt-reader-frontend](https://github.com/delphinemarpaung/wt-reader-frontend) | 

---

## 🚀 Getting Started

Follow these instructions to set up the backend service on your local machine.

### Prerequisites

* **Node.js** (or Python, depending on your core implementation)
* **Database**: Active instance of MongoDB / PostgreSQL
* API Keys for OCR and Translation services (if using external providers)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/delphinemarpaung/wt-reader-backend.git
   cd wt-reader-backend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

### Environment Variables

Create a `.env` file in the root directory:

```env
PORT=5000
NODE_ENV=development

# Database Connection
DATABASE_URL=mongodb://localhost:27017/wt_reader

# Authentication
JWT_SECRET=your_super_secret_jwt_key_here
JWT_EXPIRES_IN=7d

# 3rd Party API Keys
OCR_API_KEY=your_ocr_provider_key
TRANSLATION_API_KEY=your_translation_provider_key

# Frontend CORS Origin
CLIENT_URL=http://localhost:3000
```

### Running Locally

Start the development server:

```bash
npm run dev
```

The API server will run at `http://localhost:5000`.

---

## 📡 API Architecture & Endpoints

Summary of core REST API endpoint domains:

### 1. Processing (`/api/process`)
* `POST /api/process/ocr` - Receive image, run OCR, return raw text.
* `POST /api/process/tokenize` - Receive text, return array of tokens, Pinyin, and translations.

### 2. User & Vocabulary (`/api/user`)
* `GET  /api/user/vocab` - Get authenticated user's saved vocabulary list.
* `POST /api/user/vocab` - Add a new word (with Pinyin and meaning) to the vocab list.
* `DELETE /api/user/vocab/:id` - Remove a word from the list.

### 3. Memory Game (`/api/game`)
* `GET  /api/game/prompt` - Fetch a randomized comic panel and the target word to test the user.

### 4. Authentication (`/api/auth`)
* `POST /api/auth/register` - Register a new user.
* `POST /api/auth/login` - Authenticate user & receive JWT.

---

## 🔌 Connecting with Frontend

1. Ensure the `CLIENT_URL` environment variable matches your frontend origin (e.g., `http://localhost:3000`).
2. Set your frontend environment variable to point to this backend server to ensure seamless communication for OCR and dictionary lookups.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.