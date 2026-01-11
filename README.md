# Project Advisor (Flask + Gemini) — Document-to-Project Analysis & UML Generator

Project Advisor is a Flask-based web application that analyzes software-related documents (PDF/DOCX/TXT) and automatically generates:
- A clear **Project Overview**
- **Business / Functional / Non-Functional / Technical Requirements**
- Implementation-focused **Analysis** (feasibility, complexity, impact, approach)
- **UML diagrams** (Class, Use Case, Activity, Sequence) rendered visually
- A downloadable **Project Analysis Report (PDF)**

It’s designed to help students, junior developers, and teams quickly transform written requirements into structured engineering outputs.

---

##  Features

###  Document Analysis
- Upload documents (e.g., project descriptions, requirements, specs)
- Extracts text from:
  - `.pdf`
  - `.docx`
  - `.txt`

###  Requirements Extraction
Generates organized requirements like:
- Business Requirements
- Functional Requirements
- Non-Functional Requirements
- Technical Requirements

###  Engineering Analysis
Creates practical, implementation-oriented analysis sections such as:
- Functional Analysis (feasibility, complexity, impact, approach)
- Technical Analysis
- Impact Analysis (cross-requirement/system-wide implications)

###  UML Diagrams (Auto-Generated)
Generates UML diagrams (rendered visually in the UI):
- Class Diagram
- Use Case Diagram
- Activity Diagram
- Sequence Diagram

> Diagrams are provided in Mermaid format and rendered on the frontend.

###  Workspaces & Saved Analyses
- “New Project” workflow
- Saved analyses list on the left panel
- Re-open previous analyses by timestamp/file

###  PDF Report Export
- Produces a readable PDF report containing:
  - Overview
  - Requirements
  - Analysis
  - Diagrams section
- PDF can be viewed in-app and downloaded.

---

##  Tech Stack

- **Backend:** Python, Flask
- **AI:** Google Gemini (Generative AI)
- **Frontend:** HTML/CSS (Flask templates)
- **Diagram rendering:** Mermaid (frontend rendering)
- **PDF export:** ReportLab
- **Storage:** Local workspace storage (folders + optional lightweight DB)

