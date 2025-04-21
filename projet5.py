import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

# Configuration de la page Streamlit
st.set_page_config(page_title="Conseiller Financier Virtuel", layout="wide")
st.title("💼 Conseiller Financier Virtuel")

# Variables par défaut
profil_data = {
    "age": 30,
    "objectif": "Épargne retraite",
    "montant_initial": 1000,
    "investissement_mensuel": 100,
    "duree": 10,
    "connaissance": "Débutant",
    "risque": "Modérée",
    "situation_familiale": "Célibataire",
    "epargne_urgence": "Oui",
    "preference_esg": False,
    "horizon_liquidite": "Non",
    "age_retraite": 65,
    "montant_retraite": 25000,
    "annees_retraite": 25
}

# Onglets
tabs = st.tabs([
    "Profil Financier", "Suggestions de Portefeuille", "Simulateur de Rendement",
    "Comparateur de Fonds", "Recherche d'Actions", "FAQ", "Analyse Technique",
    "Glossaire", "Watchlist", "Simulation Monte Carlo", "Quiz Financier", "Cryptomonnaie"
])

# 1. Profil Financier
with tabs[0]:
    st.header("📋 Profil Financier")
    with st.form("profil_form"):
        col1, col2 = st.columns(2)
        with col1:
            profil_data["age"] = st.number_input("Âge", 18, 100, value=profil_data["age"])
            profil_data["objectif"] = st.selectbox("Objectif d'investissement", ["Épargne retraite", "Achat maison", "Voyage", "Revenus passifs", "Autre"])
            profil_data["montant_initial"] = st.number_input("Montant disponible à investir maintenant ($)", 0)
            profil_data["investissement_mensuel"] = st.number_input("Montant investi chaque mois ($)", 0)
            profil_data["duree"] = st.slider("Durée de l'investissement (en années)", 1, 50, profil_data["duree"])
            profil_data["connaissance"] = st.select_slider("Connaissances en finance", ["Débutant", "Intermédiaire", "Avancé"])
        with col2:
            profil_data["risque"] = st.select_slider("Tolérance au risque", ["Faible", "Modérée", "Élevée"])
            profil_data["situation_familiale"] = st.selectbox("Situation familiale", ["Célibataire", "Marié(e)", "Avec enfants", "Sans enfants"])
            profil_data["epargne_urgence"] = st.radio("Avez-vous une épargne d'urgence?", ["Oui", "Non"])
            profil_data["preference_esg"] = st.checkbox("Je préfère des investissements responsables (ESG)")
            profil_data["horizon_liquidite"] = st.radio("Avez-vous besoin de liquidité à court terme?", ["Oui", "Non"])

        if profil_data["objectif"] == "Épargne retraite":
            profil_data["age_retraite"] = st.number_input("Âge prévu de la retraite", profil_data["age"], 100, 65)
            profil_data["montant_retraite"] = st.number_input("Montant annuel désiré à la retraite ($)", 0)
            profil_data["annees_retraite"] = st.number_input("Nombre d'années après la retraite", 1, 50, 25)

        submitted = st.form_submit_button("Analyser mon profil")

    if submitted:
        st.success("✅ Profil analysé avec succès!")
        st.json(profil_data)
        if profil_data["objectif"] == "Épargne retraite":
            besoin_retraite = profil_data["montant_retraite"] * profil_data["annees_retraite"]
            estimation = profil_data["montant_initial"] * (1 + 0.05) ** profil_data["duree"]
            if estimation >= besoin_retraite:
                st.success("🎉 Vous pourriez atteindre vos objectifs de retraite avec votre plan actuel!")
            else:
                st.warning("⚠️ Votre plan actuel pourrait être insuffisant pour votre retraite souhaitée.")

# 2. Suggestions de Portefeuille
with tabs[1]:
    st.header("📊 Suggestions de Portefeuille")
    labels = ["Actions canadiennes", "Actions internationales", "Obligations", "Fonds ESG"]
    if profil_data["risque"] == "Faible":
        sizes = [20, 20, 50, 10]
    elif profil_data["risque"] == "Modérée":
        sizes = [35, 35, 20, 10]
    else:
        sizes = [50, 35, 5, 10]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

# 3. Simulateur de Rendement
with tabs[2]:
    st.header("📈 Simulateur de Rendement")
    taux = st.slider("Taux de rendement annuel (%)", 1, 15, 5)
    capital = profil_data["montant_initial"]
    historique = []
    for _ in range(profil_data["duree"]):
        capital = capital * (1 + taux / 100) + 12 * profil_data["investissement_mensuel"]
        historique.append(capital)
    st.line_chart(historique)
    st.metric("Montant estimé à terme", f"{capital:,.2f} $")

# 4. Comparateur de Fonds
with tabs[3]:
    st.header("🔍 Comparateur de Fonds")
    fonds = {
        "VEQT": {"Rendement moyen": "8%", "Risque": "Élevé", "Frais": "0.25%", "Écart-type": "15%", "Description": "Portefeuille mondial 100 % actions"},
        "XEQT": {"Rendement moyen": "7.8%", "Risque": "Élevé", "Frais": "0.20%", "Écart-type": "14.5%", "Description": "FNB tout-en-un actions"},
        "VCNS": {"Rendement moyen": "5%", "Risque": "Faible", "Frais": "0.25%", "Écart-type": "7%", "Description": "Portefeuille conservateur"},
        "VGRO": {"Rendement moyen": "6.5%", "Risque": "Modéré", "Frais": "0.25%", "Écart-type": "10%", "Description": "Portefeuille croissance équilibrée"},
        "ZBAL": {"Rendement moyen": "6%", "Risque": "Modéré", "Frais": "0.22%", "Écart-type": "9%", "Description": "Portefeuille équilibré BMO"},
        "XGRO": {"Rendement moyen": "6.3%", "Risque": "Modéré", "Frais": "0.18%", "Écart-type": "9.5%", "Description": "FNB croissance BlackRock"}
    }
    fond1 = st.selectbox("Choisir un premier fonds", list(fonds.keys()))
    fond2 = st.selectbox("Choisir un deuxième fonds", list(fonds.keys()), index=1)
    st.write(f"### 📌 {fond1}")
    st.json(fonds[fond1])
    st.write(f"### 📌 {fond2}")
    st.json(fonds[fond2])

# 5. Recherche d'Actions
with tabs[4]:
    st.header("📊 Recherche d'Actions")
    logo_col, param_col = st.columns([1, 2])
    with logo_col:
        st.image("https://upload.wikimedia.org/wikipedia/commons/5/56/Yahoo_Finance_logo_2021.svg", width=100)
    with param_col:
        ticker = st.text_input("Entrez le symbole boursier (ex: AAPL, TSLA, MSFT)")
        periode = st.selectbox("Période d'analyse", ["1d", "5d", "1mo", "1y", "5y"], index=3)

    if ticker:
        try:
            data = yf.Ticker(ticker)
            hist = data.history(period=periode)
            info = data.info

            st.subheader(info.get("longName", ticker))
            st.write(f"📈 Prix actuel: ${info.get('currentPrice', 'N/A')}")
            st.write(f"🏢 Secteur: {info.get('sector', 'N/A')}")
            st.write(f"📊 Capitalisation boursière: {info.get('marketCap', 'N/A')}")
            st.line_chart(hist['Close'])
        except Exception:
            st.error("Erreur lors de la récupération des données. Vérifiez le symbole.")

# 6. FAQ
with tabs[5]:
    st.header("❓ Questions fréquentes")
    with st.expander("C'est quoi un ETF?"):
        st.write("Un ETF (Exchange Traded Fund) est un fonds qui regroupe plusieurs actifs.")
    with st.expander("Comment fonctionne le risque?"):
        st.write("Plus le rendement espéré est élevé, plus le risque de pertes est grand.")
    with st.expander("À quelle fréquence investir?"):
        st.write("Investir périodiquement permet de réduire le risque global.")
    with st.expander("Faut-il avoir une épargne d’urgence?"):
        st.write("Oui, c'est essentiel avant tout investissement à long terme.")

# 7. Analyse Technique
with tabs[6]:
    st.header("📉 Analyse Technique")
    symbol = st.text_input("Symbole boursier à analyser", key="tech")
    periode = st.selectbox("Période", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y"], index=4)

    if symbol:
        data = yf.Ticker(symbol)
        df = data.history(period=periode)
        if not df.empty:
            fig, ax = plt.subplots()
            ax.plot(df.index, df['Close'])
            ax.set_title(f"Cours de {symbol} sur {periode}")
            ax.set_ylabel("Prix de clôture")
            st.pyplot(fig)

# 8. Glossaire
with tabs[7]:
    st.header("📘 Glossaire Financier")
    st.markdown("**ETF** : Fonds négocié en bourse, panier d'actifs.")
    st.markdown("**Diversification** : Répartir ses investissements pour limiter les risques.")
    st.markdown("**Rendement** : Gain ou perte généré par un placement.")
    st.markdown("**Frais de gestion** : Coûts associés à la gestion du fonds.")

# 9. Watchlist
with tabs[8]:
    st.header("📝 Watchlist personnalisée")
    liste = st.text_area("Ajouter des symboles boursiers (séparés par des virgules)", "AAPL, MSFT, TSLA")
    if liste:
        tickers = [sym.strip().upper() for sym in liste.split(",")]
        st.write("Votre sélection :", tickers)

# 10. Simulation Monte Carlo
with tabs[9]:
    st.header("🔮 Simulation Monte Carlo")
    nb_sim = st.number_input("Nombre de simulations", min_value=100, max_value=5000, value=500)
    volatilite = st.slider("Volatilité annuelle (%)", 1, 50, 20)
    rendement_moy = st.slider("Rendement moyen (%)", 1, 20, 7)
    resultats = []
    for _ in range(nb_sim):
        capital = profil_data['montant_initial']
        evolution = [capital]
        for _ in range(profil_data['duree']):
            r = np.random.normal(rendement_moy/100, volatilite/100)
            capital *= (1 + r)
            evolution.append(capital)
        resultats.append(evolution)
    fig, ax = plt.subplots()
    for sim in resultats[:50]:
        ax.plot(sim, alpha=0.3)
    st.pyplot(fig)

# 11. Quiz Financier
with tabs[10]:
    st.header("🧠 Quiz Financier")
    questions = [
        {"question": "Quel est l'objectif principal de la diversification ?", "réponses": ["Maximiser les rendements", "Minimiser les risques", "Augmenter les frais"], "bonne": "Minimiser les risques"},
        {"question": "Qu'est-ce qu'un ETF ?", "réponses": ["Un compte bancaire", "Un fonds négocié en bourse", "Un type d'action"], "bonne": "Un fonds négocié en bourse"},
        {"question": "Quel indicateur mesure la volatilité ?", "réponses": ["P/E", "Beta", "ROE"], "bonne": "Beta"}
    ]
    for i, q in enumerate(questions):
        reponse = st.radio(q["question"], q["réponses"], key=f"q{i}")
        if reponse:
            if reponse == q["bonne"]:
                st.success("Bonne réponse!")
            else:
                st.error(f"Mauvaise réponse. La bonne réponse est : {q['bonne']}")

# 12. Cryptomonnaie
with tabs[11]:
    st.header("💰 Cryptomonnaie")
    st.write("La cryptomonnaie est une monnaie numérique sécurisée par cryptographie.")
    st.write("**Bitcoin (BTC)** : La première et la plus célèbre.")
    st.write("**Ethereum (ETH)** : Utilisé pour les contrats intelligents.")
    st.write("**Litecoin (LTC)** : Une alternative plus rapide au Bitcoin.")