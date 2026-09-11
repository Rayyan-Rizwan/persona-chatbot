import streamlit as st
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

load_dotenv()

# ---------------- Page config ----------------
st.set_page_config(page_title="Persona Chatbot", page_icon="🎭", layout="centered")

# ---------------- Custom styling ----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif !important;
    }

    /* ---- Animated gradient background ---- */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #24243e, #302b63, #1a1a3e);
        background-size: 300% 300%;
        animation: gradientMove 18s ease infinite;
    }
    @keyframes gradientMove {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ---- Sidebar (glassmorphism) ---- */
    section[data-testid="stSidebar"] {
        background: rgba(20, 18, 40, 0.75);
        backdrop-filter: blur(14px);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    h1, h2, h3, p, span, label, .stMarkdown, .stCaption {
        color: #f0f0f5 !important;
    }

    /* ---- Header banner ---- */
    .header-banner {
        text-align: center;
        padding: 22px 16px 26px 16px;
        border-radius: 20px;
        margin-bottom: 22px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    }
    .header-banner h1 {
        font-size: 2.1rem;
        margin: 0 0 6px 0;
        background: linear-gradient(90deg, #7f5af0, #2cb67d, #7f5af0);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 6s linear infinite;
        font-weight: 700;
    }
    @keyframes shine {
        to { background-position: 200% center; }
    }
    .header-banner p {
        color: #b8b8d1 !important;
        font-size: 0.95rem;
        letter-spacing: 0.4px;
        margin: 0;
    }
    .active-badge {
        display: inline-block;
        margin-top: 10px;
        padding: 5px 16px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        background: rgba(127, 90, 240, 0.18);
        border: 1px solid rgba(127, 90, 240, 0.5);
        color: #d9c9ff !important;
    }

    /* ---- Persona cards (welcome screen) ---- */
    .persona-grid {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-top: 10px;
    }
    .persona-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 16px 20px;
        transition: all 0.25s ease;
    }
    .persona-card:hover {
        background: rgba(255,255,255,0.10);
        transform: translateY(-2px);
    }
    .persona-emoji {
        font-size: 1.6rem;
        margin-right: 10px;
    }
    .persona-title {
        font-weight: 600;
        font-size: 1.05rem;
    }
    .persona-desc {
        color: #a8a8c0 !important;
        font-size: 0.85rem;
        margin-top: 3px;
    }

    /* ---- Sidebar persona buttons ---- */
    .stButton>button {
        background: linear-gradient(90deg, #7f5af0, #2cb67d);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: 600;
        letter-spacing: 0.3px;
        box-shadow: 0 4px 14px rgba(127, 90, 240, 0.35);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        opacity: 0.92;
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(127, 90, 240, 0.5);
        color: white !important;
    }

    /* ---- Chat bubbles ---- */
    div[data-testid="stChatMessage"] {
        border-radius: 18px;
        padding: 6px 10px;
        margin-bottom: 6px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.18);
    }
    div[data-testid="stChatMessage"]:has(> div > div[data-testid="stChatMessageAvatarUser"]) {
        background: rgba(127, 90, 240, 0.14);
        border: 1px solid rgba(127, 90, 240, 0.25);
    }
    div[data-testid="stChatMessage"]:has(> div > div[data-testid="stChatMessageAvatarAssistant"]) {
        background: rgba(44, 182, 125, 0.10);
        border: 1px solid rgba(44, 182, 125, 0.22);
    }

    /* ---- Chat input ---- */
    div[data-testid="stChatInput"] {
        border-radius: 16px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.15);
    }

    /* ---- Scrollbar ---- */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(127, 90, 240, 0.5);
        border-radius: 10px;
    }

    hr { border-color: rgba(255,255,255,0.1) !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Persona definitions (same options/logic as original) ----------------
PERSONAS = {
    "1": {
        "label": "Sad Assistant",
        "system": "You are a sad assistant and reply in sad way everytime.",
        "avatar": "😢",
        "desc": "Melancholic replies, every single time.",
    },
    "2": {
        "label": "Helpful Assistant",
        "system": "You are a helpful assistant.",
        "avatar": "🤖",
        "desc": "Clear, friendly, no-nonsense help.",
    },
    "3": {
        "label": "Funny Assistant",
        "system": "You are a funny assistant.",
        "avatar": "😂",
        "desc": "Jokes and wit baked into every answer.",
    },
}

# ---------------- Cached model (same init logic as original) ----------------
@st.cache_resource
def get_model():
    return init_chat_model(
        "groq/compound-mini",
        model_provider="groq",
        temperature=0.9,
    )


model = get_model()


# ---------------- Fix LaTeX so Streamlit renders it properly ----------------
def render_math(text: str) -> str:
    # Convert \[ ... \] to $$ ... $$ (block math)
    text = text.replace("\\[", "$$").replace("\\]", "$$")
    # Convert \( ... \) to $ ... $ (inline math)
    text = text.replace("\\(", "$").replace("\\)", "$")
    return text


# ---------------- Trim history sent to the model (keeps full history for display) ----------------
MAX_TURNS = 6  # number of most-recent Human+AI message pairs to send to the model

def trimmed_messages(messages):
    system_msgs = [m for m in messages if isinstance(m, SystemMessage)]
    other_msgs = [m for m in messages if not isinstance(m, SystemMessage)]
    # keep only the last MAX_TURNS*2 non-system messages (human+ai pairs)
    other_msgs = other_msgs[-(MAX_TURNS * 2):]
    return system_msgs + other_msgs


# ---------------- Session state ----------------
if "persona_choice" not in st.session_state:
    st.session_state.persona_choice = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- Sidebar: persona picker ----------------
with st.sidebar:
    st.markdown("### 🎭 Choose your assistant")
    st.caption("Pick a personality — same as pressing 1, 2 or 3 in the CLI.")
    st.markdown("<br>", unsafe_allow_html=True)

    for key, persona in PERSONAS.items():
        if st.button(
            f"{persona['avatar']}  {persona['label']}",
            use_container_width=True,
            key=f"choose_{key}",
        ):
            st.session_state.persona_choice = key
            st.session_state.messages = [SystemMessage(content=persona["system"])]
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    if st.session_state.persona_choice:
        current = PERSONAS[st.session_state.persona_choice]
        badge_html = (
            f'<div style="text-align:center;">'
            f'<span class="active-badge">{current["avatar"]} Active: {current["label"]}</span>'
            f"</div>"
        )
        st.markdown(badge_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Restart / Switch persona", use_container_width=True):
            st.session_state.persona_choice = None
            st.session_state.messages = []
            st.rerun()

# ---------------- Header ----------------
st.markdown(
    """
    <div class="header-banner">
        <h1>🎭 Persona Chatbot</h1>
        <p>Chat with a personality that matches your mood</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- Welcome / persona selection screen ----------------
if not st.session_state.persona_choice:
    st.markdown("👈 **Pick a personality from the sidebar to start chatting:**")

    cards = []
    for persona in PERSONAS.values():
        cards.append(
            '<div class="persona-card">'
            f'<span class="persona-emoji">{persona["avatar"]}</span>'
            f'<span class="persona-title">{persona["label"]}</span>'
            f'<div class="persona-desc">{persona["desc"]}</div>'
            "</div>"
        )
    cards_html = '<div class="persona-grid">' + "".join(cards) + "</div>"

    st.markdown(cards_html, unsafe_allow_html=True)
    st.stop()

avatar = PERSONAS[st.session_state.persona_choice]["avatar"]

# ---------------- Render chat history (skip SystemMessage) ----------------
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="🧑"):
            st.markdown(render_math(msg.content))
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar=avatar):
            st.markdown(render_math(msg.content))

# ---------------- Chat input (replaces input()/exit loop) ----------------
prompt = st.chat_input("Type your message here...")

if prompt:
    # Same as: message.append(HumanMessage(content=prompt))
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user", avatar="🧑"):
        st.markdown(render_math(prompt))

    # Same as: response = model.invoke(message)
    with st.chat_message("assistant", avatar=avatar):
        with st.spinner("Thinking..."):
            response = model.invoke(trimmed_messages(st.session_state.messages))
            st.markdown(render_math(response.content))

    # Same as: message.append(AIMessage(content=response.content))
    st.session_state.messages.append(AIMessage(content=response.content))