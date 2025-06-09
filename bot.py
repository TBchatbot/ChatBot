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
    .faq-question {
        cursor: pointer;
        padding: 0.5rem 1rem;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        background-color: #f9fafb;
    }
    .faq-answer {
        padding: 0.5rem 1rem 1rem 1rem;
        margin-bottom: 1rem;
        border-left: 3px solid #3b82f6;
        background-color: #f3f4f6;
    }
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 4px;
        padding: 1rem;
    }
    .typing-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #9ca3af;
        animation: typing 1.4s infinite ease-in-out;
    }
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

def find_relevant_response(user_input):
    input_lower = user_input.lower()
    for symptom in tb_knowledge_base["symptoms"]:
        if symptom["name"].lower() in input_lower or any(keyword.lower() in input_lower for keyword in symptom["keywords"]):
            return f"Regarding {symptom['name']}: {symptom['description']}"
    for treatment in tb_knowledge_base["treatments"]:
        if treatment["name"].lower() in input_lower or any(keyword.lower() in input_lower for keyword in treatment["keywords"]):
            return f"About {treatment['name']}: {treatment['description']}"
    for prevention in tb_knowledge_base["prevention"]:
        if prevention["topic"].lower() in input_lower or any(keyword.lower() in input_lower for keyword in prevention["keywords"]):
            return f"Prevention - {prevention['topic']}: {prevention['advice']}"
    for info in tb_knowledge_base["general_info"]:
        if info["topic"].lower() in input_lower or any(keyword.lower() in input_lower for keyword in info["keywords"]):
            return f"{info['topic']}: {info['information']}"
    for faq in tb_knowledge_base["faqs"]:
        if faq["question"].lower() in input_lower:
            return f"FAQ: {faq['answer']}"
    if any(word in input_lower for word in ["hello", "hi", "hey"]):
        return "Hello! I'm here to help you with tuberculosis-related questions. You can ask me about symptoms, treatment, prevention, or general TB information."
    if "help" in input_lower:
        return """I can help you with:
• TB symptoms and signs
• Treatment options and medications
• Prevention methods
• General information about tuberculosis
• Risk factors and transmission
• Frequently Asked Questions (FAQs)

What specific topic would you like to know about?"""
    return "I understand you're asking about TB-related topics. Could you please be more specific? You can ask me about symptoms, treatment, prevention, FAQs, or general information about tuberculosis. For example, try asking 'What are TB symptoms?' or 'What is latent TB?'"

def format_time(timestamp):
    return timestamp.strftime("%H:%M")

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "id": "1",
                "text": "Hello! I'm your TB Health Assistant. I can help you with information about tuberculosis symptoms, treatment, prevention, and general questions. What would you like to know?",
                "is_bot": True,
                "timestamp": datetime.now()
            }
        ]
    if "chat_started" not in st.session_state:
        st.session_state.chat_started = False
    if "risk_score" not in st.session_state:
        st.session_state.risk_score = None
    if "show_risk_calc" not in st.session_state:
        st.session_state.show_risk_calc = False
    if "faq_open" not in st.session_state:
        st.session_state.faq_open = {i: False for i in range(len(tb_knowledge_base["faqs"]))}

def render_welcome_screen():
    st.markdown("<h1 style='text-align: center; color: #3b82f6; font-size: 3rem; margin-bottom: 1rem;'>TB Health Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.25rem; color: #6b7280; margin-bottom: 2rem;'>Your trusted companion for tuberculosis information and support</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Consultation", key="start_chat", help="Begin your TB health consultation"):
            st.session_state.chat_started = True
            st.rerun()
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    features = [
        {"icon": "💬", "title": "Interactive Chat", "description": "Get instant answers to your TB-related questions"},
        {"icon": "🛡️", "title": "Medical Accuracy", "description": "Information based on WHO and CDC guidelines"},
        {"icon": "👥", "title": "24/7 Support", "description": "Available anytime you need guidance"},
        {"icon": "📚", "title": "Comprehensive Database", "description": "Extensive TB knowledge base and resources"}
    ]
    for i, (col, feature) in enumerate(zip([col1, col2, col3, col4], features)):
        with col:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; border: 1px solid #e5e7eb; border-radius: 0.5rem; background-color: white;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{feature['icon']}</div>
                <h3 style="margin-bottom: 0.5rem;">{feature['title']}</h3>
                <p style="font-size: 0.875rem; color: #6b7280;">{feature['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("---")
    st.info("**Important Notice:** This chatbot provides educational information only. Always consult with healthcare professionals for medical advice, diagnosis, or treatment.")

def render_sidebar():
    with st.sidebar:
        st.markdown("## TB Health Assistant")
        st.markdown("Get reliable information about tuberculosis")
        if st.button("💬 Start New Chat", key="new_chat"):
            st.session_state.messages = [
                {
                    "id": "1",
                    "text": "Hello! I'm your TB Health Assistant. I can help you with information about tuberculosis symptoms, treatment, prevention, and general questions. What would you like to know?",
                    "is_bot": True,
                    "timestamp": datetime.now()
                }
            ]
            st.session_state.chat_started = True
            st.session_state.risk_score = None
            st.session_state.show_risk_calc = False
            st.rerun()

        st.markdown("### Quick Topics")
        st.markdown("Jump to common TB questions")
        quick_topics = [
            {"icon": "🔥", "title": "Symptoms", "description": "Common TB symptoms", "query": "What are TB symptoms?"},
            {"icon": "💊", "title": "Treatment", "description": "Treatment options", "query": "How is TB treated?"},
            {"icon": "🛡️", "title": "Prevention", "description": "How to prevent TB", "query": "How can I prevent TB?"},
            {"icon": "ℹ️", "title": "General Info", "description": "About tuberculosis", "query": "What is tuberculosis?"},
            {"icon": "❓", "title": "FAQs", "description": "Frequently Asked Questions", "query": "Show me some TB FAQs"}
        ]
        for topic in quick_topics:
            if st.button(f"{topic['icon']} {topic['title']}", key=f"topic_{topic['title']}", help=topic['description']):
                if topic['title'] == "FAQs":
                    st.session_state.faq_open = {i: False for i in range(len(tb_knowledge_base["faqs"]))}
                    st.session_state.show_faqs = True
                    st.session_state.chat_started = False
                    st.session_state.show_risk_calc = False
                    st.experimental_rerun()
                else:
                    st.session_state.chat_started = True
                    user_message = {
                        "id": str(len(st.session_state.messages) + 1),
                        "text": topic['query'],
                        "is_bot": False,
                        "timestamp": datetime.now()
                    }
                    st.session_state.messages.append(user_message)
                    bot_response = find_relevant_response(topic['query'])
                    bot_message = {
                        "id": str(len(st.session_state.messages) + 1),
                        "text": bot_response,
                        "is_bot": True,
                        "timestamp": datetime.now()
                    }
                    st.session_state.messages.append(bot_message)
                    st.session_state.show_risk_calc = False
                    st.experimental_rerun()

        st.markdown("---")
        st.markdown("### TB Risk Calculator")
        if st.button("Open Risk Calculator", key="open_risk_calc"):
            st.session_state.show_risk_calc = True
            st.session_state.chat_started = False
            st.session_state.show_faqs = False
            st.experimental_rerun()

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
    <div style="background-color: white; border-bottom: 1px solid #e5e7eb; padding: 1rem; margin-bottom: 1rem;">
        <div style="display: flex; align-items: center;">
            <div style="background-color: #3b82f6; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
                🤖
            </div>
            <div>
                <h2 style="margin: 0; font-weight: 600;">TB Health Assistant</h2>
                <p style="margin: 0; font-size: 0.875rem; color: #6b7280;">Online • Ready to help</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    messages_container = st.container()
    with messages_container:
        for message in st.session_state.messages:
            render_chat_message(message)
    st.markdown("---")
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(
            "Message",
            placeholder="Ask me about TB symptoms, treatment, prevention, FAQs...",
            key="user_input",
            label_visibility="collapsed"
        )
    with col2:
        send_button = st.button("Send 📤", key="send_button")
    if send_button and user_input.strip():
        user_message = {
            "id": str(len(st.session_state.messages) + 1),
            "text": user_input,
            "is_bot": False,
            "timestamp": datetime.now()
        }
        st.session_state.messages.append(user_message)
        with st.spinner("TB Assistant is typing..."):
            time.sleep(1)
        bot_response = find_relevant_response(user_input)
        bot_message = {
            "id": str(len(st.session_state.messages) + 1),
            "text": bot_response,
            "is_bot": True,
            "timestamp": datetime.now()
        }
        st.session_state.messages.append(bot_message)
        st.experimental_rerun()

    st.markdown("""
    <p style="text-align: center; font-size: 0.75rem; color: #9ca3af; margin-top: 1rem;">
        This chatbot provides educational information only. Consult healthcare professionals for medical advice.
    </p>
    """, unsafe_allow_html=True)

def render_faqs():
    st.title("Frequently Asked Questions (FAQs)")
    for i, faq in enumerate(tb_knowledge_base["faqs"]):
        if st.session_state.faq_open.get(i):
            if st.button(f"▼ {faq['question']}", key=f"faq_close_{i}"):
                st.session_state.faq_open[i] = False
                st.experimental_rerun()
            st.markdown(f"<div class='faq-answer'>{faq['answer']}</div>", unsafe_allow_html=True)
        else:
            if st.button(f"▶ {faq['question']}", key=f"faq_open_{i}"):
                st.session_state.faq_open[i] = True
                st.experimental_rerun()
    if st.button("Back to Home"):
        st.session_state.faq_open = {i: False for i in range(len(tb_knowledge_base["faqs"]))}
        st.session_state.chat_started = True
        st.session_state.show_faqs = False
        st.experimental_rerun()

def render_risk_calculator():
    st.title("TB Risk Percentage Calculator")
    st.markdown("Select symptoms you are experiencing:")
    symptom_checks = {}
    for symptom in tb_knowledge_base["symptoms"]:
        symptom_checks[symptom["name"]] = st.checkbox(symptom["name"])
    if st.button("Calculate Risk"):
        score = sum(20 for present in symptom_checks.values() if present)
        st.session_state.risk_score = score
        st.success(f"Your estimated TB risk is {score}%.")
        if score >= 60:
            st.warning("High risk detected. Please consult a healthcare professional immediately.")
        elif score >= 30:
            st.info("Moderate risk. Consider consulting a healthcare professional.")
        else:
            st.info("Low risk, but stay alert and monitor symptoms.")
    if st.session_state.risk_score is not None:
        st.markdown(f"### Last Calculated Risk: {st.session_state.risk_score}%")
    if st.button("Back to Home"):
        st.session_state.show_risk_calc = False
        st.session_state.chat_started = True
        st.experimental_rerun()

def main():
    initialize_session_state()
    render_sidebar()
    if getattr(st.session_state, "show_faqs", False):
        render_faqs()
    elif st.session_state.show_risk_calc:
        render_risk_calculator()
    elif st.session_state.chat_started:
        render_chat_interface()
    else:
        render_welcome_screen()

if __name__ == "__main__":
    main()
