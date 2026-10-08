import streamlit as st
import matplotlib.pyplot as plt
from main import LearningPathGenerator

st.set_page_config(page_title="AI Learning Path Generator", layout="wide")
st.title("AI Learning Path Generator")
st.write("Personalized learning paths using prerequisites and Q-learning.")
gen=LearningPathGenerator(); gen.train_q_learning()
sid=st.selectbox("Choose a student", gen.students["student_id"].tolist())
result=gen.generate_path(sid); s=result["student"]
c1,c2,c3=st.columns(3); c1.metric("Skill Level",s["current_skill_level"]); c2.metric("Steps",result["total_steps"]); c3.metric("Hours",result["estimated_hours"])
rows=[{"Step":i,"Topic":x["title"],"Category":x["category"],"Difficulty":x["difficulty"],"Hours":x["duration_hours"]} for i,x in enumerate(result["path"],1)]
st.dataframe(rows,use_container_width=True)
st.subheader("Path Visualization")
fig,ax=plt.subplots(figsize=(10,4)); vals=[x["difficulty"] for x in result["path"]]; labels=[x["title"] for x in result["path"]]; ax.plot(range(1,len(vals)+1),vals,marker="o"); ax.set_xticks(range(1,len(vals)+1)); ax.set_xticklabels(labels,rotation=55,ha="right",fontsize=8); ax.set_ylabel("Difficulty (1-3)"); ax.set_xlabel("Learning Step"); ax.set_title("Adaptive Learning Path"); fig.tight_layout(); st.pyplot(fig)
st.subheader("Recommendations")
for r in gen.recommendations(result): st.write("•",r)
