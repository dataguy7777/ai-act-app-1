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
    
    # Additional churn-focused KPI if scenario is chosen
    churn_kpi_data = [
        {"Business Objective": "Coinvolgimento del Cliente", "Tipo": "KPI", "Categoria": "Churn Reduction", "Focus": "Retenzione", "Metriche": "Tasso Churn pre/post"}
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
    If scenario is 'Churn', we add a churn-related question under 'Coinvolgimento del Cliente'.

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
        title (str, optional): Title of the gauge.
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
    plt.xlabel("Ease of Implementation (0-100)")
    plt.ylabel("Value Delivered (0-100)")
    st.pyplot(fig, use_container_width=True)

def input_ai_model():
    """
    Renders a form to input AI Model details and optionally upload KPI/KQI/KRI data.
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
        if ai_name and ai_description:
            st.session_state['ai_name'] = ai_name
            st.session_state['ai_description'] = ai_description
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
    relevant_kpis = kpi_df[(kpi_df['Business Objective'].isin(relevant_objectives)) & (kpi_df['Tipo'] == "KPI")]
    relevant_kqis = kpi_df[(kpi_df['Business Objective'].isin(relevant_objectives)) & (kpi_df['Tipo'] == "KQI")]
    relevant_kris = kpi_df[(kpi_df['Business Objective'].isin(relevant_objectives)) & (kpi_df['Tipo'] == "KRI")]

    # Calculate overall scores first and show the overall tangibility and matrix before KPI tabs
    ease_score, value_score = calculate_overall_scores(responses)
    tangibility_score = (value_score + ease_score) / 2  # Average for tangibility

    st.subheader("Valutazione Complessiva")
    # Show gauge and matrix first
    st.markdown("### **Tangibility of the AI Model**")
    display_gauge(tangibility_score, "Model Tangibility Score")
    
    st.markdown("### **Matrix Representation**")
    display_matrix(ease_score, value_score)
    st.markdown(f"**Ease of Implementation Score:** {ease_score:.2f}")
    st.markdown(f"**Value Delivered Score:** {value_score:.2f}")

    # Now show KPI tabs after overall evaluation
    st.markdown("---")
    st.info("Visualizzazione dei KPI/KQI/KRI in base agli obiettivi di business rilevanti...")

    # If no relevant objectives found
    if not relevant_objectives:
        st.write("Nessun obiettivo rilevante identificato dalla valutazione.")
        return
    
    result_tabs = st.tabs(relevant_objectives)

    def display_indicators_with_examples(indicators, tipo):
        """
        Display given indicators (KPI/KQI/KRI) with their formula and example.
        Now with more quantitative and specific units of measure in LaTeX.
        
        Args:
            indicators (pd.DataFrame): Subset of indicators for a given Business Objective.
            tipo (str): Tipo (KPI/KQI/KRI).
        """
        # More detailed formulas with units
        for index, row in indicators.iterrows():
            categoria = row.get('Categoria', 'N/A')
            focus = row.get('Focus', 'N/A')
            metriche = row.get('Metriche', 'N/A').split(', ')
            
            st.markdown(f"**Categoria {tipo}:** {categoria}")
            st.markdown(f"- **Focus:** {focus}")
            
            for metrica in metriche:
                metric = metrica.lower().strip()
                
                # Define a dictionary of improved formulas with units where possible
                if "tasso churn" in metric:
                    formula = r"Tasso\ Churn(\%) = \frac{\text{Clienti Persi nel Periodo}}{\text{Clienti Iniziali}} \times 100"
                    example = "Se su 1,000 clienti iniziali, 50 abbandonano nel mese, il Tasso Churn = (50/1000)*100 = 5%."
                
                elif metric == "ordini":
                    formula = r"\text{Ordini} = \text{Numero di Ordini (unità)}"
                    example = "Se in un mese ricevi 150 ordini, Ordini = 150 unità."
                elif metric == "ricavi":
                    formula = r"\text{Ricavi (€)} = \text{Prezzo Medio per Ordine (€)} \times \text{Numero di Ordini (unità)}"
                    example = "Se il prezzo medio è 50€ e ricevi 150 ordini, Ricavi = 50€ * 150 = 7,500€."
                elif "traffico clienti" in metric:
                    formula = r"\text{Traffico Clienti} = \text{Visite Totali (sessioni/mese)}"
                    example = "Se il tuo sito riceve 10,000 visite al mese, Traffico Clienti = 10,000 sessioni/mese."
                elif "transazioni" in metric:
                    formula = r"\text{Transazioni} = \text{Numero di Transazioni Completate (unità)}"
                    example = "Se vengono processate 200 transazioni in una settimana, Transazioni = 200."
                elif "ordini sociali" in metric:
                    formula = r"\text{Ordini Sociali} = \text{Ordini Provenienti da Canali Social (unità)}"
                    example = "Se 50 ordini provengono da canali social in un mese, Ordini Sociali = 50."
                elif "partner & reti" in metric:
                    formula = r"\text{Partner & Reti} = \text{Conteggio Partner Attivi e Reti (unità)}"
                    example = "Se hai 5 partner attivi e collabori con 3 reti, totale = 8."
                elif "referral & profitti" in metric:
                    formula = r"\text{Referral & Profitti (€)} = \text{Profitti da Referral (€)}"
                    example = "Se i referral generano 2,000€ di profitti, Referral & Profitti = 2,000€."
                elif "prodotti digitali" in metric:
                    formula = r"\text{Prodotti Digitali} = \text{Numero di Prodotti Digitali Offerti (unità)}"
                    example = "Se offri 10 prodotti digitali, Prodotti Digitali = 10."
                elif "prezzi" in metric:
                    formula = r"\text{Prezzi Medi (€)} = \frac{\text{Somma dei Prezzi di Tutti i Prodotti Venduti (€)}}{\text{Numero di Prodotti Venduti (unità)}}"
                    example = "Se vendi 100 prodotti per un totale di 5,000€, il prezzo medio è 5,000€/100 = 50€."
                elif "promozioni" in metric:
                    formula = r"\text{Promozioni} = \text{Numero di Promozioni Attuate (unità)}"
                    example = "Se lanci 3 promozioni in un mese, Promozioni = 3."
                elif "nuovi modelli di business" in metric:
                    formula = r"\text{Nuovi Modelli di Business} = \text{Numero di Modelli Introdotti (unità)}"
                    example = "Se introduci 2 nuovi modelli di business, Nuovi Modelli di Business = 2."
                elif "riduzione del tempo di consegna" in metric:
                    formula = r"\Delta \text{Tempo Consegna (giorni)} = \text{Tempo Iniziale} - \text{Tempo Attuale}"
                    example = "Se riduci la consegna da 5 a 3 giorni, riduzione = 2 giorni."
                elif "% conformità" in metric:
                    formula = r"\% Conformità = \frac{\text{Processi Conformi}}{\text{Processi Totali}} \times 100"
                    example = "Se 90 su 100 processi sono conformi, % Conformità = 90%."
                elif "tempo di attesa" in metric:
                    formula = r"\text{Tempo di Attesa (minuti)} = \text{Tempo Medio di Attesa per Cliente}"
                    example = "Se il tempo medio di attesa è 2 minuti, Tempo di Attesa = 2 min."
                elif "lavoro completato" in metric:
                    formula = r"\text{Lavoro Completato (unità)} = \text{Numero di Task Completati}"
                    example = "Se completi 50 task in una settimana, Lavoro Completato = 50."
                else:
                    # Default if not matched
                    formula = r"\text{Metrica non definita con unità specifiche}"
                    example = "Nessun esempio specifico disponibile."

                st.markdown(f"**{metrica.capitalize()}:**")
                st.latex(formula)
                st.markdown(f"*Esempio:* {example}\n")

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
    
    # After showing KPI tabs, show a detailed evaluation summary
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
    
    st.markdown("### Dettagli Valutazione")
    for index, row in eval_summary.iterrows():
        st.markdown(f"- **{row['Aspetto']}:** {row['Valutazione']}")


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
    
    # Footer
    st.markdown("""
    ---
    **Realizzato con Streamlit e Python**  
    [Streamlit](https://streamlit.io/) | [Python](https://www.python.org/)
    """)

if __name__ == "__main__":
    main()
