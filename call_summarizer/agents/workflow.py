from agents.workflow_graph import create_call_graph
from agents.trace_logger import trace_logger  # Import external trace logger

def run_call_summary_workflow(audio_path: str):
    # Reset trace logger for a fresh run
    trace_logger.clear()

    graph = create_call_graph()
    initial_state = {
        "audio_path": audio_path,
        # No need to include 'trace' in state anymore
    }
    result = graph.invoke(initial_state)

    # Attach external trace log to result
    return {
        **result,
        "trace": trace_logger
    }
