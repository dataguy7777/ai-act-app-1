import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Model Evaluation App", layout="wide")

st.sidebar.title("AI Value Assessment")
menu = ["Overview", "AI Model Input", "Evaluation", "Results", "Feedback"]
choice = st.sidebar.radio("Navigate", menu)

kpi_data = [
    {"Business Objective": "New Sources of Value Creation", "KPI Category": "Digital Channels", "KPI Focus": "Revenues & Profit", "KPI Metrics": "Orders, Revenue, Customer Traffic, Transactions, Social Orders"},
    {"Business Objective": "New Sources of Value Creation", "KPI Category": "Digital Ecosystem", "KPI Focus": "Revenues & Profit", "KPI Metrics": "Partners & Networks, Referrals & Profit"},
    {"Business Objective": "New Sources of Value Creation", "KPI Category": "Physical Integration", "KPI Focus": "Revenues & Profit", "KPI Metrics": "Digital Products, Pricing, Promotion, New Business Models"},
    {"Business Objective": "Customer Engagement", "KPI Category": "Customer Time Saved", "KPI Focus": "Time Saved", "KPI Metrics": "Hours Saved, Time to Fulfill, Per Request"},
    {"Business Objective": "Operational Efficiency", "KPI Category": "Speed on Response, Delivery", "KPI Focus": "Time & Compliance", "KPI Metrics": "Reduction of Delivery Time, % Compliance, Lead Time, Work Done"},
    {"Business Objective": "Workforce Engagement", "KPI Category": "Diversity, Equity & Inclusion", "KPI Focus": "Performance & Inclusion", "KPI Metrics": "DEI Index %, Training Hours, Improved %"},
    {"Business Objective": "Workforce Engagement", "KPI Category": "Talent Management", "KPI Focus": "Performance & Retention", "KPI Metrics": "Productivity & Efficiency, Talent Retention %, Turnover %"}
]

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

additional_questions = [
    "Is the AI model tangible or intangible?",
    "Does the AI model result in cost reduction or cost increase?",
    "Does the AI model result in revenue increase or revenue reduction?"
]

def load_kpi_data(uploaded_file=None):
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("Uploaded KPI/KQI/KRI data loaded successfully.")
            return df
        except:
            return pd.DataFrame(kpi_data)
    else:
        return pd.DataFrame(kpi_data)

if choice == "Overview":
    st.title("AI Model Evaluation App")
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)
    st.markdown("""
    **Features:**
    - **Structured Evaluation**: Answer comprehensive questions to assess your AI model.
    - **Interactive Dashboard**: Visualize your KPIs with dynamic charts and tables.
    - **Feedback System**: Provide feedback to help improve the evaluation process.
    
    **How to Use:**
    1. Navigate to the **AI Model Input** section to describe your AI application.
    2. Proceed to the **Evaluation** section to answer evaluation questions.
    3. View and analyze the results in the **Results** section.
    4. Provide feedback in the **Feedback** section to help refine the system.
    """)

elif choice == "AI Model Input":
    st.header("Describe Your AI Model/Application")
    with st.form(key='ai_model_form'):
        ai_name = st.text_input("AI Model/Application Name", "e.g., Customer Churn Prediction")
        ai_description = st.text_area("AI Model/Application Description", "Describe the purpose, target domain, risk factors, and operational context of your AI model...", height=200)
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

elif choice == "Evaluation":
    st.header("Evaluate Your AI Model/Application")
    if 'ai_name' not in st.session_state or 'ai_description' not in st.session_state:
        st.warning("Please provide details about your AI model/application in the 'AI Model Input' section first.")
    else:
        st.subheader(f"AI Model/Application: {st.session_state['ai_name']}")
        st.write(f"**Description:** {st.session_state['ai_description']}")
        with st.form(key='evaluation_form'):
            st.markdown("### Evaluation Questionnaire")
            responses = {}
            for question in likert_questions:
                responses[question] = st.radio(question, options=["Disagree", "Agree"], index=1)
            for question in additional_questions:
                if question == "Is the AI model tangible or intangible?":
                    responses[question] = st.selectbox(question, options=["Tangible", "Intangible"])
                elif question == "Does the AI model result in cost reduction or cost increase?":
                    responses[question] = st.selectbox(question, options=["Cost Reduction", "Cost Increase"])
                elif question == "Does the AI model result in revenue increase or revenue reduction?":
                    responses[question] = st.selectbox(question, options=["Revenue Increase", "Revenue Reduction"])
            submit_evaluation = st.form_submit_button(label='Submit Evaluation')
        
        if submit_evaluation:
            st.session_state['evaluation'] = responses
            st.success("Evaluation submitted successfully!")

elif choice == "Results":
    st.header("Evaluation Results")
    if 'evaluation' not in st.session_state:
        st.warning("Please complete an evaluation in the 'Evaluation' section first.")
    else:
        responses = st.session_state['evaluation']
        kpi_df = st.session_state['kpi_data']
        
        st.subheader("Usable KPIs")
        relevant_kpis = kpi_df.copy()
        st.dataframe(relevant_kpis)
        fig_kpi = px.bar(relevant_kpis, x='KPI Focus', y='KPI Metrics', title="KPIs Visualization")
        st.plotly_chart(fig_kpi, use_container_width=True)
        
        st.subheader("Model Evaluation")
        tangible = responses.get("Is the AI model tangible or intangible?", "Intangible")
        cost_impact = responses.get("Does the AI model result in cost reduction or cost increase?", "Cost Reduction")
        revenue_impact = responses.get("Does the AI model result in revenue increase or revenue reduction?", "Revenue Increase")
        
        eval_summary = pd.DataFrame({
            "Aspect": ["Tangible/Intangible", "Cost Impact", "Revenue Impact"],
            "Evaluation": [tangible, cost_impact, revenue_impact]
        })
        st.table(eval_summary)
        
        fig_eval = px.bar(eval_summary, x='Aspect', y='Evaluation', title="Model Evaluation", text='Evaluation')
        st.plotly_chart(fig_eval, use_container_width=True)

elif choice == "Feedback":
    st.header("Provide Your Feedback")
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
        feedback_df = pd.DataFrame.from_dict(feedback_scores, orient='index', columns=['Rating'])
        feedback_df.reset_index(inplace=True)
        feedback_df.rename(columns={'index': 'Question'}, inplace=True)
        st.table(feedback_df)
        st.write("**Your Comments:**")
        st.write(comments)

st.markdown("""
---
**Built with Streamlit and Python**  
[Streamlit](https://streamlit.io/) | [Python](https://www.python.org/)
""")
