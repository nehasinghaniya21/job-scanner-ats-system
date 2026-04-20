import httpx
import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

ADZUNA_API_ID = os.getenv("ADZUNA_API_ID")
ADZUNA_API_KEY = os.getenv("ADZUNA_API_KEY")

TIMEOUT = httpx.Timeout(15.0)

async def safe_fetch(url):
    for attempt in range(3):  # retry
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                res = await client.get(url)
                res.raise_for_status()
                return res.json()
        except Exception as e:
            print(f"Retry {attempt+1} failed for {url}: {e}")
            await asyncio.sleep(2 ** attempt)
    return []

async def fetch_greenhouse(company):
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    data = await safe_fetch(url)
    return data.get("jobs", []) if isinstance(data, dict) else []

async def fetch_remoteok():
    return await safe_fetch("https://remoteok.com/api")

async def fetch_adzuna(query):
    url = f"https://api.adzuna.com/v1/api/jobs/us/search/1?what={query}&app_id={ADZUNA_API_ID}&app_key={ADZUNA_API_KEY}"

    data = await safe_fetch(url)

    return data.get("results", [])