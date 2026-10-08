# AI Learning Path Generator — AI-SS-013

This project implements Internship Task 1: AI Learning Path Generator using Python, Q-learning, Pandas and NumPy.

## Features
- Student profiling
- Learning content management with 16 modules
- Prerequisite mapping
- Q-learning based path optimization
- Adaptive difficulty
- Personalized recommendations
- Path visualization through an optional Streamlit dashboard

## Structure
```text
AI_Learning_Path_Generator/
├── main.py
├── app.py
├── requirements.txt
├── README.md
├── project_report.md
├── path_output.txt
├── data/
│   ├── learning_content.json
│   └── student_profiles.csv
└── docs/
    └── submission_notes.md
```

## Run
```powershell
pip install -r requirements.txt
python main.py
```
Optional dashboard:
```powershell
streamlit run app.py
```

## Q-learning in simple terms
**State:** current learning module.  
**Action:** possible next module.  
**Reward:** higher value for career relevance, suitable difficulty and progression.  
**Q-table:** stores learned values for state-action pairs.  
**Prerequisites:** stop a module from being selected before required modules are completed.

## Sample students
The CSV contains four sample profiles created for demonstrating personalization. No external dataset is required.

## Before publishing
Add the exact Task 1 URL supplied by the internship portal to this README if required by your submission instructions.

## Submission checklist
- Public GitHub repository
- README with task link and setup
- Proper commits
- Demo video / YouTube link
- 5+ screenshots
- 1–2 page report
- Blog submission with GitHub and YouTube links
