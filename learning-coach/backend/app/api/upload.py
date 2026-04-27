from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd, io
from app.mcp.tool4_question_generator import QUESTION_BANK

router = APIRouter()

@router.post("/upload/dataset")
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Only CSV files supported")
    content = await file.read()
    try:
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))
        added = 0
        for _, row in df.iterrows():
            topic = str(row.get("topic", "General")).strip()
            try:
                entry = {
                    "question": str(row["question"]).strip(),
                    "options": [str(row.get("option_a","A")), str(row.get("option_b","B")),
                                str(row.get("option_c","C")), str(row["correct_answer"])],
                    "correct_answer": str(row["correct_answer"]).strip(),
                    "explanation": str(row.get("explanation","")).strip(),
                    "difficulty": int(row.get("difficulty", 2)),
                    "topic": topic,
                }
                QUESTION_BANK.setdefault(topic, []).append(entry)
                added += 1
            except Exception:
                continue
        return {"message": f"Imported {added} questions", "topics": list(df["topic"].unique())}
    except Exception as e:
        raise HTTPException(500, str(e))
