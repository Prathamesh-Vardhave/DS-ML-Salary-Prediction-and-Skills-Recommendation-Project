import pandas as pd
import joblib
import os

# Load lookup tables
BASE_PATH = os.path.join("..", "Model")

job_role_map = joblib.load(os.path.join(BASE_PATH, "job_role_map.pkl"))
city_salary_map = joblib.load(os.path.join(BASE_PATH, "city_salary_map.pkl"))
city_group_map = joblib.load(os.path.join(BASE_PATH, "city_group_map.pkl"))

def process_user_input(user_data):

    skills = [s.strip().lower() for s in user_data["skills"]]
    experience = user_data["experience"]

    # ---------------- Basic ----------------
    num_skills = len(skills)
    has_experience = 1 if experience > 0 else 0
    exp_x_skills = experience * num_skills

    # ---------------- Experience Level ----------------
    if experience < 2:
        exp_level = "Junior"
        exp_level_num = 0
        exp_bucket = 0
    elif experience < 5:
        exp_level = "Mid"
        exp_level_num = 1
        exp_bucket = 1
    else:
        exp_level = "Senior"
        exp_level_num = 2
        exp_bucket = 2

    is_senior_role = 1 if experience >= 5 else 0

    # ---------------- Binary Skill Features ----------------
    skill_python = 1 if "python" in skills else 0
    skill_machine_learning = 1 if "machine learning" in skills else 0
    skill_deep_learning = 1 if "deep learning" in skills else 0
    skill_aws = 1 if "aws" in skills else 0
    skill_spark = 1 if "spark" in skills else 0
    skill_sql = 1 if "sql" in skills else 0

    # ---------------- Skill Groups (basic version) ----------------
    num_prog_langs = skill_python
    num_ml_skills = skill_machine_learning + skill_deep_learning
    num_cloud = skill_aws
    num_data_eng = skill_spark
    num_databases = skill_sql
    num_bi_tools = 0
    num_soft_skills = 0

    is_cloud_heavy = 1 if num_cloud >= 1 else 0
    is_ml_heavy = 1 if num_ml_skills >= 1 else 0

    skill_density = num_skills / (experience + 1)

    # ---------------- City Info ----------------
    primary_city = user_data["primary_city"]

    city_salary_index = city_salary_map.get(primary_city, 0)
    city_group = city_group_map.get(primary_city, "Unknown")

    is_multi_city = 0
    is_remote = 0

    # ---------------- Job Role Encoding ----------------
    job_role_encoded = job_role_map.get(user_data["Job_Role"], 0)

    # ---------------- Skill Set String ----------------
    skill_set = ", ".join(skills)

    # ---------------- Final DataFrame ----------------
    input_df = pd.DataFrame([{
        "Job_Role": user_data["Job_Role"],
        "primary_city": primary_city,
        "is_multi_city": is_multi_city,
        "is_remote": is_remote,
        "city_group": city_group,
        "num_skills": num_skills,
        "has_experience": has_experience,
        "skill_set": skill_set,
        "experience": experience,
        "exp_level": exp_level,
        "exp_level_num": exp_level_num,
        "skill_density": skill_density,
        "exp_x_skills": exp_x_skills,
        "job_role_encoded": job_role_encoded,
        "num_prog_langs": num_prog_langs,
        "num_ml_skills": num_ml_skills,
        "num_data_eng": num_data_eng,
        "num_cloud": num_cloud,
        "num_databases": num_databases,
        "num_bi_tools": num_bi_tools,
        "num_soft_skills": num_soft_skills,
        "skill_python": skill_python,
        "skill_machine_learning": skill_machine_learning,
        "skill_deep_learning": skill_deep_learning,
        "skill_aws": skill_aws,
        "skill_spark": skill_spark,
        "skill_sql": skill_sql,
        "city_salary_index": city_salary_index,
        "is_senior_role": is_senior_role,
        "is_cloud_heavy": is_cloud_heavy,
        "is_ml_heavy": is_ml_heavy,
        "exp_bucket": exp_bucket
    }])

    return input_df