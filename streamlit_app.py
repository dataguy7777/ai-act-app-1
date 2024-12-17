import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="App di Valutazione Modello AI", layout="wide")

st.sidebar.title("Valutazione Valore AI")
menu = ["Panoramica", "Input Modello AI", "Valutazione", "Risultati", "Feedback"]
choice = st.sidebar.radio("Naviga", menu)

# Dati KPI, KQI e KRI (in italiano)
kpi_data = [
    {"Business Objective": "Nuove Fonti di Creazione di Valore", "Tipo": "KPI", "Categoria KPI": "Canali Digitali", "Focus KPI": "Ricavi & Profitti", "Metriche KPI": "Ordini, Ricavi, Traffico Clienti, Transazioni, Ordini Sociali"},
    {"Business Objective": "Nuove Fonti di Creazione di Valore", "Tipo": "KPI", "Categoria KPI": "Ecosistema Digitale", "Focus KPI": "Ricavi & Profitti", "Metriche KPI": "Partner & Reti, Referral & Profitti"},
    {"Business Objective": "Nuove Fonti di Creazione di Valore", "Tipo": "KPI", "Categoria KPI": "Integrazione Fisica", "Focus KPI": "Ricavi & Profitti", "Metriche KPI": "Prodotti Digitali, Prezzi, Promozioni, Nuovi Modelli di Business"},
    {"Business Objective": "Coinvolgimento del Cliente", "Tipo": "KQI", "Categoria KQI": "Tempo Risparmiato dal Cliente", "Focus KQI": "Tempo Risparmiato", "Metriche KQI": "Ore Risparmiate, Tempo per Completare, Per Richiesta"},
    {"Business Objective": "Efficienza Operativa", "Tipo": "KPI", "Categoria KPI": "Velocità di Risposta, Consegna", "Focus KPI": "Tempo & Conformità", "Metriche KPI": "Riduzione del Tempo di Consegna, % Conformità, Tempo di Attesa, Lavoro Completato"},
    {"Business Objective": "Coinvolgimento della Forza Lavoro", "Tipo": "KRI", "Categoria KRI": "Diversità, Equità & Inclusione", "Focus KRI": "Performance & Inclusione", "Metriche KRI": "Indice DEI %, Ore di Formazione, Miglioramento %"},
    {"Business Objective": "Coinvolgimento della Forza Lavoro", "Tipo": "KQI", "Categoria KQI": "Gestione del Talento", "Focus KQI": "Performance & Ritenzione", "Metriche KQI": "Produttività & Efficienza, % Ritenzione Talenti, % Turnover"}
]

# Domande Likert (in italiano)
likert_questions = [
    "Il modello AI raggiunge efficacemente l'obiettivo aziendale previsto.",
    "I KPI identificati sono appropriati per misurare le prestazioni del modello AI.",
    "I KQI suggeriti forniscono preziose intuizioni sulla qualità del modello AI.",
    "I KRI aiutano a mitigare i rischi associati all'applicazione AI.",
    "Il modello AI è allineato con i requisiti di conformità e regolamentazione (es. AI Act).",
    "L'applicazione AI migliora l'efficienza operativa misurata dai KPI rilevanti.",
    "Il coinvolgimento del cliente è aumentato grazie all'implementazione del modello AI.",
    "Il modello AI ha un impatto positivo sulla produttività della forza lavoro e sulla gestione dei talenti.",
    "Il modello AI supporta efficacemente gli obiettivi di sostenibilità.",
    "Le raccomandazioni generate dall'AI sono azionabili e rilevanti per gli obiettivi aziendali."
]

# Domande aggiuntive (in italiano)
additional_questions = [
    "Il modello AI è tangibile o intangibile?",
    "Il modello AI comporta una riduzione dei costi o un aumento dei costi?",
    "Il modello AI comporta un aumento dei ricavi o una riduzione dei ricavi?"
]

# Funzione per caricare i dati KPI/KQI/KRI
def load_kpi_data(uploaded_file=None):
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("Dati KPI/KQI/KRI caricati con successo.")
            return df
        except:
            st.error("Errore nel caricamento del file. Utilizzo dei dati KPI predefiniti.")
            return pd.DataFrame(kpi_data)
    else:
        return pd.DataFrame(kpi_data)

# Panoramica
if choice == "Panoramica":
    st.title("App di Valutazione Modello AI")
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)
    st.markdown("""
    **Caratteristiche:**
    - **Valutazione Strutturata**: Rispondi a domande comprehensive per valutare il tuo modello AI.
    - **Dashboard Interattiva**: Visualizza i tuoi KPI con grafici e tabelle dinamici.
    - **Sistema di Feedback**: Fornisci feedback per migliorare il processo di valutazione.
    
    **Come Usare:**
    1. Naviga nella sezione **Input Modello AI** per descrivere la tua applicazione AI.
    2. Procedi alla sezione **Valutazione** per rispondere alle domande di valutazione.
    3. Visualizza e analizza i risultati nella sezione **Risultati**.
    4. Fornisci feedback nella sezione **Feedback** per aiutare a perfezionare il sistema.
    """)

# Input Modello AI
elif choice == "Input Modello AI":
    st.header("Descrivi il Tuo Modello/App AI")
    with st.form(key='ai_model_form'):
        ai_name = st.text_input("Nome del Modello/App AI", "es. Previsione di Abbandono Cliente")
        ai_description = st.text_area("Descrizione del Modello/App AI", "Descrivi lo scopo, il dominio target, i fattori di rischio e il contesto operativo del tuo modello AI...", height=200)
        uploaded_file = st.file_uploader("Carica Dati KPI/KQI/KRI (Opzionale)", type=["csv"])
        submit_button = st.form_submit_button(label='Salva Descrizione')
    
    if submit_button:
        if ai_name and ai_description:
            st.session_state['ai_name'] = ai_name
            st.session_state['ai_description'] = ai_description
            st.session_state['kpi_data'] = load_kpi_data(uploaded_file)
            st.success("Dettagli del Modello/App AI salvati con successo!")
        else:
            st.error("Per favore, fornisci sia il Nome del Modello/App AI che la Descrizione.")

# Valutazione
elif choice == "Valutazione":
    st.header("Valuta il Tuo Modello/App AI")
    if 'ai_name' not in st.session_state or 'ai_description' not in st.session_state:
        st.warning("Per favore, fornisci i dettagli del tuo modello/app AI nella sezione 'Input Modello AI' prima.")
    else:
        st.subheader(f"Modello/App AI: {st.session_state['ai_name']}")
        st.write(f"**Descrizione:** {st.session_state['ai_description']}")
        with st.form(key='evaluation_form'):
            st.markdown("### Questionario di Valutazione")
            st.markdown("""
            **Scala:**
            - **1**: Fortemente in disaccordo
            - **4**: Neutrale
            - **7**: Fortemente d'accordo
            """)
            col1, col2 = st.columns(2)
            responses = {}
            for i, question in enumerate(likert_questions):
                with col1 if i % 2 == 0 else col2:
                    responses[question] = st.select_slider(
                        question,
                        options=range(1, 8),
                        value=4,
                        format_func=lambda x: f"{x}"
                    )
            st.markdown("---")
            for question in additional_questions:
                if question == "Il modello AI è tangibile o intangibile?":
                    responses[question] = st.selectbox(question, options=["Tangibile", "Intangibile"])
                elif question == "Il modello AI comporta una riduzione dei costi o un aumento dei costi?":
                    responses[question] = st.selectbox(question, options=["Riduzione dei Costi", "Aumento dei Costi"])
                elif question == "Il modello AI comporta un aumento dei ricavi o una riduzione dei ricavi?":
                    responses[question] = st.selectbox(question, options=["Aumento dei Ricavi", "Riduzione dei Ricavi"])
            submit_evaluation = st.form_submit_button(label='Invia Valutazione')
        
        if submit_evaluation:
            st.session_state['evaluation'] = responses
            st.success("Valutazione inviata con successo!")

# Risultati
elif choice == "Risultati":
    st.header("Risultati della Valutazione")
    if 'evaluation' not in st.session_state:
        st.warning("Per favore, completa una valutazione nella sezione 'Valutazione' prima.")
    else:
        responses = st.session_state['evaluation']
        kpi_df = st.session_state['kpi_data']
        
        # Mappatura delle domande ai Business Objectives
        question_mapping = {
            "Il modello AI raggiunge efficacemente l'obiettivo aziendale previsto.": "Nuove Fonti di Creazione di Valore",
            "I KPI identificati sono appropriati per misurare le prestazioni del modello AI.": "Nuove Fonti di Creazione di Valore",
            "I KQI suggeriti forniscono preziose intuizioni sulla qualità del modello AI.": "Coinvolgimento del Cliente",
            "I KRI aiutano a mitigare i rischi associati all'applicazione AI.": "Coinvolgimento della Forza Lavoro",
            "Il modello AI è allineato con i requisiti di conformità e regolamentazione (es. AI Act).": "Efficienza Operativa",
            "L'applicazione AI migliora l'efficienza operativa misurata dai KPI rilevanti.": "Efficienza Operativa",
            "Il coinvolgimento del cliente è aumentato grazie all'implementazione del modello AI.": "Coinvolgimento del Cliente",
            "Il modello AI ha un impatto positivo sulla produttività della forza lavoro e sulla gestione dei talenti.": "Coinvolgimento della Forza Lavoro",
            "Il modello AI supporta efficacemente gli obiettivi di sostenibilità.": "Coinvolgimento del Cliente",
            "Le raccomandazioni generate dall'AI sono azionabili e rilevanti per gli obiettivi aziendali.": "Nuove Fonti di Creazione di Valore"
        }
        
        # Calcolo del punteggio per ogni Business Objective
        business_scores = {}
        for question, score in responses.items():
            if question in question_mapping:
                obj = question_mapping[question]
                business_scores[obj] = business_scores.get(obj, 0) + score
        
        # Determinare i Business Objectives con punteggio sopra la media
        avg_score = sum(business_scores.values()) / len(business_scores) if business_scores else 0
        relevant_objectives = [obj for obj, score in business_scores.items() if score >= avg_score]
        
        # Filtrare KPI, KQI, KRI basati sui Business Objectives rilevanti
        relevant_kpis = kpi_df[(kpi_df['Business Objective'].isin(relevant_objectives)) & (kpi_df['Tipo'] == "KPI")]
        relevant_kqis = kpi_df[(kpi_df['Business Objective'].isin(relevant_objectives)) & (kpi_df['Tipo'] == "KQI")]
        relevant_kris = kpi_df[(kpi_df['Business Objective'].isin(relevant_objectives)) & (kpi_df['Tipo'] == "KRI")]
        
        # Risultati KPI
        st.subheader("KPI Utilizzabili")
        if not relevant_kpis.empty:
            st.dataframe(relevant_kpis[['Business Objective', 'Categoria KPI', 'Focus KPI', 'Metriche KPI']])
            fig_kpi = px.bar(relevant_kpis, x='Focus KPI', y='Metriche KPI', color='Categoria KPI',
                             title="Visualizzazione dei KPI", labels={"Focus KPI": "Focus", "Metriche KPI": "Metriche"})
            st.plotly_chart(fig_kpi, use_container_width=True)
        else:
            st.write("Nessun KPI rilevante trovato basato sulla valutazione.")
        
        # Risultati KQI
        st.subheader("KQI Utilizzabili")
        if not relevant_kqis.empty:
            st.dataframe(relevant_kqis[['Business Objective', 'Categoria KQI', 'Focus KQI', 'Metriche KQI']])
            fig_kqi = px.bar(relevant_kqis, x='Focus KQI', y='Metriche KQI', color='Categoria KQI',
                             title="Visualizzazione dei KQI", labels={"Focus KQI": "Focus", "Metriche KQI": "Metriche"})
            st.plotly_chart(fig_kqi, use_container_width=True)
        else:
            st.write("Nessun KQI rilevante trovato basato sulla valutazione.")
        
        # Risultati KRI
        st.subheader("KRI Utilizzabili")
        if not relevant_kris.empty:
            st.dataframe(relevant_kris[['Business Objective', 'Categoria KRI', 'Focus KRI', 'Metriche KRI']])
            fig_kri = px.bar(relevant_kris, x='Focus KRI', y='Metriche KRI', color='Categoria KRI',
                             title="Visualizzazione dei KRI", labels={"Focus KRI": "Focus", "Metriche KRI": "Metriche"})
            st.plotly_chart(fig_kri, use_container_width=True)
        else:
            st.write("Nessun KRI rilevante trovato basato sulla valutazione.")
        
        # Valutazione del Modello
        st.subheader("Valutazione del Modello")
        tangible = responses.get("Il modello AI è tangibile o intangibile?", "Intangibile")
        cost_impact = responses.get("Il modello AI comporta una riduzione dei costi o un aumento dei costi?", "Riduzione dei Costi")
        revenue_impact = responses.get("Il modello AI comporta un aumento dei ricavi o una riduzione dei ricavi?", "Aumento dei Ricavi")
        
        eval_summary = pd.DataFrame({
            "Aspetto": ["Tangibile/Intangibile", "Impatto sui Costi", "Impatto sui Ricavi"],
            "Valutazione": [tangible, cost_impact, revenue_impact]
        })
        st.table(eval_summary)
        
        # Visualizzazione della Valutazione del Modello
        fig_eval = px.bar(eval_summary, 
                          x='Aspetto', 
                          y='Valutazione', 
                          title="Valutazione del Modello",
                          text='Valutazione',
                          color='Aspetto',
                          color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_eval.update_traces(texttemplate='%{text}', textposition='outside')
        fig_eval.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', yaxis_title="")
        st.plotly_chart(fig_eval, use_container_width=True)

# Feedback
elif choice == "Feedback":
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
                feedback_scores[question] = st.select_slider(
                    question,
                    options=range(1, 8),
                    value=4,
                    format_func=lambda x: f"{x}"
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

st.markdown("""
---
**Realizzato con Streamlit e Python**  
[Streamlit](https://streamlit.io/) | [Python](https://www.python.org/)
""")
