from utils.llm import call_llm

def recommend_actions(entities: dict) -> str:
    prompt = f"Based on these entities, recommend next steps:\n{entities}"
    return call_llm(prompt)