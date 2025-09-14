from fastapi import FastAPI, UploadFile, File, HTTPException
from agents.workflow import run_call_summary_workflow
import uuid
import os

import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-call")
async def upload_call(file: UploadFile = File(...)):
    if file.content_type not in ["audio/wav", "audio/mpeg", "audio/mp4", "audio/x-wav"]:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    audio_id = str(uuid.uuid4())
    audio_path = f"temp/{audio_id}_{file.filename}"
    os.makedirs("temp", exist_ok=True)
    with open(audio_path, "wb") as f:
        f.write(await file.read())

    try:
        result = run_call_summary_workflow(audio_path)
        return {
        "transcript": result.get("transcript"),
        "entities": result.get("entities"),
        "summary": result.get("summary"),
        "recommendations": result.get("recommendations"),
        "trace": result.get("trace", [])
    }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(audio_path)

    return result


if __name__ == "__main__" :
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)