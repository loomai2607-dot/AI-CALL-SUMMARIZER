from utils.llm import call_llm

def extract_entities(transcript: str) -> dict:
    prompt = f"Extract structured info from this transcript:\n{transcript}"
    return call_llm(prompt, output_format="json")