# Project Report — AI Learning Path Generator (AI-SS-013)

## 1. Problem Statement
Students have different career goals, current skill levels and learning requirements. A fixed sequence is not ideal for every student. This project generates personalized learning paths using student profiles, prerequisite relationships, difficulty and career goals.

## 2. Objectives
The system generates an optimized path using reinforcement learning, personalizes the sequence, respects prerequisites, adapts difficulty and provides recommendations and visualization.

## 3. Methodology
Sixteen learning modules are stored in `learning_content.json` with title, category, difficulty, duration and prerequisites. Four sample student profiles are stored in `student_profiles.csv`.

Q-learning uses the following model:
- State: current learning module.
- Action: candidate next module.
- Reward: relevance to the career goal, appropriate difficulty and valid progression.
- Learning rate: 0.10.
- Discount factor: 0.90.
- Initial epsilon: 0.10.

Before an action is selected, its prerequisites must be completed. The learned Q-values and student skill level are then used to select the next suitable topic.

## 4. Personalization
The demonstration includes AI Engineer/Beginner, Data Scientist/Intermediate, ML Engineer/Advanced and Full Stack AI/Beginner profiles. Completed topics and skill levels differ, allowing different paths and recommendations.

## 5. Results
The program trains a Q-learning model and prints personalized paths containing topic, category, difficulty, duration and prerequisites. The optional Streamlit dashboard shows the selected path in a table and visualizes difficulty across the sequence.

## 6. Conclusion
The project demonstrates reinforcement learning for personalized educational planning with a simple implementation that can be understood and extended by a beginner.

## 7. Future Enhancements
Real-time adjustment after progress updates, gamification, multi-domain paths, richer analytics and email reports can be added later.
