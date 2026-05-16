from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from retriever import retrieve_assessments

app = FastAPI()


# -----------------------------
# Request Schema
# -----------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# -----------------------------
# Helper Functions
# -----------------------------

def is_vague(query):

    query = query.lower().strip()

    vague_terms = [
        "assessment",
        "test",
        "hiring",
        "job",
        "need assessment"
    ]

    if len(query.split()) < 3:
        return True

    if query in vague_terms:
        return True

    return False


def is_off_topic(query):

    allowed_keywords = [
        "developer",
        "engineer",
        "manager",
        "assessment",
        "test",
        "hiring",
        "role",
        "skills",
        "personality",
        "java",
        "python",
        "analyst",
        "backend",
        "frontend",
        "leadership",
        "compare",
        "difference",
        "opq",
        "gsa"
    ]

    query = query.lower()

    return not any(word in query for word in allowed_keywords)


# -----------------------------
# Health Endpoint
# -----------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------
# Chat Endpoint
# -----------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    messages = request.messages

    # Combine all user messages
    conversation_text = " ".join(
        [msg.content for msg in messages if msg.role == "user"]
    )

    # -----------------------------
    # Off-topic detection
    # -----------------------------

    if is_off_topic(conversation_text):

        return {
            "reply": "I can only help with SHL assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Vague query detection
    # -----------------------------

    if is_vague(conversation_text):

        return {
            "reply": "Sure. What role are you hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Comparison Mode
    # -----------------------------

    if "difference" in conversation_text.lower() or "compare" in conversation_text.lower():

        results = retrieve_assessments(conversation_text, k=2)

        if len(results) >= 2:

            first = results[0]
            second = results[1]

            return {
                "reply": f"""
{first['name']} is mainly designed for assessing {', '.join(first['keys'])}.

{second['name']} focuses more on {', '.join(second['keys'])}.

Both assessments are useful for different hiring needs depending on whether you want technical, behavioral, competency, or personality evaluation.
""",
                "recommendations": [],
                "end_of_conversation": False
            }

    # -----------------------------
    # Retrieve assessments
    # -----------------------------

    results = retrieve_assessments(conversation_text, k=5)

    recommendations = []

    for item in results:

        recommendations.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": ", ".join(item["keys"])
        })

    return {
        "reply": "Here are some SHL assessments that match your hiring needs.",
        "recommendations": recommendations,
        "end_of_conversation": True
    }