import streamlit as st
import pandas as pd

st.set_page_config(page_title="App di Valutazione Modello AI", layout="wide")

st.sidebar.title("Valutazione Valore AI")
menu = ["Panoramica", "Input Modello AI", "Valutazione", "Risultati", "Feedback"]
choice = st.sidebar.radio("Naviga", menu)

# Dati KPI, KQI e KRI (in italiano)
kpi_data = [
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

# Domande Likert (in italiano) associate ai Business Objectives
likert_questions = {
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
    - **Dashboard Interattiva**: Visualizza i tuoi KPI con tabelle ben formattate.
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
        
        # Creazione delle tabs per ciascun Business Objective
        evaluation_tabs = st.tabs(["Nuove Fonti di Creazione di Valore", "Coinvolgimento del Cliente", "Efficienza Operativa", "Coinvolgimento della Forza Lavoro"])
        responses = {}
        
        with st.form(key='evaluation_form'):
            for tab, objective in zip(evaluation_tabs, likert_questions.keys()):
                with tab:
                    st.markdown(f"### {objective}")
                    for question in likert_questions[objective]:
                        responses[question] = st.slider(
                            question,
                            min_value=1,
                            max_value=7,
                            value=4,
                            step=1,
                            format="{}",
                            help="1: Fortemente in disaccordo | 7: Fortemente d'accordo"
                        )
            # Domande aggiuntive convertite in scala Likert
            st.markdown("---")
            st.markdown("### Valutazioni Aggiuntive")
            for question in additional_questions:
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
            "Il modello AI facilita l'innovazione all'interno dell'azienda.": "Nuove Fonti di Creazione di Valore",
            "Il modello AI contribuisce a migliorare la soddisfazione del cliente.": "Nuove Fonti di Creazione di Valore",
            "Il modello AI è facilmente integrabile con i sistemi esistenti.": "Nuove Fonti di Creazione di Valore",
            "Il modello AI contribuisce significativamente alla riduzione dei costi.": "Efficienza Operativa",
            "Il modello AI contribuisce significativamente all'aumento dei ricavi.": "Efficienza Operativa",
            "Il modello AI è facilmente comprensibile e misurabile.": "Efficienza Operativa",
            "Il modello AI riduce significativamente i tempi di processo.": "Efficienza Operativa",
            "Il modello AI aumenta la qualità dei servizi/prodotti offerti.": "Efficienza Operativa",
            "Il coinvolgimento del cliente è aumentato grazie all'implementazione del modello AI.": "Coinvolgimento del Cliente",
            "Il modello AI supporta efficacemente gli obiettivi di sostenibilità.": "Coinvolgimento del Cliente",
            "Le raccomandazioni generate dall'AI sono azionabili e rilevanti per gli obiettivi aziendali.": "Coinvolgimento del Cliente",
            "Il modello AI ha un impatto positivo sulla produttività della forza lavoro e sulla gestione dei talenti.": "Coinvolgimento della Forza Lavoro",
            "I KQI suggeriti forniscono preziose intuizioni sulla qualità del modello AI.": "Coinvolgimento della Forza Lavoro",
            "I KRI aiutano a mitigare i rischi associati all'applicazione AI.": "Coinvolgimento della Forza Lavoro"
        }
        
        # Calcolo del punteggio per ogni Business Objective
        business_scores = {}
        for question, score in responses.items():
            if question in question_mapping:
                obj = question_mapping[question]
                business_scores[obj] = business_scores.get(obj, 0) + score
        
        # Determinare i Business Objectives con punteggi sopra la media
        avg_score = sum(business_scores.values()) / len(business_scores) if business_scores else 0
        relevant_objectives = [obj for obj, score in business_scores.items() if score >= avg_score]
        
        # Filtrare KPI, KQI, KRI basati sui Business Objectives rilevanti
        relevant_kpis = kpi_df[(kpi_df['Business Objective'].isin(relevant_objectives)) & (kpi_df['Tipo'] == "KPI")]
        relevant_kqis = kpi_df[(kpi_df['Business Objective'].isin(relevant_objectives)) & (kpi_df['Tipo'] == "KQI")]
        relevant_kris = kpi_df[(kpi_df['Business Objective'].isin(relevant_objectives)) & (kpi_df['Tipo'] == "KRI")]
        
        # Creazione delle tabs per ciascun Business Objective nei Risultati
        result_tabs = st.tabs(["Nuove Fonti di Creazione di Valore", "Coinvolgimento del Cliente", "Efficienza Operativa", "Coinvolgimento della Forza Lavoro"])
        
        # Funzione per formattare KPI/KQI/KRI
        def display_indicators(indicators, tipo):
            if not indicators.empty:
                for index, row in indicators.iterrows():
                    st.markdown(f"**Categoria {tipo}:** {row['Categoria']}")
                    st.markdown(f"- **Focus:** {row['Focus']}")
                    st.markdown(f"- **Metriche:** {row['Metriche']}")
                    st.markdown("---")
            else:
                st.write(f"Nessun {tipo} rilevante trovato per questa categoria.")
        
        # Tab: Nuove Fonti di Creazione di Valore
        with result_tabs[0]:
            st.subheader("KPI Utilizzabili")
            display_indicators(relevant_kpis[relevant_kpis['Business Objective'] == "Nuove Fonti di Creazione di Valore"], "KPI")
            
            st.subheader("KQI Utilizzabili")
            display_indicators(relevant_kqis[relevant_kqis['Business Objective'] == "Nuove Fonti di Creazione di Valore"], "KQI")
            
            st.subheader("KRI Utilizzabili")
            display_indicators(relevant_kris[relevant_kris['Business Objective'] == "Nuove Fonti di Creazione di Valore"], "KRI")
        
        # Tab: Coinvolgimento del Cliente
        with result_tabs[1]:
            st.subheader("KPI Utilizzabili")
            display_indicators(relevant_kpis[relevant_kpis['Business Objective'] == "Coinvolgimento del Cliente"], "KPI")
            
            st.subheader("KQI Utilizzabili")
            display_indicators(relevant_kqis[relevant_kqis['Business Objective'] == "Coinvolgimento del Cliente"], "KQI")
            
            st.subheader("KRI Utilizzabili")
            display_indicators(relevant_kris[relevant_kris['Business Objective'] == "Coinvolgimento del Cliente"], "KRI")
        
        # Tab: Efficienza Operativa
        with result_tabs[2]:
            st.subheader("KPI Utilizzabili")
            display_indicators(relevant_kpis[relevant_kpis['Business Objective'] == "Efficienza Operativa"], "KPI")
            
            st.subheader("KQI Utilizzabili")
            display_indicators(relevant_kqis[relevant_kqis['Business Objective'] == "Efficienza Operativa"], "KQI")
            
            st.subheader("KRI Utilizzabili")
            display_indicators(relevant_kris[relevant_kris['Business Objective'] == "Efficienza Operativa"], "KRI")
        
        # Tab: Coinvolgimento della Forza Lavoro
        with result_tabs[3]:
            st.subheader("KPI Utilizzabili")
            display_indicators(relevant_kpis[relevant_kpis['Business Objective'] == "Coinvolgimento della Forza Lavoro"], "KPI")
            
            st.subheader("KQI Utilizzabili")
            display_indicators(relevant_kqis[relevant_kqis['Business Objective'] == "Coinvolgimento della Forza Lavoro"], "KQI")
            
            st.subheader("KRI Utilizzabili")
            display_indicators(relevant_kris[relevant_kris['Business Objective'] == "Coinvolgimento della Forza Lavoro"], "KRI")
        
        # Valutazione del Modello AI
        st.subheader("Valutazione del Modello")
        eval_summary = pd.DataFrame({
            "Aspetto": ["Comprensibilità e Misurabilità", "Contributo alla Riduzione dei Costi", "Contributo all'Aumento dei Ricavi"],
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

st.markdown("""
---
**Realizzato con Streamlit e Python**  
[Streamlit](https://streamlit.io/) | [Python](https://www.python.org/)
""")
