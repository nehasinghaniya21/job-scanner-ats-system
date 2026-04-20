from flask import json
from app.services.llm import llm

async def rank_agent(state):
    for job in state.get("jobs_filtered", []):
        try:
            score = llm.invoke(f"Score 0-100: {job['description']}").content
            job["score"] = score
        except:
            job["score"] = "N/A"

    state["jobs_ranked"] = state.get("jobs_filtered", [])
    # Debugging output
    print("RANKED:", len(state.get("jobs_ranked", [])))
    # print('Formatted ranked jobs sample:', json.dumps(state["jobs_ranked"][:2], indent=4))
    return state