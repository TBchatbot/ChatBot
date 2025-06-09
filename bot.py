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

def initialize_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "show_faqs" not in st.session_state:
        st.session_state.show_faqs = False
    if "show_risk_calculator" not in st.session_state:
        st.session_state.show_risk_calculator = False
    if "risk_score" not in st.session_state:
        st.session_state.risk_score = 0
    if "risk_messages" not in st.session_state:
        st.session_state.risk_messages = []

def add_message(role, content):
    st.session_state.chat_history.append({"role": role, "content": content})

def clear_chat():
    st.session_state.chat_history = []
    st.session_state.user_input = ""

def reset_risk_calculator():
    st.session_state.risk_score = 0
    st.session_state.risk_messages = []

def risk_calculator():
    st.markdown("### TB Risk Calculator")
    symptom = st.selectbox("Do you have a persistent cough for more than 2 weeks?", ["Yes", "No"])
    if symptom == "Yes":
        st.session_state.risk_score += 3
        st.session_state.risk_messages.append("Persistent cough +3")
    fever = st.selectbox("Do you have fever or night sweats?", ["Yes", "No"])
    if fever == "Yes":
        st.session_state.risk_score += 2
        st.session_state.risk_messages.append("Fever/Night sweats +2")
    weight_loss = st.selectbox("Have you experienced unexplained weight loss?", ["Yes", "No"])
    if weight_loss == "Yes":
        st.session_state.risk_score += 2
        st.session_state.risk_messages.append("Weight loss +2")
    contact = st.selectbox("Have you been in contact with a TB patient?", ["Yes", "No"])
    if contact == "Yes":
        st.session_state.risk_score += 3
        st.session_state.risk_messages.append("Contact with TB patient +3")
    smoking = st.selectbox("Are you a smoker?", ["Yes", "No"])
    if smoking == "Yes":
        st.session_state.risk_score += 1
        st.session_state.risk_messages.append("Smoking +1")
    if st.button("Calculate Risk"):
        st.success(f"Your TB risk score is: {st.session_state.risk_score}")
        if st.session_state.risk_score >= 5:
            st.warning("High risk. Please consult a healthcare professional.")
        else:
            st.info("Low risk. Maintain healthy habits and monitor symptoms.")
        reset_risk_calculator()

def show_faq():
    st.markdown("### TB FAQs")
    for faq in tb_knowledge_base:
        with st.expander(faq["question"]):
            st.write(faq["answer"])

def main():
    initialize_session_state()

    st.sidebar.title("TB Health Assistant")
    if st.sidebar.button("Start New Chat"):
        clear_chat()
        st.session_state.show_faqs = False
        st.session_state.show_risk_calculator = False
        st.experimental_rerun()

    if st.sidebar.button("Open Risk Calculator"):
        st.session_state.show_risk_calculator = True
        st.session_state.show_faqs = False
        clear_chat()
        st.experimental_rerun()

    quick_topics = ["What is TB?", "Symptoms", "Treatment", "Prevention"]
    st.sidebar.markdown("### Quick Topics")
    for topic in quick_topics:
        if st.sidebar.button(topic):
            st.session_state.show_faqs = True
            st.session_state.show_risk_calculator = False
            add_message("user", topic)
            add_message("bot", tb_knowledge_base.get(topic, "Sorry, I don't have info on that topic."))
            st.experimental_rerun()

    if st.session_state.show_risk_calculator:
        risk_calculator()
        return

    if st.session_state.show_faqs:
        show_faq()
        if st.button("Back to Chat"):
            st.session_state.show_faqs = False
            clear_chat()
            st.experimental_rerun()
        return

    st.title("TB Health Assistant Chat")

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Bot:** {msg['content']}")

    user_input = st.text_input("Your message:", value=st.session_state.user_input, key="input")
    st.session_state.user_input = user_input

    if st.button("Send") and user_input.strip():
        add_message("user", user_input)
        add_message("bot", f"Echo: {user_input}")
        st.session_state.user_input = ""
        st.experimental_rerun()

if __name__ == "__main__":
    main()
