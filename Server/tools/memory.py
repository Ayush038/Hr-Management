from datetime import datetime
from db import db



def save_message(session_id: str, role: str, stage: str, content: str):
    db.messages.insert_one({
        "session_id": session_id,
        "role": role,
        "stage": stage,
        "content": content,
        "timestamp": datetime.utcnow()
    })

def save_evaluation(session_id, question, answer, scores):
    db.evaluations.insert_one({
        "session_id": session_id,
        "question": question,
        "answer": answer,
        "scores": scores,
        "timestamp": datetime.utcnow()
    })

def get_evaluations(session_id: str):
    return list(db.evaluations.find(
        {"session_id": session_id}
    ))

def get_messages(session_id: str):
    return list(db.messages.find(
        {"session_id": session_id}
    ).sort("timestamp", 1))