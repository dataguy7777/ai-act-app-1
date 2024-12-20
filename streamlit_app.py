import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Set page configuration with improved UI theme and icon
st.set_page_config(
    page_title="Valore AI",
    page_icon=":robot_face:",
    layout="wide"
)

# Improved styling for UI
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .sidebar .sidebar-content {
        background-color: #f0f0f0;
    }
    h1, h2, h3, h4 {
        color: #303030;
    }
</style>
""", unsafe_allow_html=True)

def sidebar_navigation():
    """
    Render the sidebar navigation and allow user to choose a page.

    Returns:
        str: The selected page from the sidebar.
    """
    # Updated menu to remove the "Panoramica" page and focus on input, evaluation, results, and feedback.
    st.sidebar.title("Valutazione Valore AI")
    menu = ["Input Modello AI", "Valutazione", "Risultati", "Feedback"]
    choice = st.sidebar.radio("Naviga", menu)
    return choice

def load_kpi_data(uploaded_file=None, scenario=None):
    """
    Load KPI/KQI/KRI data. If a file is uploaded, try to load it,
    otherwise use default data. Includes additional metrics focusing
    on churn evaluation in a Marketing & Sales scenario if the scenario
    is set to 'Churn'.

    Args:
        uploaded_file (UploadedFile, optional): Uploaded CSV file.  
            example: Load a CSV with columns: "Business Objective", "Tipo", "Categoria", "Focus", "Metriche".
        scenario (str, optional): Scenario to load additional KPI data. 
            e.g. "Churn" to load extended marketing & sales metrics.

    Returns:
        pd.DataFrame: Dataframe with KPI/KQI/KRI information.
    """
    default_kpi_data = [
        {"Business Objective": "Nuove Fonti di Creazione di Valore", "Tipo": "KPI", "Categoria": "Canali Digitali", "Focus": "Ricavi & Profitti", "Metriche": "Ordini, Ricavi, Traffico Clienti, Transazioni, Ordini Sociali"},
        {"Business Objective": "Nuove Fonti di Creazione di Valore", "Tipo": "KPI", "Categoria": "Ecosistema Digitale", "Focus": "Ricavi & Profitti", "Metriche": "Partner & Reti, Referral & Profitti"},
        {"Business Objective": "Nuove Fonti di Creazione di Valore", "Tipo": "KPI", "Categoria": "Integrazione Fisica", "Focus": "Ricavi & Profitti", "Metriche": "Prodotti Digitali, Prezzi, Promozioni, Nuovi Modelli di Business"},
        {"Business Objective": "Coinvolgimento del Cliente", "Tipo": "KQI", "Categoria": "Tempo Risparmiato dal Cliente", "Focus": "Tempo Risparmiato", "Metriche": "Ore Risparmiate, Tempo per Completare, Per Richiesta"},
        {"Business Objective": "Efficienza Operativa", "Tipo": "KPI", "Categoria": "Velocità di Risposta, Consegna", "Focus": "Tempo & Conformità", "Metriche": "Riduzione del Tempo di Consegna, % Conformità, Tempo di Attesa, Lavoro Completato"},
        {"Business Objective": "Coinvolgimento della Forza Lavoro", "Tipo": "KRI", "Categoria": "Diversità, Equità & Inclusione", "Focus": "Performance & Inclusione", "Metriche": "Indice DEI %, Ore di Formazione, Miglioramento %"},
        {"Business Objective": "Coinvolgimento della Forza Lavoro", "Tipo": "KQI", "Categoria": "Gestione del Talento", "Focus": "Performance & Ritenzione", "Metriche": "Produttività & Efficienza, % Ritenzione Talenti, % Turnover"},
        {"Business Objective": "Innovazione", "Tipo": "KQI", "Categoria": "Sviluppo Prodotto", "Focus": "Innovazione", "Metriche": "Numero di Nuovi Prodotti, Tempo di Sviluppo, Percentuale di Innovazione"},
        {"Business Objective": "Soddisfazione del Cliente", "Tipo": "KQI", "Categoria": "Feedback Cliente", "Focus": "Soddisfazione", "Metriche": "Net Promoter Score, Recensioni Positive, Tasso di Ritorno"},
        {"Business Objective": "Sostenibilità", "Tipo": "KRI", "Categoria": "Impatto Ambientale", "Focus": "Sostenibilità", "Metriche": "Emissioni di CO2, Consumo Energetico, Uso di Risorse Rinnovabili"}
    ]
    
    # Additional Marketing & Sales KPIs focusing on Customer Engagement and Churn
    # The user provided a large table. Here we extract a single relevant line as an example.
    # For churn scenario, we add a KPI that focuses on churn reduction.
    churn_kpi_data = [
        {"Business Objective": "Coinvolgimento del Cliente", "Tipo": "KPI", "Categoria": "Churn Reduction", "Focus": "Retenzione", "Metriche": "Tasso Churn pre/post"},
    ]

    if uploaded_file:
        st.info("Tentativo di caricare i dati KPI/KQI/KRI dal file fornito...")
        try:
            df = pd.read_csv(uploaded_file)
            required_columns = {"Business Objective", "Tipo", "Categoria", "Focus", "Metriche"}
            if not required_columns.issubset(set(df.columns)):
                missing = required_columns - set(df.columns)
                st.error(f"Il file caricato manca delle seguenti colonne richieste: {', '.join(missing)}")
                st.warning("Utilizzo dei dati KPI predefiniti.")
                base_df = pd.DataFrame(default_kpi_data)
            else:
                st.success("Dati KPI/KQI/KRI caricati con successo.")
                base_df = df
        except Exception as e:
            st.error(f"Errore nel caricamento del file: {e}. Utilizzo dei dati KPI predefiniti.")
            base_df = pd.DataFrame(default_kpi_data)
    else:
        st.info("Utilizzo dei dati KPI/KQI/KRI predefiniti.")
        base_df = pd.DataFrame(default_kpi_data)

    # If scenario is 'Churn', we merge the churn-focused KPIs into the base dataframe.
    if scenario == "Churn":
        st.info("Caricamento dei KPI focalizzati sulla riduzione del churn...")
        churn_df = pd.DataFrame(churn_kpi_data)
        base_df = pd.concat([base_df, churn_df], ignore_index=True)

    return base_df

def get_likert_questions(scenario=None):
    """
    Get a dictionary of business objectives mapped to their respective Likert scale questions.
    If scenario is 'Churn', we add a question related to churn reduction.

    Args:
        scenario (str, optional): If 'Churn', include churn-related question.

    Returns:
        dict: A mapping of business objectives to a list of questions.
    """
    base_questions = {
        "Nuove Fonti di Creazione di Valore": [
            "Il modello AI facilita l'innovazione all'interno dell'azienda.",
            "Il modello AI contribuisce a migliorare la soddisfazione del cliente.",
            "Il modello AI è facilmente integrabile con i sistemi esistenti."
        ],
        "Coinvolgimento del Cliente": [
            "Il coinvolgimento del cliente è aumentato grazie all'implementazione del modello AI.",
            "Il modello AI supporta efficacemente gli obiettivi di sostenibilità.",
            "Le raccomandazioni generate dall'AI sono azionabili e rilevanti per gli obiettivi aziendali."
        ],
        "Efficienza Operativa": [
            "Il modello AI riduce significativamente i tempi di processo.",
            "Il modello AI aumenta la qualità dei servizi/prodotti offerti.",
            "Il modello AI contribuisce significativamente alla riduzione dei costi.",
            "Il modello AI contribuisce significativamente all'aumento dei ricavi.",
            "Il modello AI è facilmente comprensibile e misurabile."
        ],
        "Coinvolgimento della Forza Lavoro": [
            "Il modello AI ha un impatto positivo sulla produttività della forza lavoro e sulla gestione dei talenti."
        ]
    }

    # If scenario is churn, add a churn-related question under Coinvolgimento del Cliente
    if scenario == "Churn":
        base_questions["Coinvolgimento del Cliente"].append(
            "Il modello di AI ha contribuito a ridurre il churn del cliente."
        )

    return base_questions

def display_gauge(score, title="Tangibility Score"):
    """
    Display a gauge chart using Plotly for the given score.

    Args:
        score (float): The score to be displayed on the gauge.
        title (str, optional): Title of the gauge. example: "Model Tangibility Score".
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': title},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 33], 'color': "lightgray"},
                {'range': [33, 66], 'color': "yellow"},
                {'range': [66, 100], 'color': "lightgreen"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': score}
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

def display_matrix(ease_score, value_score):
    """
    Display a matrix (quadrant) chart using matplotlib to show Ease of Implementation vs Value Delivered.

    Args:
        ease_score (float): The ease of implementation score.
        value_score (float): The value delivered score.
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    plt.axvline(50, color='grey', linestyle='--')  # Mid vertical line
    plt.axhline(50, color='grey', linestyle='--')  # Mid horizontal line

    # Labels in quadrants
    plt.text(20, 80, "Easy Value", ha="center", va="center", fontsize=12, fontweight='bold')
    plt.text(80, 80, "Moonshots", ha="center", va="center", fontsize=12, fontweight='bold')
    plt.text(20, 20, "Low Value", ha="center", va="center", fontsize=12, fontweight='bold')
    plt.text(80, 20, "Money Pits", ha="center", va="center", fontsize=12, fontweight='bold')

    # Place the dot
    ax.scatter(ease_score, value_score, color="red", s=100)
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.xticks(range(0, 101, 10))
    plt.yticks(range(0, 101, 10))
    plt.title("Ease of Implementation vs Value Delivered")
    plt.xlabel("Ease of Implementation")
    plt.ylabel("Value Delivered")
    st.pyplot(fig, use_container_width=True)

def input_ai_model():
    """
    Renders a form to input AI Model details and optionally upload KPI/KQI/KRI data.

    Returns:
        None
    """
    st.header("Descrivi il Tuo Modello/App AI")
    with st.form(key='ai_model_form'):
        ai_name = st.text_input("Nome del Modello/App AI", "es. Previsione di Abbandono Cliente")
        ai_description = st.text_area("Descrizione del Modello/App AI", 
                                      "Descrivi lo scopo, il dominio target, i fattori di rischio e il contesto operativo del tuo modello AI...", height=200)
        scenario = st.selectbox("Scenario di Valutazione", ["Standard", "Churn"])
        uploaded_file = st.file_uploader("Carica Dati KPI/KQI/KRI (Opzionale)", type=["csv"])
        submit_button = st.form_submit_button(label='Salva Descrizione')
    
    if submit_button:
        # Logging input validation
        st.info("Verifica degli input del modello AI...")
        if ai_name and ai_description:
            st.session_state['ai_name'] = ai_name
            st.session_state['ai_description'] = ai_description
            # Load KPI data with scenario parameter
            scenario_param = "Churn" if scenario == "Churn" else None
            st.session_state['kpi_data'] = load_kpi_data(uploaded_file, scenario=scenario_param)
            st.session_state['scenario'] = scenario_param
            st.success("Dettagli del Modello/App AI salvati con successo!")
        else:
            st.error("Per favore, fornisci sia il Nome del Modello/App AI che la Descrizione.")

def evaluate_ai_model():
    """
    Allows the user to evaluate the AI model by answering Likert scale questions.
    Includes scenario-based questions if applicable.
    """
    st.header("Valuta il Tuo Modello/App AI")
    if 'ai_name' not in st.session_state or 'ai_description' not in st.session_state:
        st.warning("Per favore, fornisci i dettagli del tuo modello/app AI nella sezione 'Input Modello AI' prima.")
        return
    
    scenario = st.session_state.get('scenario', None)
    st.subheader(f"Modello/App AI: {st.session_state['ai_name']}")
    st.write(f"**Descrizione:** {st.session_state['ai_description']}")
    
    likert_questions = get_likert_questions(scenario=scenario)
    evaluation_tabs = st.tabs(likert_questions.keys())
    responses = {}
    
    with st.form(key='evaluation_form'):
        for tab, (objective, questions) in zip(evaluation_tabs, likert_questions.items()):
            with tab:
                st.markdown(f"### {objective}")
                for question in questions:
                    # Logging the question being answered
                    responses[question] = st.slider(
                        question,
                        min_value=1,
                        max_value=7,
                        value=4,
                        step=1,
                        format="{}",
                        help="1: Fortemente in disaccordo | 7: Fortemente d'accordo"
                    )
        submit_evaluation = st.form_submit_button(label='Invia Valutazione')
    
    if submit_evaluation:
        st.session_state['evaluation'] = responses
        st.success("Valutazione inviata con successo!")
        # Logging evaluation submission
        st.info("Valutazione del modello AI salvata con successo nel session state.")

def calculate_overall_scores(responses):
    """
    Calculate overall 'ease score' and 'value score' based on the responses.

    Args:
        responses (dict): Dictionary of question:score pairs.
        Returns:
            tuple: (ease_score, value_score) both scaled to 100.
    """
    ease_questions = [
        "Il modello AI è facilmente integrabile con i sistemi esistenti.",
        "Il modello AI è facilmente comprensibile e misurabile."
    ]
    value_score = sum(responses.values()) / len(responses) * 14.3  # Scale to 100
    ease_score = sum([responses.get(q, 4) for q in ease_questions]) / len(ease_questions) * 14.3
    return ease_score, value_score

def show_results():
    """
    Display the results of the evaluation, including relevant KPI/KQI/KRI,
    scores, and visualizations.
    """
    st.header("Risultati della Valutazione")
    if 'evaluation' not in st.session_state:
        st.warning("Per favore, completa una valutazione nella sezione 'Valutazione' prima.")
        return
    
    responses = st.session_state['evaluation']
    kpi_df = st.session_state['kpi_data']
    scenario = st.session_state.get('scenario', None)
    likert_questions = get_likert_questions(scenario=scenario)
    
    # Mapping of questions to Business Objectives
    question_mapping = {}
    for objective, questions in likert_questions.items():
        for question in questions:
            question_mapping[question] = objective
    
    # Calculate scores per Business Objective
    business_scores = {}
    for question, score in responses.items():
        obj = question_mapping.get(question)
        if obj:
            business_scores[obj] = business_scores.get(obj, 0) + score
    
    # Calculate average score to determine relevant objectives
    avg_score = sum(business_scores.values()) / len(business_scores) if business_scores else 0
    relevant_objectives = [obj for obj, score in business_scores.items() if score >= avg_score]
    
    # Filter KPI/KQI/KRI based on relevant objectives
    relevant_kpis = kpi_df[kpi_df['Business Objective'].isin(relevant_objectives) & (kpi_df['Tipo'] == "KPI")]
    relevant_kqis = kpi_df[kpi_df['Business Objective'].isin(relevant_objectives) & (kpi_df['Tipo'] == "KQI")]
    relevant_kris = kpi_df[kpi_df['Business Objective'].isin(relevant_objectives) & (kpi_df['Tipo'] == "KRI")]

    st.info("Visualizzazione dei risultati in base agli obiettivi di business rilevanti...")

    # Tabs for each Business Objective
    if relevant_objectives:
        result_tabs = st.tabs(relevant_objectives)
    else:
        st.write("Nessun obiettivo rilevante identificato dalla valutazione.")
        return
    
    def display_indicators_with_examples(indicators, tipo):
        """
        Display given indicators (KPI/KQI/KRI) with their formula and example.

        Args:
            indicators (pd.DataFrame): Subset of indicators for a given Business Objective.
            tipo (str): Tipo indicator (KPI, KQI, or KRI).
        """
        if not indicators.empty:
            for index, row in indicators.iterrows():
                categoria = row.get('Categoria', 'N/A')
                focus = row.get('Focus', 'N/A')
                metriche = row.get('Metriche', 'N/A').split(', ')
                
                st.markdown(f"**Categoria {tipo}:** {categoria}")
                st.markdown(f"- **Focus:** {focus}")
                
                for metrica in metriche:
                    metric = metrica.lower().strip()
                    formula = r"\text{Definizione non disponibile}"
                    example = "Nessun esempio disponibile."

                    # Add a churn-related example if we detect the churn metric
                    if "tasso churn" in metric:
                        formula = r"Tasso\ Churn = \frac{\text{Numero Clienti Persi nel Periodo}}{\text{Numero Clienti Iniziali nel Periodo}} \times 100"
                        example = "Se su 1,000 clienti iniziali, 50 abbandonano nel mese, il Tasso Churn = (50/1000)*100 = 5%."

                    # Other standard metrics (you can extend as needed)
                    elif metric == "ordini":
                        formula = r"Numero\ di\ Ordini = \text{Totale Ordini Ricevuti in un Periodo}"
                        example = "Se in un mese ricevi 150 ordini, il Numero di Ordini è 150."
                    elif metric == "ricavi":
                        formula = r"Ricavi = \text{Prezzo Medio per Ordine} \times \text{Numero di Ordini}"
                        example = "Se il prezzo medio per ordine è €50 e ricevi 150 ordini, i Ricavi sono €7,500."

                    st.markdown(f"**{metrica}:**")
                    st.latex(formula)
                    st.markdown(f"*Esempio:* {example}\n")
        else:
            st.write(f"Nessun {tipo} rilevante trovato per questa categoria.")
    
    for tab, objective in zip(result_tabs, relevant_objectives):
        with tab:
            st.subheader(f"KPI/KQI/KRI per {objective}")
            st.markdown("**KPI/KQI/KRI Utilizzabili**")
            indicators = kpi_df[kpi_df['Business Objective'] == objective]
            tipi = indicators['Tipo'].unique()
            for tipo in tipi:
                st.markdown(f"### {tipo}")
                subset = indicators[indicators['Tipo'] == tipo]
                display_indicators_with_examples(subset, tipo)
    
    st.markdown("---")
    st.subheader("Valutazione Complessiva")
    
    # Calculate overall scores
    ease_score, value_score = calculate_overall_scores(responses)
    tangibility_score = (value_score + ease_score) / 2  # Average for tangibility
    
    # Tabs for overall visualizations
    overall_tabs = st.tabs(["Valutazione Complessiva", "Nuove Fonti di Creazione di Valore", 
                            "Coinvolgimento del Cliente", "Efficienza Operativa", "Coinvolgimento della Forza Lavoro"])
    
    with overall_tabs[0]:
        st.markdown("### **Tangibility of the AI Model**")
        display_gauge(tangibility_score, "Model Tangibility Score")
    
        st.markdown("### **Matrix Representation**")
        display_matrix(ease_score, value_score)
        st.markdown(f"**Ease of Implementation Score:** {ease_score:.2f}")
        st.markdown(f"**Value Delivered Score:** {value_score:.2f}")
    
    st.markdown("---")
    st.subheader("Valutazione Dettagliata")
    eval_summary = pd.DataFrame({
        "Aspetto": [
            "Comprensibilità e Misurabilità", 
            "Contributo alla Riduzione dei Costi", 
            "Contributo all'Aumento dei Ricavi"
        ],
        "Valutazione": [
            responses.get("Il modello AI è facilmente comprensibile e misurabile.", 4),
            responses.get("Il modello AI contribuisce significativamente alla riduzione dei costi.", 4),
            responses.get("Il modello AI contribuisce significativamente all'aumento dei ricavi.", 4)
        ]
    })
    st.table(eval_summary)
    
    st.markdown("### Valutazione Dettagliata")
    for index, row in eval_summary.iterrows():
        st.markdown(f"- **{row['Aspetto']}:** {row['Valutazione']}")

def feedback_section():
    """
    Collect user feedback about the app's usability and effectiveness.
    """
    st.header("Fornisci il Tuo Feedback")
    with st.form(key='feedback_form'):
        st.markdown("### Valuta l'Esperienza dell'App")
        st.markdown("""
        **Scala:**
        - **1**: Fortemente in disaccordo
        - **4**: Neutrale
        - **7**: Fortemente d'accordo
        """)
        feedback_scores = {}
        feedback_questions = [
            "L'interfaccia dell'app è intuitiva.",
            "Il processo di valutazione è stato chiaro e completo.",
            "Le suggerimenti di KPI/KQI/KRI sono rilevanti.",
            "Le visualizzazioni rappresentano efficacemente i dati.",
            "Nel complesso, sono soddisfatto dell'app."
        ]
        col1, col2 = st.columns(2)
        for i, question in enumerate(feedback_questions):
            with col1 if i % 2 == 0 else col2:
                feedback_scores[question] = st.slider(
                    question,
                    min_value=1,
                    max_value=7,
                    value=4,
                    step=1,
                    format="{}",
                    help="1: Fortemente in disaccordo | 7: Fortemente d'accordo"
                )
        st.markdown("---")
        st.subheader("Commenti Aggiuntivi")
        comments = st.text_area("I Tuoi Commenti", height=100)
        submit_feedback = st.form_submit_button(label='Invia Feedback')
    
    if submit_feedback:
        st.success("Grazie per il tuo feedback!")
        feedback_df = pd.DataFrame.from_dict(feedback_scores, orient='index', columns=['Valutazione'])
        feedback_df.reset_index(inplace=True)
        feedback_df.rename(columns={'index': 'Domanda'}, inplace=True)
        st.table(feedback_df)
        st.write("**I Tuoi Commenti:**")
        st.write(comments)
        st.info("Feedback inviato con successo. Grazie per il tuo contributo!")

def main():
    """
    Main function to orchestrate the rendering of pages based on user's selection.
    """
    choice = sidebar_navigation()
    
    if choice == "Input Modello AI":
        input_ai_model()
    
    elif choice == "Valutazione":
        evaluate_ai_model()
    
    elif choice == "Risultati":
        show_results()
    
    elif choice == "Feedback":
        feedback_section()
    
    # Footer
    st.markdown("""
    ---
    **Realizzato con Streamlit e Python**  
    [Streamlit](https://streamlit.io/) | [Python](https://www.python.org/)
    """)

if __name__ == "__main__":
    main()
