import streamlit as st
import time
from datetime import datetime
from data import tb_knowledge_base

st.set_page_config(
    page_title="TB Health Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        background-color: #3b82f6;
        color: white;
        margin-left: 20%;
    }
    .bot-message {
        background-color: #f3f4f6;
        color: #374151;
        margin-right: 20%;
    }
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 10px;
        font-weight: bold;
    }
    .user-avatar {
        background-color: #1e40af;
        color: white;
    }
    .bot-avatar {
        background-color: #3b82f6;
        color: white;
    }
    .message-content {
        flex: 1;
    }
    .message-time {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-top: 0.25rem;
    }
    .sidebar-content {
        padding: 1rem;
    }
    .quick-topic {
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid #e5e7eb;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    .quick-topic:hover {
        background-color: #f9fafb;
    }
    .emergency-card {
        background-color: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def search_faq(user_input, faq_data):
    user_input_lower = user_input.lower()
    for item in faq_data:
        for keyword in item["keywords"]:
            if keyword in user_input_lower:
                return item["answer"]
    return None

def get_bot_response(user_input):
    faq_response = search_faq(user_input, tb_knowledge_base.get("faq", []))
    if faq_response:
        return faq_response
    for section in ["symptoms", "treatments", "prevention", "general_info"]:
        for item in tb_knowledge_base.get(section, []):
            for keyword in item["keywords"]:
                if keyword in user_input.lower():
                    if section == "symptoms":
                        return f"{item['name']}: {item['description']}"
                    elif section == "treatments":
                        return f"{item['name']}: {item['description']}"
                    elif section == "prevention":
                        return f"{item['topic']}: {item['advice']}"
                    elif section == "general_info":
                        return f"{item['topic']}: {item['information']}"
    if any(word in user_input.lower() for word in ["hello", "hi", "hey"]):
        return "Hello! I'm here to help you with tuberculosis-related questions. You can ask me about symptoms, treatment, prevention, or general TB information."
    if "help" in user_input.lower():
        return """I can help you with:
• TB symptoms and signs
• Treatment options and medications
• Prevention methods
• General information about tuberculosis
• Risk factors and transmission

What specific topic would you like to know about?"""
    return "I understand you're asking about TB-related topics. Could you please be more specific? Try asking 'What are TB symptoms?' or 'How is TB treated?'"

def format_time(timestamp):
    return timestamp.strftime("%H:%M")

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "id": "1",
            "text": "Hello! I'm your TB Health Assistant. I can help you with information about tuberculosis symptoms, treatment, prevention, and general questions. What would you like to know?",
            "is_bot": True,
            "timestamp": datetime.now()
        }]
    if "chat_started" not in st.session_state:
        st.session_state.chat_started = False

def render_sidebar():
    with st.sidebar:
        st.markdown("## TB Health Assistant")
        st.markdown("Get reliable information about tuberculosis")

        if st.button("💬 Start New Chat", key="new_chat"):
            st.session_state.messages = [{
                "id": "1",
                "text": "Hello! I'm your TB Health Assistant. I can help you with information about tuberculosis symptoms, treatment, prevention, and general questions. What would you like to know?",
                "is_bot": True,
                "timestamp": datetime.now()
            }]
            st.session_state.chat_started = True
            st.rerun()

        st.markdown("### Quick Topics")
        quick_topics = [
            {"icon": "🔥", "title": "Symptoms", "description": "Common TB symptoms", "query": "What are TB symptoms?"},
            {"icon": "💊", "title": "Treatment", "description": "Treatment options", "query": "How is TB treated?"},
            {"icon": "🛡️", "title": "Prevention", "description": "How to prevent TB", "query": "How can I prevent TB?"},
            {"icon": "ℹ️", "title": "General Info", "description": "About tuberculosis", "query": "What is tuberculosis?"}
        ]
        for topic in quick_topics:
            if st.button(f"{topic['icon']} {topic['title']}", key=f"topic_{topic['title']}", help=topic['description']):
                st.session_state.chat_started = True
                st.session_state.messages.append({
                    "id": str(len(st.session_state.messages) + 1),
                    "text": topic['query'],
                    "is_bot": False,
                    "timestamp": datetime.now()
                })
                st.session_state.messages.append({
                    "id": str(len(st.session_state.messages) + 2),
                    "text": get_bot_response(topic['query']),
                    "is_bot": True,
                    "timestamp": datetime.now()
                })
                st.rerun()

        st.markdown("### 🧮 TB Risk Calculator")
        cough = st.selectbox("Persistent cough?", ["No", "Yes"], key="cough")
        fever = st.selectbox("Fever?", ["No", "Yes"], key="fever")
        weight_loss = st.selectbox("Weight loss?", ["No", "Yes"], key="weight_loss")
        if st.button("📊 Calculate Risk", key="calculate_risk"):
            risk = 0
            if cough == "Yes": risk += 30
            if fever == "Yes": risk += 30
            if weight_loss == "Yes": risk += 40
            st.success(f"Estimated TB risk: **{risk}%**")

        st.markdown("---")
        st.markdown("""
        <div class="emergency-card">
            <h4 style="color: #dc2626;">🚨 Emergency</h4>
            <p style="color: #b91c1c;">If you're experiencing severe symptoms, seek immediate medical attention.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🏥 Find Nearest Hospital", key="emergency"):
            st.error("Please contact your local emergency services or visit the nearest hospital immediately.")

def render_welcome_screen():
    st.markdown("<h1 style='text-align: center; color: #3b82f6;'>TB Health Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6b7280;'>Your trusted companion for tuberculosis information and support</p>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        if st.button("🚀 Start Consultation", key="start_chat"):
            st.session_state.chat_started = True
            st.rerun()
    st.markdown("---")
    features = [
        {"icon": "💬", "title": "Interactive Chat", "description": "Instant answers to TB questions"},
        {"icon": "🛡️", "title": "Accurate Info", "description": "Based on WHO and CDC guidelines"},
        {"icon": "👥", "title": "24/7 Support", "description": "Always available assistance"},
        {"icon": "📚", "title": "Extensive Knowledge", "description": "Covers all TB aspects"}
    ]
    cols = st.columns(4)
    for col, feature in zip(cols, features):
        with col:
            st.markdown(f"""
            <div style="text-align: center; border: 1px solid #e5e7eb; padding: 1rem; border-radius: 0.5rem;">
                <div style="font-size: 2rem;">{feature['icon']}</div>
                <h4>{feature['title']}</h4>
                <p style="color: #6b7280;">{feature['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("---")
    st.info("**Note:** This chatbot provides educational info only. Consult a doctor for medical advice.")

def render_chat_message(message):
    if message["is_bot"]:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <div class="message-avatar bot-avatar">🤖</div>
            <div class="message-content">
                <div>{message['text']}</div>
                <div class="message-time">{format_time(message['timestamp'])}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-content">
                <div>{message['text']}</div>
                <div class="message-time">{format_time(message['timestamp'])}</div>
            </div>
            <div class="message-avatar user-avatar">👤</div>
        </div>
        """, unsafe_allow_html=True)

def render_chat_interface():
    st.markdown("""
    <div style="background-color: white; padding: 1rem; border-bottom: 1px solid #e5e7eb;">
        <div style="display: flex; align-items: center;">
            <div style="background-color: #3b82f6; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
                🤖
            </div>
            <div>
                <h2 style="margin: 0;">TB Health Assistant</h2>
                <p style="margin: 0; font-size: 0.875rem; color: #6b7280;">Online • Ready to help</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for message in st.session_state.messages:
        render_chat_message(message)

    st.markdown("---")
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Message", placeholder="Ask about TB symptoms, treatment...", key="user_input", label_visibility="collapsed")
    with col2:
        if st.button("Send 📤", key="send_button") and user_input.strip():
            st.session_state.messages.append({
                "id": str(len(st.session_state.messages) + 1),
                "text": user_input,
                "is_bot": False,
                "timestamp": datetime.now()
            })
            with st.spinner("TB Assistant is typing..."):
                time.sleep(1)
            st.session_state.messages.append({
                "id": str(len(st.session_state.messages) + 2),
                "text": get_bot_response(user_input),
                "is_bot": True,
                "timestamp": datetime.now()
            })
            st.rerun()

    st.markdown("---")
    st.markdown("<p style='text-align: center; font-size: 0.75rem; color: #9ca3af;'>This chatbot provides educational information only.</p>", unsafe_allow_html=True)

def main():
    initialize_session_state()
    render_sidebar()
    if not st.session_state.chat_started:
        render_welcome_screen()
    else:
        render_chat_interface()

if __name__ == "__main__":
    main()