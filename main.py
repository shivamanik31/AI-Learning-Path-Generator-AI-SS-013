"""AI Learning Path Generator - AI-SS-013"""
import json, random
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
CONTENT_FILE = BASE_DIR / "data" / "learning_content.json"
STUDENT_FILE = BASE_DIR / "data" / "student_profiles.csv"
SKILL_LEVEL = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}

class LearningPathGenerator:
    def __init__(self):
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            self.content = {x["id"]: x for x in json.load(f)}
        self.students = pd.read_csv(STUDENT_FILE)
        self.states = list(self.content.keys())
        self.q_table = pd.DataFrame(np.zeros((len(self.states), len(self.states))), index=self.states, columns=self.states)
        self.learning_rate, self.discount_factor, self.epsilon = 0.10, 0.90, 0.10

    def prerequisites_met(self, topic, completed):
        return all(p in completed for p in self.content[topic]["prerequisites"])

    def available_topics(self, completed):
        return [x for x in self.states if x not in completed and self.prerequisites_met(x, completed)]

    def reward(self, topic, student):
        item = self.content[topic]
        goal_categories = {
            "AI Engineer": ["Machine Learning","Deep Learning","Generative AI","MLOps","Project"],
            "Data Scientist": ["Data Science","Machine Learning","Project"],
            "ML Engineer": ["Machine Learning","Deep Learning","MLOps","Project"],
            "Full Stack AI": ["Programming","Generative AI","Project","MLOps"]}
        reward = 10.0
        if item["category"] in goal_categories.get(student["goal"], []): reward += 5.0
        target = SKILL_LEVEL.get(student["current_skill_level"], 1)
        reward += max(0, 3 - abs(item["difficulty"] - target))
        if item["difficulty"] <= target + 1: reward += 2.0
        return reward

    def train_q_learning(self, episodes=300):
        random.seed(42)
        for episode in range(episodes):
            student = self.students.iloc[episode % len(self.students)].to_dict()
            completed, state = set(), "python_basics"
            for _ in range(len(self.states) * 2):
                available = self.available_topics(completed)
                if not available: break
                if random.random() < self.epsilon:
                    action = random.choice(available)
                else:
                    action = self.q_table.loc[state, available].idxmax()
                r = self.reward(action, student)
                next_completed = completed | {action}
                next_available = self.available_topics(next_completed)
                next_max = self.q_table.loc[action, next_available].max() if next_available else 0
                old_q = self.q_table.loc[state, action]
                self.q_table.loc[state, action] = old_q + self.learning_rate * (r + self.discount_factor * next_max - old_q)
                completed.add(action); state = action
            self.epsilon = max(0.01, self.epsilon * 0.995)
        return self.epsilon

    def student(self, student_id):
        rows = self.students[self.students["student_id"] == student_id]
        return rows.iloc[0].to_dict() if not rows.empty else None

    def generate_path(self, student_id):
        student = self.student(student_id)
        if student is None: return None
        completed = set()
        if isinstance(student.get("completed_topics"), str) and student["completed_topics"].strip():
            completed.update(x.strip() for x in student["completed_topics"].split(";"))
        path, state = [], "python_basics"
        target = SKILL_LEVEL[student["current_skill_level"]]
        for _ in range(len(self.states)):
            available = self.available_topics(completed)
            if not available: break
            suitable = [x for x in available if self.content[x]["difficulty"] <= target + 1]
            if not suitable: suitable = available
            scores = {x: float(self.q_table.loc[state, x]) + 0.01*self.reward(x, student) for x in suitable}
            nxt = max(scores, key=scores.get)
            path.append(self.content[nxt]); completed.add(nxt); state = nxt
            if len(path) >= 10: break
        return {"student": student, "path": path, "total_steps": len(path), "estimated_hours": sum(x["duration_hours"] for x in path)}

    def recommendations(self, result):
        s = result["student"]
        recs = {"Beginner":["Build strong Python fundamentals before advanced AI topics."],"Intermediate":["Strengthen machine learning, statistics and project skills."],"Advanced":["Focus on advanced ML, deployment and challenging AI projects."]}[s["current_skill_level"]]
        goal = {"AI Engineer":"Prioritize model deployment, Generative AI and end-to-end applications.","Data Scientist":"Prioritize statistics, visualization and ML projects.","ML Engineer":"Prioritize advanced ML, deep learning, MLOps and deployment.","Full Stack AI":"Combine programming, AI concepts and end-to-end project development."}[s["goal"]]
        return recs + [goal, "Review completed topics regularly so the next path can adapt."]

def show(result, gen):
    s = result["student"]
    print("\n"+"="*65); print("AI LEARNING PATH GENERATOR"); print("="*65)
    print(f"Student: {s['name']} ({s['student_id']}) | Goal: {s['goal']} | Level: {s['current_skill_level']}")
    print(f"Steps: {result['total_steps']} | Estimated time: {result['estimated_hours']} hours\n")
    for i, x in enumerate(result["path"],1):
        print(f"{i}. {x['title']} | {x['category']} | Difficulty {x['difficulty']}/3 | {x['duration_hours']} hours")
    print("\nRecommendations:")
    for r in gen.recommendations(result): print(" -", r)

def main():
    gen = LearningPathGenerator()
    print("Training Q-Learning model...")
    eps = gen.train_q_learning()
    print(f"Training complete. Final epsilon: {eps:.3f}")
    outputs=[]
    for sid in gen.students["student_id"]:
        result=gen.generate_path(sid); show(result,gen)
        outputs.append(f"{sid}: " + " -> ".join(x["title"] for x in result["path"]))
    (BASE_DIR/"path_output.txt").write_text("\n".join(outputs),encoding="utf-8")
    print("\nSaved output to path_output.txt")

if __name__ == "__main__": main()
