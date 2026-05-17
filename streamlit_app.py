import streamlit as st
import requests

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# TITLE
# -----------------------------

st.title("🤖 SHL Assessment Recommender")

st.markdown(
    "Get the best SHL assessments based on hiring requirements."
)

# -----------------------------
# SESSION STATE
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# USER INPUT
# -----------------------------

prompt = st.chat_input("Enter hiring requirement...")

if prompt:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # -----------------------------
    # API CALL
    # -----------------------------

    api_url = "http://127.0.0.1:8000/chat"
    
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    assistant_reply = ""

    try:

        response = requests.post(
            api_url,
            json=payload,
            timeout=60
        )

        # Check status
        if response.status_code != 200:

            assistant_reply = (
                "Backend server error. "
                "Please wait a few seconds and try again."
            )

        else:

            try:

                data = response.json()

                assistant_reply = data.get(
                    "reply",
                    "No response received."
                )

                recommendations = data.get(
                    "recommendations",
                    []
                )

                if recommendations:

                    assistant_reply += "\n\n### Recommended Assessments:\n"

                    for item in recommendations:

                        assistant_reply += f"""
- **{item['name']}**
  - Type: {item['test_type']}
  - [Open Assessment]({item['url']})
"""

            except Exception:

                assistant_reply = (
                    "Invalid response received from backend."
                )

    except requests.exceptions.Timeout:

        assistant_reply = (
            "Server is waking up. Please try again in 30 seconds."
        )

    except Exception as e:

        assistant_reply = f"Error: {str(e)}"

    # -----------------------------
    # SAVE ASSISTANT MESSAGE
    # -----------------------------

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

    # -----------------------------
    # DISPLAY ASSISTANT MESSAGE
    # -----------------------------

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)