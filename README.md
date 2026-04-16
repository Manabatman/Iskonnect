ISKONNECT – Scholarship Matcher Philippines

A policy-aware scholarship matching platform that helps Filipino students discover scholarships they are eligible for.

The system evaluates student profiles against scholarship requirements using eligibility filters, Philippine policy thresholds, and structured scoring logic. It aims to reduce the time students spend searching across scattered scholarship listings.

This project is currently being developed as an early prototype.

**Deploy (Vercel + Render + Supabase):** see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md). The repo includes `.python-version` (3.11.x) so Render does not default to Python 3.14.

Overview

Many Filipino students struggle to find scholarships because information is fragmented across different websites and institutions.

ISKONNECT attempts to solve this by:

Collecting scholarship opportunities into a structured database
Allowing students to create a detailed academic and socioeconomic profile
Automatically matching students with scholarships they qualify for
Explaining why each scholarship appears as a match
The system integrates several Philippine policy references and standardized academic classifications to improve matching accuracy.

Core Features
Student Profile System
Students create a structured profile through a guided multi-step form covering:
Personal information
Academic background
Geographic location

Merit indicators
Socioeconomic background
Policy-Aware Eligibility Matching
The platform incorporates eligibility thresholds commonly used by Philippine scholarship programs, including:
Income bracket limits
Academic grade requirements
Geographic or regional restrictions
Education level eligibility

Several policy frameworks referenced include:

RA 7277 – Magna Carta for Persons with Disabilities
RA 7279 – Urban Development and Housing Act
RA 8371 – Indigenous Peoples Rights Act
RA 11861 – Expanded Solo Parents Welfare Act

These help identify priority groups often recognized in scholarship programs.

Hard Eligibility Filters

Before scoring occurs, impossible matches are removed using strict filters such as:
Age requirements
Education level
Income ceilings
Grade thresholds
Regional restrictions

This ensures the scoring system only evaluates realistic scholarship options.

Modular Scoring Engine
The ranking system is designed to be replaceable.
A default rule-based scorer is included, but new scoring algorithms can be plugged into the system without modifying the rest of the application.
This allows experimentation with different matching approaches.

Match Explanation

Each scholarship match includes a breakdown explaining why the student matched, such as:
Academic requirement satisfied
Income eligibility met (for need-sensitive programs)
Location and field alignment
Priority group alignment when applicable
Document readiness is tracked separately for applications and is not part of the eligibility fit score.
This transparency helps students understand how to improve their eligibility.
Document Readiness Tracking
The system compares required scholarship documents with documents already available to the student.

Examples include:
Transcript of records
Certificate of indigency
Proof of enrollment
Recommendation letters
Students can quickly see what they still need before applying.
PSCED Field-of-Study Matching
Courses are categorized using the Philippine Standard Classification of Education (PSCED) taxonomy.

This improves matching accuracy between:
Student degree programs
Scholarship field-of-study requirements

Technology Stack
Backend
Python

FastAPI
SQLAlchemy
SQLite

Frontend
React
TypeScript
Vite
Tailwind CSS

Quick Start
1. Clone the repository
git clone https://github.com/your-repo/scholarship-match.git
cd scholarship-match
2. Backend Setup

Install dependencies:

pip install -r requirements.txt

Copy `.env.example` to `.env` in the project root. For **local development**, keep `AUTH_DISABLED=true` and `RUN_MIGRATIONS_ON_STARTUP=true` so you can use the app without logging in and migrations apply on server start. For **production**, set `AUTH_DISABLED=false`, a strong `SECRET_KEY`, and run migrations via your host’s release command (see `docs/DEPLOYMENT.md`).

Run database migrations (if not using startup migrations):

alembic upgrade head

Seed the database with scholarship data:

python seed_data.py

Run the backend server:

uvicorn app.main:app --reload --port 8000

Backend will run at:

http://localhost:8000

API documentation:

http://localhost:8000/docs
3. Frontend Setup

Navigate to the frontend directory:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

Frontend will run at:

http://localhost:5173
Running Both Services

You can either:

Run backend and frontend in separate terminals

Use the included script:

START_BOTH.bat

(Windows only)

API Endpoints
Method	Endpoint	Description
GET	/health	Health check
GET	/api/v1/profiles	List student profiles
POST	/api/v1/profiles	Create or update a profile
GET	/api/v1/profiles/{id}	Retrieve a profile
GET	/api/v1/scholarships	List scholarships
POST	/api/v1/scholarships	Add a scholarship
GET	/api/v1/matches/{profile_id}	Get ranked scholarship matches
