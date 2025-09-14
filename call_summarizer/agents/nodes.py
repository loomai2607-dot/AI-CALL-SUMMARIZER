from autogen import AssistantAgent, UserProxyAgent
from utils.llm import call_llm
from agents.transcription import transcribe_audio
from dotenv import load_dotenv
import json
from agents.trace_logger import trace_logger


load_dotenv()


def log_trace(name, input_data, output_data, status="success"):
    trace_logger.append({
        "name": name,
        "input": input_data,
        "output": output_data,
        "status": status
    })
    print("trace_logger",trace_logger)

def get_agent_nodes():
    # Dummy tool agents (not LLM-backed)
    user_proxy = UserProxyAgent(name="user_proxy", human_input_mode="NEVER")
    transcription_agent = AssistantAgent(name="TranscriptionAgent", code_execution_config={"use_docker": False})
    entity_agent = AssistantAgent(name="EntityExtractionAgent", code_execution_config={"use_docker": False})
    summary_agent = AssistantAgent(name="SummarizationAgent", code_execution_config={"use_docker": False})
    recommendation_agent = AssistantAgent(name="RecommendationAgent", code_execution_config={"use_docker": False})

    return {
        "transcription": lambda state: (
            lambda result: (
                log_trace("transcription", {"audio_path": state["audio_path"]}, {"transcript": result}),
                {**state, "transcript": result}
            )[1]
        )(str(transcribe_audio(state["audio_path"]))),

        "entity_extraction": lambda state: (
            (_ for _ in ()).throw(ValueError("❌ Transcript missing in state!"))
            if not state.get("transcript")
            else (
                lambda result: (
                    log_trace("entity_extraction", {"transcript": state["transcript"]}, {"entities": result}),
                    {**state, "entities": result}
                )[1]
            )(call_llm(
                f"""Extract key entities from the following transcript.\nReturn a valid JSON list of entity strings.\n\nTranscript:\n{state['transcript']}"""
            ))
        ),

        "summarization": lambda state: (
            lambda result: (
                log_trace("summarization", {"transcript": state["transcript"]}, {"summary": result}),
                {**state, "summary": result}
            )[1]
        )(call_llm(
            f"Summarize this transcript:\n\n{state['transcript']},  return only a valid json of the caller questions list with 'member_questtions' as key, the responder answers as list with 'agenet_answer' as key , the actions agreed as 'agreed_actions' as key , the semntiment of the call as 'sentiment' as key and give positive/negative/neutral as value based on the call and based on the sentiment give 'is_resolved' as key and give value as true/false based on the sentiment of the call. Return only a valid JSON object with these keys."
        )),

        "recommendation": lambda state: (
            lambda result: (
                log_trace("recommendation", {
                    "entities": state.get("entities"),
                    "summary": state.get("summary")
                }, {"recommendations": result}),
                {**state, "recommendations": result}
            )[1]
        )(call_llm(
            f"""Based on these entities: {json.dumps(state['entities'], indent=2)}\nand the summary: {state['summary']}\nWhat actions should be taken next?"""
        )),
    }
