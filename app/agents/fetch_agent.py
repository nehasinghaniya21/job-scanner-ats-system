import asyncio
import json

from flask import json
from app.services.api_clients import fetch_greenhouse, fetch_remoteok, fetch_adzuna

async def fetch_agent(state):
    print("Fetching jobs...")
    GREENHOUSE_COMPANIES = [
        "stripe",
        "airbnb",
        "coinbase",
        "robinhood",
        "figma",
        "databricks",
        "discord",
        "seatgeek",
        "anthropic",
        "coursera",
    ]
    tasks = [
        fetch_greenhouse(company)
        for company in GREENHOUSE_COMPANIES
    ]
    query = state["query"].lower()

    results = await asyncio.gather(
        *tasks,
        fetch_remoteok(),
        fetch_adzuna(query),
        return_exceptions=True
    )
    print("Fetching completed...")
    jobs = []
    for r in results:
        if isinstance(r, Exception):
            print("Error in fetch:", r)
            continue
        jobs.extend(r[:10])  # limit

    filtered_jobs = [
        job for job in jobs
        if matches_query(job, query)
    ]

    state["jobs_raw"] = filtered_jobs[:5]
    # Debugging output    
    print("RAW:", len(state.get("jobs_raw", [])))
    # print('Formatted jobs sample:', json.dumps(state["jobs_raw"][:2], indent=4))

    return state

def matches_query(job, query):
    text = (job.get("title", "") + " " + str(job)).lower()
    return all(word in text for word in query.split())