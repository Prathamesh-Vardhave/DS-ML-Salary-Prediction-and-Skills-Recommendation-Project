import joblib
import os
from collections import Counter

BASE_PATH = os.path.join("..", "Model")

df_rec = joblib.load(os.path.join(BASE_PATH, "recommendation_data.pkl"))

def recommend_skills(job_role, exp_bucket, user_skills, top_n=10):

    user_skills = [s.strip().lower() for s in user_skills]

    # Filter by role + experience bucket
    filtered = df_rec[
        (df_rec["Job_Role"] == job_role) &
        (df_rec["exp_bucket"] == exp_bucket)
    ]

    all_skills = []

    for skills in filtered["skills"]:
        skill_list = [s.strip().lower() for s in skills.split(",")]
        all_skills.extend(skill_list)

    skill_counts = Counter(all_skills)

    # Remove already known skills
    for skill in user_skills:
        skill_counts.pop(skill, None)

    # Return top skills only
    recommended = [skill for skill, _ in skill_counts.most_common(top_n)]

    return recommended