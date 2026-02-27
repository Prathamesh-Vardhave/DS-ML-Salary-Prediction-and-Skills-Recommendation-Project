import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px


# Page Config
st.set_page_config(
    page_title="Salary & Skill Recommendation",
    page_icon="🚀",
    layout="wide"
)


# Dark Modern Styling
st.markdown("""
<style>
body {
    background-color: #0E1117;
}
.card {
    background-color: #1E1E2F;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}
.big-font {
    font-size: 28px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Salary Prediction & Intelligence Skill Recommendation System")

st.markdown("### Enter Your Profile")

# -------------------------
# Dropdown Options
# -------------------------
job_roles = [
 'Business Analyst',
 'Data Analyst',
 'Data Architect',
 'Data Engineer',
 'Data Scientist',
 'Machine Learning Engineer',
 'Senior Business Analyst',
 'Senior Data Analyst',
 'Senior Data Engineer',
 'Senior Data Scientist'
]

cities = [
    'Ahmedabad',
 'Ambah',
 'Bengaluru',
 'Bharuch',
 'Bhiwadi',
 'Bhopal',
 'Chandigarh',
 'Chennai',
 'Coimbatore',
 'Erode',
 'Faridabad',
 'Gandhinagar',
 'Ghaziabad',
 'Gurugram',
 'Guwahati', 'Hosur',
 'Hyderabad',
 'Indore', 'Jaipur',
 'Kalyani',
 'Kochi',
 'Kolkata',
 'Kota',
 'Kozhikode',
 'Lucknow',
 'Madurai',
 'Mangalore',
 'Mohali',
 'Mumbai',
 'Mumbai Suburban',
 'Muzaffarpur',
 'Nagpur',
 'Navi Mumbai',
 'New Delhi',
 'Noida',
 'Palani',
 'Panaji',
 'Panchkula',
 'Pune',
 'Rajkot',
 'Remote',
 'Salem',
 'Serilingampally',
 'Surat',
 'Thane',
 'Thiruvananthapuram',
 'Vadodara',
 'Vijayawada',
 'Visakhapatnam'
]

skills_list = [
    'agile', 'airflow', 'ansible', 'aws', 'azure', 'bash', 'bigquery', 'c#', 'c++', 'cassandra', 'ci/cd', 'communication', 'computer vision', 'databricks', 'deep learning', 'docker', 'ec2', 'elt', 'etl', 'excel', 'gcp', 'git', 'hadoop', 'java', 'javascript', 'jenkins', 'kafka', 'keras', 'kubernetes', 'lambda', 'leadership', 'looker', 'machine learning', 'management', 'mongodb', 'mysql', 'nlp', 'nosql', 'oracle', 'pipeline', 'postgresql', 'powerbi', 'project', 'python', 'pytorch', 'qlikview', 'r', 'redis', 's3', 'scala', 'scikit-learn', 'scrum', 'snowflake', 'spark', 'sql', 'ssis', 'ssrs', 'stakeholder', 'synapse', 'tableau', 'tensorflow', 'terraform', 'xgboost'
]


# Input Section
# -------------------------
with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_role = st.selectbox("Job Role", job_roles)

    with col2:
        selected_city = st.selectbox("Primary City", cities)

    with col3:
        experience = st.number_input("Years of Experience", min_value=0.0, max_value=40.0, step=0.5)

    selected_skills = st.multiselect("Select Your Skills", skills_list)

    predict_button = st.button("Analyze Profile 🚀")


# Prediction Section
# -------------------------
if predict_button:

    if not selected_skills:
        st.warning("Please select at least one skill.")
    else:
        payload = {
            "Job_Role": selected_role,
            "primary_city": selected_city,
            "experience": experience,
            "skills": selected_skills
        }

        with st.spinner("Analysis in progress..."):

            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                salary = result["predicted_salary"]
                recommended_skills = result["recommended_skills"]

                st.markdown("---")

                colA, colB = st.columns(2)

                
                # Salary Gauge
                # -------------------------
                with colA:
                    st.markdown("### 💰 Predicted Salary")

                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=salary,
                        number={'suffix': " LPA"},
                        gauge={
                            'axis': {'range': [0, 50]},
                            'bar': {'color': "#00BFFF"},
                            'steps': [
                                {'range': [0, 10], 'color': "#2E2E2E"},
                                {'range': [10, 25], 'color': "#3A3A5A"},
                                {'range': [25, 50], 'color': "#4B0082"}
                            ],
                        }
                    ))

                    fig.update_layout(
                        paper_bgcolor="#0E1117",
                        font={'color': "white"}
                    )

                    st.plotly_chart(fig, use_container_width=True)

                
                # Recommended Skills Card
                # -------------------------
                with colB:
                    st.markdown("### 📚 Recommended Skills")

                    st.markdown('<div class="card">', unsafe_allow_html=True)

                    for skill in recommended_skills:
                        st.markdown(f"✅ {skill}")

                    st.markdown('</div>', unsafe_allow_html=True)

                
                # Skill Importance Graph
                # -------------------------
                st.markdown("### 📈 Skill Importance")

                # Fake importance score (since XGBoost importance not passed yet)
                importance_scores = list(range(len(recommended_skills), 0, -1))

                fig2 = px.bar(
                    x=importance_scores,
                    y=recommended_skills,
                    orientation='h',
                    color=importance_scores,
                    color_continuous_scale='Blues'
                )

                fig2.update_layout(
                    paper_bgcolor="#0E1117",
                    plot_bgcolor="#0E1117",
                    font_color="white"
                )

                st.plotly_chart(fig2, use_container_width=True)

            else:
                st.error("Backend error. Check FastAPI.")