# AI Resume Evaluator

An AI-powered resume evaluation system that analyzes how well a candidate fits a given job role using Large Language Models (LLMs).

The application takes a **Job Description** and a **Candidate Resume (PDF/DOCX)**, extracts meaningful information from both, and generates a detailed candidate compatibility analysis.

The system works like an AI recruitment assistant that helps identify:

- Candidate-job fit score
- Matching skills
- Missing skills
- Relevant experience
- Strengths and weaknesses
- Final hiring recommendation

---

## Features

### Resume Analysis

- Supports:
  - PDF resumes
  - DOCX resumes

- Extracts:
  - Candidate information
  - Technical skills
  - Education
  - Projects
  - Work experience
  - Certifications

---

### Job Description Analysis

The system analyzes job descriptions and extracts:

- Role information
- Required skills
- Preferred skills
- Education requirements
- Responsibilities
- Experience requirements

---

### AI-Powered Evaluation

Using LLMs, the application compares:

```
Job Requirements
        +
Candidate Profile
        |
        ↓
AI Evaluation
        |
        ↓
Candidate Match Score
```

The output includes:

- Overall compatibility score
- Skills matched
- Missing requirements
- Candidate strengths
- Areas of improvement
- Final recommendation

---

# Tech Stack

## Backend / AI Pipeline

- Python
- Groq API
- LLM:
  - GPT-OSS-120B
- Pydantic
- JSON structured outputs

---

## Document Processing

- PyPDF
- python-docx

Used for extracting text from:

- PDF files
- Microsoft Word documents

---

## Frontend

- Streamlit

Provides:

- Resume upload interface
- Job description input
- Evaluation dashboard
- Result visualization

---

# Architecture

```
                    User
                     |
        -----------------------------
        |                           |
 Job Description              Resume Upload
        |                           |
        ↓                           ↓
  JD Parser                  PDF/DOCX Extractor
        |                           |
        ↓                           ↓
    Job Schema              Resume Text
                                    |
                                    ↓
                            Resume Parser
                                    |
                                    ↓
                             Resume Schema

                    Job Schema + Resume Schema

                              |
                              ↓

                         AI Evaluator

                              |
                              ↓

                    Candidate Evaluation Report
```

---

---

# How It Works

## 1. Upload Resume

The user uploads:

```
resume.pdf
```

or:

```
resume.docx
```

The application extracts the text from the document.

---

## 2. Parse Resume

The extracted resume text is sent to the LLM.

The LLM converts unstructured resume information into structured data:

Example:

```json
{
  "skills": [
    "Python",
    "React",
    "Machine Learning"
  ],
  "projects": [
    "AI Resume Evaluator"
  ]
}
```

---

## 3. Parse Job Description

The job description is analyzed and converted into structured requirements:

Example:

```json
{
  "role": "Software Engineering Intern",
  "required_skills": [
    "Python",
    "Java",
    "System Design"
  ]
}
```

---

## 4. Candidate Evaluation

The AI compares:

```
Candidate Resume

against

Job Requirements
```

and generates:

```json
{
  "score": 85,
  "matching_skills": [
    "Python",
    "JavaScript"
  ],
  "missing_skills": [
    "AWS"
  ],
  "verdict": "Strong candidate"
}
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/<username>/<repository-name>.git

cd resume-evaluator
```

---

## Create Environment

Using uv:

```bash
uv sync
```

or using pip:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

# Running the Application

Start Streamlit:

```bash
streamlit run main.py
```

or with uv:

```bash
uv run streamlit run main.py
```

The application will open at:

```
http://localhost:8501
```

---

# Example Output

The evaluator generates:

## Candidate Score

```
Match Score: 87%
```

## Matching Skills

```
✓ Python
✓ React
✓ SQL
✓ Machine Learning
```

## Missing Skills

```
× AWS
× Docker
```

## Recommendation

```
Strong candidate. Recommended for technical interview.
```

---

# Future Improvements

## Better Frontend

The current Streamlit interface is a functional prototype.

Future improvements:

- Modern dashboard UI
- Better visualizations
- Candidate comparison interface
- Resume analytics dashboard
- Interactive skill matching graphs

---

## ATS Compatibility Score

Add:

- Resume keyword analysis
- Missing keyword suggestions
- Formatting analysis
- Recruiter-style ATS score

---

## Multiple Candidate Ranking

Allow recruiters to upload multiple resumes:

```
Candidate A → 92%
Candidate B → 84%
Candidate C → 76%
```

---

## Interview Question Generation

Generate personalized interview questions based on:

- Resume projects
- Missing skills
- Job requirements

---

# Security Notes

- API keys are stored using environment variables.
- `.env` files should never be committed.
- Production deployments should use secret management systems.

---

# Author

Built as an AI engineering project demonstrating:

- LLM application development
- Structured AI outputs
- Document processing
- Prompt engineering
- AI-powered decision support
