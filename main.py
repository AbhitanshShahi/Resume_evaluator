import streamlit as st
from pathlib import Path
import os

from resume_parser import (
    resume_reader,
    resume_parser,
    score_calc,
    parse_job_description
)

# --- Configuration ---
st.set_page_config(
    page_title="AI Resume Evaluator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS ---
def load_css():
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1E3A8A;
            margin-bottom: 0px;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #6B7280;
            margin-bottom: 2rem;
        }
        .section-header {
            font-size: 1.5rem;
            font-weight: 600;
            color: #111827;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

# --- UI Components ---
def render_header():
    st.markdown('<p class="main-header">AI Resume Evaluator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Analyze candidate-job compatibility using LLM-powered resume intelligence</p>', unsafe_allow_html=True)
    st.divider()

def render_jd_section():
    st.markdown('<p class="section-header">Job Description</p>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Job Description Input",
        height=250,
        placeholder="Paste the full Job Description here...\n\nExample:\nWe are looking for a Senior Software Engineer with 5+ years of experience in Python, AWS, and React...",
        label_visibility="collapsed"
    )
    if job_description:
        st.caption(f"Character count: {len(job_description)}")
    return job_description

def render_upload_section():
    st.markdown('<p class="section-header">Candidate Resume</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
        help="Drag and drop your file here. Only PDF and DOCX formats are supported.",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        file_size_kb = len(uploaded_file.getvalue()) / 1024
        st.success(f"**{uploaded_file.name}** uploaded successfully ({file_size_kb:.1f} KB - {uploaded_file.type})")
        
    return uploaded_file

def display_results(result, job_info, resume_info):
    st.divider()
    st.markdown('<p class="main-header" style="font-size: 2rem;">Evaluation Results Dashboard</p>', unsafe_allow_html=True)
    
    details = result.details
    score = float(result.score)
    
    # Try to extract common keys intelligently based on the LLM prompt in resume_parser.py
    candidate_name = resume_info.name if resume_info.name else details.get("Candidate name", details.get("candidate_name", "Not found in resume"))
    role_evaluated = job_info.role if job_info.role else "Specified Role"
    verdict = details.get("A short final verdict", details.get("final_verdict", details.get("verdict", "N/A")))
    matching_skills = details.get("Matching skills", details.get("matching_skills", []))
    missing_skills = details.get("Missing important skills", details.get("missing_skills", []))
    exp_met = details.get("Whether experience requirement is met", details.get("experience_requirement_met", details.get("experience_met", "N/A")))
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Overall Match Score")
        st.metric(label="Match Percentage", value=f"{score}%")
        st.progress(int(score) / 100)
    
    with col2:
        st.markdown("### Candidate Information")
        st.markdown(f"**Name:** {candidate_name}")
        st.markdown(f"**Role Evaluated For:** {role_evaluated}")
        st.markdown(f"**Overall Verdict:** {verdict}")

    st.markdown("---")
    
    st.markdown("### Skills Analysis")
    skills_col1, skills_col2 = st.columns(2)
    
    with skills_col1:
        st.success("✅ **Matching Skills**")
        if isinstance(matching_skills, list) and matching_skills:
            for skill in matching_skills:
                st.markdown(f"- {skill}")
        elif isinstance(matching_skills, str):
            st.write(matching_skills)
        else:
            st.write("None identified")
            
    with skills_col2:
        st.error("❌ **Missing Skills**")
        if isinstance(missing_skills, list) and missing_skills:
            for skill in missing_skills:
                st.markdown(f"- {skill}")
        elif isinstance(missing_skills, str):
            st.write(missing_skills)
        else:
            st.write("None identified")

    st.markdown("---")
    
    st.markdown("### Evaluation Details")
    with st.expander("View Detailed Breakdown", expanded=True):
        st.markdown(f"**Experience Match:** {exp_met}")
        
        # Displaying remaining keys that might act as Strengths/Weaknesses or just additional details
        known_keys = [
            "Candidate name", "candidate_name", 
            "Matching skills", "matching_skills",
            "Missing important skills", "missing_skills",
            "Whether experience requirement is met", "experience_requirement_met", "experience_met",
            "Overall match percentage from 0 to 100", "overall_match_percentage",
            "A short final verdict", "final_verdict", "verdict"
        ]
        
        other_details = {k: v for k, v in details.items() if k not in known_keys}
        if other_details:
            for k, v in other_details.items():
                formatted_key = str(k).replace('_', ' ').title()
                if isinstance(v, list):
                    st.markdown(f"**{formatted_key}:**")
                    for item in v:
                        st.markdown(f"- {item}")
                else:
                    st.markdown(f"**{formatted_key}:** {v}")

def main():
    load_css()
    render_header()
    
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        job_description = render_jd_section()
        
    with col_right:
        uploaded_file = render_upload_section()

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        evaluate_clicked = st.button("🚀 Analyze Resume", use_container_width=True, type="primary")

    if evaluate_clicked:
        if not job_description or not job_description.strip():
            st.error("❌ Please provide a Job Description before analyzing.")
        elif not uploaded_file:
            st.error("❌ Please upload a Candidate Resume before analyzing.")
        else:
            with st.spinner("Analyzing candidate compatibility... This may take a moment."):
                try:
                    temp_path = Path(uploaded_file.name)
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("Parsing Job Description...")
                    job = parse_job_description(job_description)
                    progress_bar.progress(30)
                    
                    status_text.text("Reading and Parsing Resume...")
                    resume_text = resume_reader(temp_path)
                    resume = resume_parser(resume_text)
                    progress_bar.progress(60)
                    
                    status_text.text("Calculating Match Score...")
                    result = score_calc(job, resume)
                    progress_bar.progress(100)
                    
                    status_text.empty()
                    progress_bar.empty()
                    
                    display_results(result, job, resume)
                    
                    if temp_path.exists():
                        os.remove(temp_path)
                        
                except Exception as e:
                    st.error(f"An error occurred during evaluation: {str(e)}")

if __name__ == "__main__":
    main()