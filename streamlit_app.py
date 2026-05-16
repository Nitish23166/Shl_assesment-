import streamlit as st
import requests

# --------------------------------
# Page Config
# --------------------------------

st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 SHL Assessment Recommender")

st.markdown(
    "Chat with the AI agent to find the best SHL assessments for hiring."
)

# --------------------------------
# Session State for Chat History
# --------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------
# Display Previous Messages
# --------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        # Show recommendations if present
        if "recommendations" in message:

            for rec in message["recommendations"]:

                st.markdown(f"### {rec['name']}")
                st.markdown(f"**Type:** {rec['test_type']}")
                st.markdown(f"[Open Assessment]({rec['url']})")

# --------------------------------
# User Input
# --------------------------------

user_input = st.chat_input("Enter hiring requirement...")

if user_input:

    # Add user message to chat
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # --------------------------------
    # Prepare API Payload
    # --------------------------------

    payload = {
        "messages": [
            {
                "role": msg["role"],
                "content": msg["content"]
            }
            for msg in st.session_state.messages
        ]
    }

    # --------------------------------
    # Call FastAPI Backend
    # --------------------------------

    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json=payload
    )

    data = response.json()

    assistant_reply = data["reply"]

    recommendations = data.get("recommendations", [])

    # --------------------------------
    # Display Assistant Response
    # --------------------------------

    with st.chat_message("assistant"):

        st.markdown(assistant_reply)

        for rec in recommendations:

            st.markdown(f"### {rec['name']}")
            st.markdown(f"**Type:** {rec['test_type']}")
            st.markdown(f"[Open Assessment]({rec['url']})")

    # --------------------------------
    # Save Assistant Message
    # --------------------------------

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_reply,
        "recommendations": recommendations
    })