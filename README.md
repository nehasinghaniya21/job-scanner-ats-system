# Jobs Aggregator + CV Scanner

An intelligent job aggregation and CV analysis platform powered by AI. Search for jobs across multiple sources and optimize your resume with AI-driven insights.

## 🎯 Features

### 1. **Job Aggregator** 🔍
- **Multi-Agent Pipeline**: Fetch → Parse → Filter → Rank
- **Async Job Fetching**: Concurrent requests from multiple job sources
- **Intelligent Filtering**: AI-powered job matching using Groq LLM
- **Smart Ranking**: Jobs ranked by relevance to your query
- **Excel Export**: Download results as formatted Excel files
- **Web-based Search**: Simple UI for job search with location filters

### 2. **CV Scanner** 📋
- **ATS Score Analysis**: Measures how well your CV passes Applicant Tracking Systems
- **Match Score**: Calculates resume-to-job-description compatibility
- **Comprehensive CV Ranking**:
  - Searchability: Keywords & ATS visibility
  - Hard Skills: Technical requirements match
  - Soft Skills: Interpersonal & leadership capabilities  
  - Formatting: Structure & readability assessment
- **Missing Keywords Detection**: Identifies skills from job description not in your resume
- **Strengths Identification**: Highlights what's working well in your CV
- **Improvement Suggestions**: Actionable recommendations to strengthen your resume
- **Ready-to-Add Bullet Points**: AI-generated bullet points tailored to the job description (copy-to-clipboard ready)
- **PDF Upload Support**: Drag-and-drop resume upload

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask
- **LLM**: Groq (llama-3.1-8b-instant)
- **Libraries**: 
  - LangChain: For agent orchestration and LLM interactions
  - Playwright: For web scraping and dynamic content parsing
  - pdfplumber: PDF text extraction
  - pandas: Data manipulation and Excel export

### Frontend
- **HTML/CSS**: Tailwind CSS for responsive design
- **JavaScript**: Vanilla JS for interactivity, drag-and-drop, clipboard operations
- **UI Components**: Custom styled cards, progress bars, animations

### Environment
- **Python**: 3.x
- **Virtual Environment**: venv (recommended)

## 📋 Prerequisites

- Python 3.9+
- pip (Python package manager)
- Groq API Key (get from [Groq Console](https://console.groq.com))
- Modern web browser

## ⚙️ Setup Instructions

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd jobs-aggregator
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Playwright Browser
```bash
playwright install
```

### Step 5: Configure Environment Variables
Create a `.env` file in the root directory:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from [Groq Console](https://console.groq.com/keys)

### Step 6: Verify Setup
```bash
python -c "from app.graph.workflow import build_graph; print('Setup successful!')"
```

## 🚀 Execution

### Start the Application
```bash
source .venv/bin/activate  # Activate virtual environment
python main.py
```

The application will start at: **http://localhost:5000**

### Usage

#### **Job Search**
1. Navigate to **Home** page (http://localhost:5000/)
2. Enter job title and location
3. Click "Search"
4. Results display with job title, company, location, and relevance score
5. Click "Download" to export results as Excel file

#### **CV Scanner**
1. Navigate to **CV Scanner** page (http://localhost:5000/cv-scanner)
2. **Upload your CV**: Drag & drop or click to select PDF file
3. **Paste Job Description**: Copy and paste the target job description
4. Click **"Analyze Resume"**
5. View comprehensive analysis:
   - ATS Score & Match Score
   - CV Ranking breakdown (Searchability, Hard Skills, Soft Skills, Formatting)
   - Missing Keywords
   - Your Strengths
   - Improvement Suggestions
   - Ready-to-Add Bullet Points (copy-to-clipboard)

## 📁 Project Structure

```
jobs-aggregator/
├── main.py                 # Flask application & routes
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create this)
│
├── app/
│   ├── agents/
│   │   ├── fetch_agent.py    # Job fetching agent
│   │   ├── parse_agent.py    # HTML parsing agent
│   │   ├── filter_agent.py   # AI filtering agent
│   │   └── rank_agent.py     # Relevance ranking agent
│   │
│   ├── graph/
│   │   └── workflow.py       # LangGraph orchestration
│   │
│   └── services/
│       ├── api_clients.py    # Job API integrations
│       └── llm.py            # LLM configuration
│
├── templates/
│   ├── index.html           # Job search interface
│   └── cv_scanner.html      # CV scanner interface
│
└── static/
    ├── script.js            # Frontend logic
    ├── styles/
    │   └── style.css        # Custom styles
    └── images/              # UI assets
```

## 🔑 Key Features Explained

### Job Aggregator Architecture
- **Fetch Agent**: Retrieves job listings from multiple sources concurrently
- **Parse Agent**: Extracts relevant information (Playwright for dynamic content)
- **Filter Agent**: Uses AI to filter jobs matching your criteria
- **Rank Agent**: Sorts results by relevance score

### CV Scanner Intelligence
- **PDF Processing**: Extracts and analyzes CV content
- **LLM Analysis**: Uses Groq's llama-3.1-8b model for intelligent scoring
- **Multi-dimensional Scoring**: 
  - ATS Score: 0-100 (how well it passes ATS systems)
  - Match Score: 0-100 (relevance to job description)
  - Component Ranking: 4 separate scores for detailed insights

## 🐛 Troubleshooting

### Issue: "GROQ_API_KEY is MISSING"
**Solution**: Make sure `.env` file exists and contains your valid Groq API key

### Issue: PDF Upload Fails
**Solution**: Ensure the PDF file is not corrupted and is in a standard format

### Issue: Port 5000 Already in Use
**Solution**: Change port in `main.py`:
```python
app.run(debug=True, port=5001)
```

## 📊 Sample Output

**Job Search Results**: Excel file with columns:
- Job Title
- Company
- Location
- Link
- Match Score
- Description

**CV Scanner Results**: 
- Scores & Rankings
- Missing Keywords List
- Strengths & Improvements
- Copy-ready Bullet Points

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📝 License

This project is open source and available under the MIT License.

## 🔗 Resources

- [Groq Documentation](https://console.groq.com/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [Playwright Documentation](https://playwright.dev/python/)
- [Tailwind CSS](https://tailwindcss.com/)

---
