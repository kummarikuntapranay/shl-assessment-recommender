import streamlit as st
import requests

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 SHL Assessment Recommendation Web App")
st.markdown(
    "Enter a job description or hiring query to receive relevant **SHL Individual Test Solutions**."
)

# -----------------------------
# Input box
# -----------------------------
query = st.text_area(
    "Job Description / Query",
    height=220,
    placeholder="Example: I am hiring Java developers who can collaborate with business teams..."
)

# -----------------------------
# Button
# -----------------------------
if st.button("Recommend Assessments"):
    if not query.strip():
        st.warning("Please enter a job description or query.")
    else:
        with st.spinner("Running recommendation pipeline..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/recommend",
                    json={"query": query},
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()["recommendations"]

                    if not data:
                        st.info("No recommendations found.")
                    else:
                        st.success(f"Found {len(data)} relevant assessments")

                        st.table([
                            {
                                "Assessment Name": r["assessment_name"],
                                "Assessment URL": r["assessment_url"]
                            }
                            for r in data
                        ])
                else:
                    st.error("Backend API error. Make sure the API is running.")

            except Exception as e:
                st.error(f"Could not connect to API: {e}")
