from flask import json
from playwright.async_api import async_playwright
from datetime import datetime
async def parse_agent(state):
    parsed = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for job in state["jobs_raw"][:50]:  # limit parsing to top 50
            try:
                page = await browser.new_page()
                # Get the URL from possible fields
                url = job.get("absolute_url") or job.get("url") or job.get("apply_url")
                if not url:
                    continue

                # Get the job title from possible fields
                title = job.get("title") or job.get("position") or "N/A"
                if not title:
                    continue

                # Get the description from possible fields
                content = job.get("description") or job.get("details")
                if not content:
                    await page.goto(url, timeout=30000)
                    content = await page.locator("body").inner_text()

                # Handle location which can be a string or an object
                location_data = job.get("location")
                if isinstance(location_data, dict):
                    # It's an object, so get the "name" key
                    location = location_data.get("name", "N/A").strip()
                elif isinstance(location_data, str):
                    location = location_data.strip()
                else:
                    location = "N/A"
                # Handle date which can be in various formats
                date = job.get("date") or job.get("created") or job.get("first_published") or "N/A"
                dt = datetime.fromisoformat(date)
                date  = dt.strftime("%Y-%m-%d") if date != "N/A" else "N/A"

                # Create a parsed job entry
                parsed.append({
                    "title": title,
                    "company": job.get("company") or job.get("company_name") or "N/A",
                    "date": date,
                    "location": location,
                    "url": url,
                    "description": content[:5000]
                })
            except Exception as e:
                print("Parse error:", e)

        await browser.close()

    state["jobs_parsed"] = parsed
    # Debugging output
    print("PARSED:", len(state.get("jobs_parsed", [])))
    # print('Formatted parsed jobs sample:', json.dumps(state["jobs_parsed"][:2], indent=4))
    return state