from flask import Flask, render_template, request, jsonify, send_file
import asyncio
import json
from langchain_groq import ChatGroq
import pandas as pd
from io import BytesIO
from app.graph.workflow import build_graph
import pdfplumber
import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=GROQ_API_KEY)
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")
    location = request.form.get("location")

    graph = build_graph()
    state = {"query": f"{query} {location}"}

    result = asyncio.run(graph.ainvoke(state))
    jobs = result.get("jobs_ranked", [])

    return jsonify(jobs)


@app.route("/download", methods=["POST"])
def download():
    data = request.json
    df = pd.DataFrame(data)

    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="jobs.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.route("/cv-scanner", methods=["GET", "POST"])
def cv_scanner():
    #print(f"DEBUG: GROQ_API_KEY is {'SET' if os.getenv('GROQ_API_KEY') else 'MISSING'}")

    if request.method == "GET":
        return render_template("cv_scanner.html")

    file = request.files.get("cv")
    job_desc = request.form.get("job_description")

    if not file or not job_desc:
        return jsonify({"error": "Missing inputs"}), 400

    # -----------------------------
    # EXTRACT TEXT FROM PDF
    # -----------------------------
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    print(f"DEBUG: Extracted {len(text)} characters from CV")
    print("DEBUG: Sample extracted text:", text[:5000])
    # -----------------------------
    # LLM ANALYSIS
    # -----------------------------
    prompt = f"""You are an excellent ATS system. Analyze the resume against the job description.

        Resume:
        {text}

        Job Description:
        {job_desc}

        Return ONLY valid JSON (no markdown, no extra text):
        {{
            "ats_score": <number 0-100>,
            "match_score": <number 0-100>,
            "missing_keywords": [<list of strings>],
            "strengths": [<list of strings>],
            "improvements": [<list of strings>],
            "cv_ranking": {{
                "searchability": <number 0-100>,
                "hard_skills": <number 0-100>,
                "soft_skills": <number 0-100>,
                "formatting": <number 0-100>
            }},
            "cv_points": [<list of 5-7 actual bullet points ready to add to CV in this format: "Developed AI agent architecture using LangChain for real-time data processing" - ONLY bullet points, no "Highlight" or "Add" statements>],
            "summary": "<string>"
        }}"""

    response = llm.invoke(prompt)
    print("DEBUG: Full LLM response:", response.content)
    
    # Parse JSON response from LLM - handle markdown code blocks
    try:
        response_text = response.content.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]  # Remove ```json
        elif response_text.startswith("```"):
            response_text = response_text[3:]  # Remove ```
        
        if response_text.endswith("```"):
            response_text = response_text[:-3]  # Remove trailing ```
        
        response_text = response_text.strip()
        
        print(f"DEBUG: Cleaned response: {response_text}")
        
        if not response_text:
            return jsonify({"error": "Empty response from LLM"}), 500
        
        analysis = json.loads(response_text)
        
        # Validate required fields
        if not isinstance(analysis, dict):
            return jsonify({"error": "Response is not a JSON object"}), 500
        
        # Ensure required fields exist
        analysis.setdefault("ats_score", 0)
        analysis.setdefault("match_score", 0)
        analysis.setdefault("missing_keywords", [])
        analysis.setdefault("improvements", [])
        analysis.setdefault("strengths", [])
        analysis.setdefault("cv_points", [])
        analysis.setdefault("cv_ranking", {
            "searchability": 0,
            "hard_skills": 0,
            "soft_skills": 0,
            "formatting": 0
        })
        analysis.setdefault("summary", "Analysis complete")
        
        return jsonify(analysis)
        
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse LLM response: {e}")
        print(f"Response content: {response.content}")
        return jsonify({"error": f"Failed to parse response: {str(e)}"}), 500
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)