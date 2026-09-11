```markdown
# Persona Chatbot 🤖

An interactive conversational AI web application built with **Streamlit**, **LangChain**, and **Groq API** (`llama-3.3-70b-versatile`). This app allows users to interact with customizable chat personas through a clean UI and streamlined session memory.

---

## 🌟 Features

* **LLM Integration**: Powered by Groq's high-speed `llama-3.3-70b-versatile` model via LangChain.
* **Persona Switching**: Engage with custom system prompts and chat personas.
* **Session Memory**: Remembers conversational context across multiple user inputs.
* **Streamlit UI**: Intuitive, responsive web chat interface powered by `st.chat_message` and `st.chat_input`.
* **Secrets Management**: Secure API key management using Streamlit Secrets or `.env` files.

---

## 🛠️ Tech Stack

* **Frontend / Framework**: [Streamlit](https://streamlit.io/)
* **Orchestration**: [LangChain](https://www.langchain.com/)
* **Inference Engine**: [Groq API](https://groq.com/)
* **Language**: Python 3.10+

---

## 🚀 Getting Started Locally

### Prerequisites

* Python 3.10 or higher
* A Groq API key (get one from [Groq Console](https://console.groq.com/))

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/persona-chatbot.git](https://github.com/YOUR_USERNAME/persona-chatbot.git)
   cd persona-chatbot

```

2. **Create and activate a virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

```


3. **Install required dependencies:**
```bash
pip install -r requirements.txt

```


4. **Set up Environment Variables:**
Create a `.env` file in the project root directory:
```env
GROQ_API_KEY=your_groq_api_key_here

```


5. **Run the Streamlit application:**
```bash
streamlit run uichat.py

```



---

## ☁️ Streamlit Cloud Deployment

To deploy this repository to **Streamlit Community Cloud**:

1. Push your code to a GitHub repository.
2. Log into [Streamlit Community Cloud](https://streamlit.io/cloud) and create a **New App**.
3. Select your repository, branch (`main`), and main file path (`uichat.py`).
4. In **Advanced Settings** > **Secrets**, add your Groq API Key:
```toml
GROQ_API_KEY = "your_groq_api_key_here"

```


5. Click **Deploy!**

---

## 📁 Repository Structure

```text
persona-chatbot/
│
├── uichat.py            # Main Streamlit application file
├── requirements.txt     # Python dependencies
├── .env                 # Local environment keys (ignored by git)
└── README.md            # Project documentation

```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

```

```
