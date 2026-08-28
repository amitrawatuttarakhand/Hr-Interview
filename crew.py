import os
import streamlit as st
from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv
from pypdf import PdfReader
from streamlit.typing import UploadedFile

# Load local environment variables (.env)
load_dotenv()

def build_crew() -> Crew:
    """Create a fresh crew using Groq's fast open-source Llama model."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set. Add it to your .env file or sidebar.")

    # UPDATED Configured to use the current Llama 3.3 70B model via Groq API
    llm = LLM(
        model="groq/llama-3.3-70b-versatile", 
        api_key=api_key, 
        temperature=0.2
    )

    resume_screener = Agent(
        role="Senior HR Resume Screener",
        goal="Identify candidate skill alignments and gaps against a job description.",
        backstory="You are an expert technical recruiter with 10+ years of experience.",
        llm=llm,
        verbose=False,
    )
    
    interview_strategist = Agent(
        role="Technical Interview Strategist",
        goal="Generate focused technical interview questions from screening results.",
        backstory="You are a principal engineer who designs rigorous interview loops.",
        llm=llm,
        verbose=False,
    )

    screening_task = Task(
        description=(
            "Review this candidate resume:\n{resume}\n\nCompare it to this job description:\n"
            "{job_description}\n\nList matching skills, missing skills, relevant experience, "
            "and a hiring recommendation."
        ),
        expected_output="A concise screening report with skills, gaps, experience, and recommendation.",
        agent=resume_screener,
    )
    
    interview_task = Task(
        description=(
            "Using the screening report above, create 8 technical interview questions. "
            "For each, state the skill assessed and what a strong answer demonstrates."
        ),
        expected_output="Eight targeted interview questions with evaluation criteria.",
        agent=interview_strategist,
    )

    return Crew(
        agents=[resume_screener, interview_strategist],
        tasks=[screening_task, interview_task],
        process=Process.sequential,
        verbose=False,
    )


def extract_resume_text(uploaded_pdf: UploadedFile) -> str:
    """Extract readable text from an uploaded resume PDF."""
    reader = PdfReader(uploaded_pdf)
    return "\n".join(page.extract_text() or "" for page in reader.pages).strip()


def main() -> None:
    st.set_page_config(
        page_title="HR Sourcing Crew",
        page_icon="🤖",
        layout="wide",
    )
    st.title("🤖 HR Sourcing Crew")
    st.write("Screen a resume against a job description and generate interview questions instantly using free Llama 3.3 cloud intelligence.")

    # Dynamic fallback: Let user provide API key in sidebar if .env is missing
    with st.sidebar:
        st.header("🔑 Authentication")
        user_key = st.text_input("Groq API Key", type="password", value=os.getenv("GROQ_API_KEY", ""))
        if user_key:
            os.environ["GROQ_API_KEY"] = user_key

    with st.form("candidate_analysis", border=False):
        resume_column, job_column = st.columns(2)

        with resume_column:
            resume_pdf = st.file_uploader(
                "Candidate resume (PDF)",
                type="pdf",
                help="Upload a text-based PDF resume, up to 10 MB.",
            )

        with job_column:
            job_description_text = st.text_area(
                "Job description",
                height=360,
                placeholder="Paste the job description here...",
            )

        submitted = st.form_submit_button(
            "Analyze candidate",
            type="primary",
        )

    if submitted:
        if resume_pdf is None or not job_description_text.strip():
            st.warning("Upload a candidate resume PDF and enter a job description.")
            return

        try:
            resume_text = extract_resume_text(resume_pdf)

            if not resume_text:
                st.warning(
                    "No readable text was found in the PDF. "
                    "Upload a text-based resume PDF."
                )
                return

            with st.spinner("The HR crew is reviewing the candidate..."):
                result = build_crew().kickoff(
                    inputs={
                        "resume": resume_text,
                        "job_description": job_description_text,
                    }
                )

            st.subheader("Analysis Results")
            st.markdown(str(result))

        except (RuntimeError, ValueError) as error:
            st.error(str(error))

        except Exception as e:
            st.error(
                f"The analysis could not be completed. Error details: {e}. "
                "Check your API key and network connection."
            )


if __name__ == "__main__":
    main()
