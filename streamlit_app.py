import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="AI Model Evaluation App", layout="wide")

# Sidebar Configuration
st.sidebar.title("AI Value Assessment")
menu = ["Overview", "AI Model Input", "Evaluation", "Feedback"]
choice = st.sidebar.radio("Navigate", menu)

# KPI List (Pre-embedded)
kpi_data = [
    {"Business Objective": "New Sources of Value Creation", "KPI Category": "Digital Channels", "KPI Focus": "Revenues & Profit", "KPI Metrics": "Orders, Revenue, Customer Traffic, Transactions, Social Orders"},
    {"Business Objective": "New Sources of Value Creation", "KPI Category": "Digital Ecosystem", "KPI Focus": "Revenues & Profit", "KPI Metrics": "Partners & Networks, Referrals & Profit"},
    {"Business Objective": "New Sources of Value Creation", "KPI Category": "Physical Integration", "KPI Focus": "Revenues & Profit", "KPI Metrics": "Digital Products, Pricing, Promotion, New Business Models"},
    {"Business Objective": "Customer Engagement", "KPI Category": "Customer Time Saved", "KPI Focus": "Time Saved", "KPI Metrics": "Hours Saved, Time to Fulfill, Per Request"},
    {"Business Objective": "Operational Efficiency", "KPI Category": "Speed on Response, Delivery", "KPI Focus": "Time & Compliance", "KPI Metrics": "Reduction of Delivery Time, % Compliance, Lead Time, Work Done"},
    {"Business Objective": "Workforce Engagement", "KPI Category": "Diversity, Equity & Inclusion", "KPI Focus": "Performance & Inclusion", "KPI Metrics": "DEI Index %, Training Hours, Improved %"},
    {"Business Objective": "Workforce Engagement", "KPI Category": "Talent Management", "KPI Focus": "Performance & Retention", "KPI Metrics": "Productivity & Efficiency, Talent Retention %, Turnover %"}
]

# Likert Scale Questions (Agree/Disagree)
likert_questions = [
    "The AI model effectively achieves the intended business objective.",
    "The KPIs identified are appropriate for measuring the AI model's performance.",
    "The suggested KQIs provide valuable insights into the quality of the AI model.",
    "The KRIs help mitigate risks associated with the AI application.",
    "The AI model aligns with compliance and regulatory requirements (e.g., AI Act).",
    "The AI application improves operational efficiency as measured by relevant KPIs.",
    "Customer engagement is enhanced due to the AI model implementation.",
    "The AI model positively impacts workforce productivity and talent management.",
    "The AI model supports sustainability objectives effectively.",
    "The AI-generated recommendations are actionable and relevant to the business goals."
]

# Function to load KPI data
def load_kpi_data(uploaded_file=None):
    """
    Load KPI/KQI/KRI data into a pandas DataFrame.
    If a file is uploaded, load from the file; otherwise, use pre-embedded data.
    """
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("Uploaded KPI/KQI/KRI data loaded successfully.")
            return df
        except Exception as e:
            st.error(f"Error loading uploaded file: {e}")
            return pd.DataFrame(kpi_data)
    else:
        return pd.DataFrame(kpi_data)

# Overview Page
if choice == "Overview":
    st.title("AI Model Evaluation App")
    st.write("### Assess the value of your AI models, use cases, or applications by evaluating relevant KPIs, KQIs, and KRIs.")
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)
    st.markdown("""
    **Features:**
    - **Structured Evaluation**: Answer comprehensive questions to assess your AI model.
    - **Interactive Dashboard**: Visualize your KPIs with dynamic charts and tables.
    - **Feedback System**: Provide feedback to help improve the evaluation process.
    
    **How to Use:**
    1. Navigate to the **AI Model Input** section to describe your AI application.
    2. Proceed to the **Evaluation** section to answer evaluation questions.
    3. View and analyze the results in the **Evaluation** section.
    4. Provide feedback in the **Feedback** section to help refine the system.
    """)

# AI Model Input Page
elif choice == "AI Model Input":
    st.header("Describe Your AI Model/Application")
    st.write("Provide detailed information about your AI model to evaluate its value effectively.")
    
    with st.form(key='ai_model_form'):
        ai_name = st.text_input("AI Model/Application Name", "e.g., Customer Churn Prediction")
        ai_description = st.text_area("AI Model/Application Description", 
                                       "Describe the purpose, target domain, risk factors, and operational context of your AI model...", 
                                       height=200)
        uploaded_file = st.file_uploader("Upload KPI/KQI/KRI Data (Optional)", type=["csv"])
        submit_button = st.form_submit_button(label='Save Description')
    
    if submit_button:
        if ai_name and ai_description:
            st.session_state['ai_name'] = ai_name
            st.session_state['ai_description'] = ai_description
            st.session_state['kpi_data'] = load_kpi_data(uploaded_file)
            st.success("AI Model/Application details saved successfully!")
        else:
            st.error("Please provide both the AI Model/Application Name and Description.")

# Evaluation Page
elif choice == "Evaluation":
    st.header("Evaluate Your AI Model/Application")
    
    if 'ai_name' not in st.session_state or 'ai_description' not in st.session_state:
        st.warning("Please provide details about your AI model/application in the 'AI Model Input' section first.")
    else:
        st.subheader(f"AI Model/Application: {st.session_state['ai_name']}")
        st.write(f"**Description:** {st.session_state['ai_description']}")
        
        st.markdown("### Evaluation Questionnaire")
        with st.form(key='evaluation_form'):
            st.write("Please answer the following questions to evaluate your AI model/application.")
            responses = {}
            for question in likert_questions:
                responses[question] = st.slider(question, 1, 5, 3)
            submit_evaluation = st.form_submit_button(label='Submit Evaluation')
        
        if submit_evaluation:
            st.session_state['evaluation'] = responses
            st.success("Evaluation submitted successfully!")
            
            # Display Evaluation Summary
            st.markdown("### Evaluation Summary")
            eval_df = pd.DataFrame.from_dict(responses, orient='index', columns=['Rating'])
            eval_df.index.name = 'Question'
            eval_df.reset_index(inplace=True)
            st.table(eval_df)
            
            # Visualize Ratings
            fig = px.bar(eval_df, x='Question', y='Rating', title="Evaluation Ratings", 
                         labels={'Rating': 'Score (1-5)'}, 
                         range_y=[0,5], 
                         height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Suggest Relevant KPIs/KQIs/KRIs based on high ratings
            st.markdown("### Suggested KPIs/KQIs/KRIs")
            kpi_df = st.session_state['kpi_data']
            st.dataframe(kpi_df)
            
            # Visualize KPIs
            st.markdown("#### KPIs Visualization")
            fig_kpi = px.bar(kpi_df, x='KPI Focus', y='KPI Metrics', title="KPIs Visualization")
            st.plotly_chart(fig_kpi, use_container_width=True)

# Feedback Page
elif choice == "Feedback":
    st.header("Provide Your Feedback")
    st.write("Help us improve by rating your experience with the AI Model Evaluation App.")
    
    if 'evaluation' not in st.session_state:
        st.warning("Please complete an evaluation in the 'Evaluation' section first.")
    else:
        with st.form(key='feedback_form'):
            st.subheader("Rate the App Experience")
            feedback_scores = {}
            feedback_questions = [
                "The app interface is user-friendly.",
                "The evaluation process was clear and comprehensive.",
                "The KPIs/KQIs/KRIs suggestions are relevant.",
                "The visualizations effectively represent the data.",
                "Overall, I am satisfied with the app."
            ]
            for question in feedback_questions:
                feedback_scores[question] = st.slider(question, 1, 5, 3)
            
            st.subheader("Additional Comments")
            comments = st.text_area("Your Comments", height=100)
            
            submit_feedback = st.form_submit_button(label='Submit Feedback')
        
        if submit_feedback:
            st.success("Thank you for your feedback!")
            st.write("**Your Ratings:**")
            feedback_df = pd.DataFrame.from_dict(feedback_scores, orient='index', columns=['Rating'])
            st.table(feedback_df)
            st.write("**Your Comments:**")
            st.write(comments)

# Footer
st.markdown("""
---
**Built with Streamlit and Python**  
[Streamlit](https://streamlit.io/) | [Python](https://www.python.org/)
""")
