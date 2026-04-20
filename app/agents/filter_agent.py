import json

from app.services.llm import llm

KEYWORDS_WEIGHT = 0.6
LLM_WEIGHT = 0.4

async def filter_agent(state):
    query = state["query"].lower()
    query_terms = set(query.split())

    filtered = []

    for job in state.get("jobs_parsed", []):
        desc = job.get("description", "").lower()

        match_count = sum(1 for word in query_terms if word in desc)
        keyword_score = match_count / max(len(query_terms), 1)
        
        try:
            prompt = f"""
            Rate relevance between 0 to 100.
            Query: {query}
            Job: {desc[:5000]}
            Only return a number.
            """
            llm_response = llm.invoke(prompt).content.strip()
            llm_score = float(''.join(filter(str.isdigit, llm_response)) or 0) / 100
        except Exception as e:
            llm_score = 0.3  # fallback

        final_score = (KEYWORDS_WEIGHT * keyword_score) + (LLM_WEIGHT * llm_score)
        job["keyword_score"] = round(keyword_score, 2)
        job["llm_score"] = round(llm_score, 2)
        job["final_score"] = round(final_score, 2)

        if final_score > 0.2:  # low threshold to avoid zero results
            filtered.append(job)

    if not filtered:
        print("Fallback triggered: returning top parsed jobs")
        filtered = state.get("jobs_parsed", [])[:50]

    state["jobs_filtered"] = filtered
    # Debugging output
    print("FILTERED:", len(state.get("jobs_filtered", [])))
    # print('Formatted filtered jobs sample:', json.dumps(state["jobs_filtered"][:2], indent=4))
    return state