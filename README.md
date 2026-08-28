# 🤖 HR Sourcing Crew

An AI-powered Streamlit application that automates candidate resume screening against job descriptions and generates targeted technical interview questions using **CrewAI** and **Groq**.

---

## 🌟 Key Features

* **PDF Resume Extraction**: Upload any text-based candidate resume (up to 10 MB).
* **Automated Screening**: Compares skill sets, identifies missing qualifications, and evaluates candidate experience against a job description.
* **Interview Question Generator**: Generates targeted technical interview questions complete with evaluation criteria for strong responses.
* **Fast & Free Inference**: Powered by high-speed open-source models via Groq Cloud without requiring heavy external dependencies like `litellm`.

---

## 🛠️ Architecture

The app coordinates two specialized CrewAI agents sequentially:

1. **Senior HR Resume Screener**: Evaluates the candidate's resume, identifies alignment/gaps, and provides a hiring recommendation.
2. **Technical Interview Strategist**: Takes the screening output to design technical interview questions and scoring criteria.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10 to 3.12 installed.
* A free **Groq API Key** (Get one at [Groq Console](https://console.groq.com/)).

### Local Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/hr-sourcing-crew.git](https://github.com/your-username/hr-sourcing-crew.git)
   cd hr-sourcing-crew
