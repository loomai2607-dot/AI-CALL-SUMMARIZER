from utils.llm import call_llm

def summarize_call(transcript: str) -> str:
    prompt = f"Summarize this call:\n{transcript}"
    return call_llm(prompt)