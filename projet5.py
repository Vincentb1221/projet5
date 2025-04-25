import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
from datetime import date, timedelta
import plotly.graph_objects as go

# Configuration de la page Streamlit
st.set_page_config(page_title="Conseiller Financier Virtuel", layout="wide")
st.title("💼 Conseiller Financier Virtuel")

# Récupération des tickers clés
tickers = {
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "Dow Jones": "^DJI",
    "Or": "GC=F",
    "Bitcoin": "BTC-USD",
    "US 10Y": "^TNX"
}

# Données en temps réel - version plus robuste
try:
    data = yf.download(list(tickers.values()), period="1d", interval="5m", progress=False, threads=False)
    latest_data = data["Close"].iloc[-1]
    previous_data = data["Close"].iloc[-2]

    st.subheader("📊 Marchés en temps réel")
    cols = st.columns(len(tickers))

    for i, (name, symbol) in enumerate(tickers.items()):
        try:
            latest = latest_data[symbol]
            previous = previous_data[symbol]
            if pd.notna(latest) and pd.notna(previous):
                delta = round(((latest - previous) / previous) * 100, 2)
                cols[i].metric(label=name, value=f"${latest:,.2f}", delta=f"{delta}%")
            else:
                cols[i].metric(label=name, value="N/A", delta="N/A")
        except Exception:
            cols[i].metric(label=name, value="Erreur", delta="")

except Exception as e:
    st.error(f"Erreur lors de la récupération des données financières : {e}")

# Variables par défaut pour éviter les erreurs si le formulaire n'est pas soumis
age = 30
objectif = "Épargne retraite"
montant_initial = 1000
investissement_mensuel = 100
duree = 10
connaissance = "Débutant"
risque = "Modérée"
situation_familiale = "Célibataire"
epargne_urgence = "Oui"
preference_esg = False
horizon_liquidite = "Non"

# Onglets
tabs = st.tabs([
    "Profil Financier",
    "Suggestions de Portefeuille",
    "Simulateur de Rendement",
    "Comparateur de Fonds",
    "Recherche d'Actions",
    "FAQ",
    "Analyse Technique",
    "Glossaire",
    "Watchlist",
    "Simulation Monte Carlo",
    "Quiz Financier",
    "Cryptomonnaie"
])

# 1. Profil Financier
with tabs[0]:
    st.header("📋 Profil Financier")
    with st.form("profil_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Âge", min_value=18, max_value=100, value=30)
            objectif = st.selectbox("Objectif d'investissement", ["Épargne retraite", "Achat maison", "Voyage", "Revenus passifs", "Autre"])
            montant_initial = st.number_input("Montant disponible à investir maintenant ($)", min_value=0)
            investissement_mensuel = st.number_input("Montant investi chaque mois ($)", min_value=0)
            duree = st.slider("Durée de l'investissement (en années)", 1, 50, 10)
            connaissance = st.select_slider("Connaissances en finance", options=["Débutant", "Intermédiaire", "Avancé"])
        with col2:
            risque = st.select_slider("Tolérance au risque", options=["Faible", "Modérée", "Élevée"])
            situation_familiale = st.selectbox("Situation familiale", ["Célibataire", "Marié(e)", "Avec enfants", "Sans enfants"])
            epargne_urgence = st.radio("Avez-vous une épargne d'urgence?", ["Oui", "Non"])
            preference_esg = st.checkbox("Je préfère des investissements responsables (ESG)")
            horizon_liquidite = st.radio("Avez-vous besoin de liquidité à court terme?", ["Oui", "Non"])

        submitted = st.form_submit_button("Analyser mon profil")

    if submitted:
        st.success("✅ Profil analysé avec succès!")
        st.write("### Résumé de votre profil :")
        st.json({
            "Âge": age,
            "Objectif": objectif,
            "Montant initial": montant_initial,
            "Investissement mensuel": investissement_mensuel,
            "Durée": duree,
            "Tolérance au risque": risque,
            "Situation familiale": situation_familiale,
            "Épargne d'urgence": epargne_urgence,
            "Préférence ESG": preference_esg,
            "Connaissances financières": connaissance,
            "Besoin de liquidité court terme": horizon_liquidite
        })

# 2. Suggestions de Portefeuille
with tabs[1]:
    st.header("📊 Suggestions de Portefeuille")
    st.markdown("Voici un exemple de répartition suggérée basée sur votre profil :")

    labels = ["Actions canadiennes", "Actions internationales", "Obligations", "Fonds ESG", "Liquidité"]

    # Étape 1: Base selon l’objectif
    if objectif == "Épargne retraite":
        sizes = [30, 30, 30, 0, 10]
    elif objectif == "Achat maison":
        sizes = [20, 20, 40, 0, 20]
    elif objectif == "Voyage":
        sizes = [25, 25, 30, 0, 20]
    elif objectif == "Revenus passifs":
        sizes = [20, 20, 50, 0, 10]
    else:  # Autre
        sizes = [25, 25, 25, 0, 25]

    # Étape 2: Ajustement par la tolérance au risque
    if risque == "Faible":
        sizes[0] -= 5  # Moins d'actions canadiennes
        sizes[1] -= 5
        sizes[2] += 10  # Plus d'obligations
    elif risque == "Élevée":
        sizes[0] += 5
        sizes[1] += 5
        sizes[2] -= 10

    # Étape 3: Ajustement par la durée
    if duree <= 5:
        sizes[2] += 10  # Plus d'obligations à court terme
        sizes[0] -= 5
        sizes[1] -= 5
    elif duree >= 15:
        sizes[0] += 5
        sizes[1] += 5
        sizes[2] -= 10

    # Étape 4: Préférence ESG
    if preference_esg:
        esg_transfer = min(sizes[0], 10)  # max 10% transféré
        sizes[0] -= esg_transfer // 2
        sizes[1] -= esg_transfer // 2
        sizes[3] += esg_transfer  # Fonds ESG

    # Étape 5: Liquidité à court terme
    if horizon_liquidite == "Oui":
        liquidite_boost = 10
        # Réduction équilibrée ailleurs
        reduction = liquidite_boost // 3
        sizes[0] -= reduction
        sizes[1] -= reduction
        sizes[2] -= reduction
        sizes[4] += liquidite_boost

    # Normalisation (juste au cas où les tailles dépassent 100 ou sont < 0)
    total = sum(sizes)
    sizes = [round(s / total * 100) for s in sizes]

    # Affichage du graphique
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # Résumé explicatif
    st.markdown("### 📝 Explication personnalisée de la répartition")

    explication = []

    # Objectif
    if objectif == "Épargne retraite":
        explication.append("Votre objectif d'épargne retraite favorise une croissance à long terme, d'où une part importante en actions et une diversification équilibrée.")
    elif objectif == "Achat maison":
        explication.append("L'achat d'une maison implique un horizon de placement plus court, donc davantage d'obligations et de liquidités pour sécuriser votre capital.")
    elif objectif == "Voyage":
        explication.append("Un projet de voyage nécessite des fonds disponibles sous peu, donc plus de liquidités et d'actifs à faible risque.")
    elif objectif == "Revenus passifs":
        explication.append("Vous cherchez à générer des revenus réguliers, les obligations occupent donc une place centrale dans votre portefeuille.")
    else:
        explication.append("Votre objectif général a mené à une répartition équilibrée entre croissance, revenu et sécurité.")

    # Tolérance au risque
    if risque == "Faible":
        explication.append("Votre faible tolérance au risque a réduit l'exposition aux actions et renforcé les actifs stables comme les obligations.")
    elif risque == "Modérée":
        explication.append("Votre profil modéré combine actions et obligations pour équilibrer rendement et sécurité.")
    elif risque == "Élevée":
        explication.append("Votre tolérance élevée au risque augmente l'exposition aux actions pour maximiser le potentiel de rendement.")

    # Durée
    if duree <= 5:
        explication.append("Comme votre horizon de placement est court, la priorité a été mise sur des actifs plus sécuritaires.")
    elif duree >= 15:
        explication.append("Avec un horizon à long terme, le portefeuille favorise les actions pour maximiser le rendement dans le temps.")

    # ESG
    if preference_esg:
        explication.append("Votre préférence pour les investissements responsables a conduit à une réallocation vers des fonds ESG.")

    # Liquidité
    if horizon_liquidite == "Oui":
        explication.append("Comme vous avez besoin de liquidités à court terme, une part plus importante a été allouée à des actifs très accessibles.")

    st.markdown("<br>".join(explication), unsafe_allow_html=True)

# 3. Simulateur de Rendement
with tabs[2]:
    st.header("📈 Simulateur de Rendement")
    taux = st.slider("Taux de rendement annuel (%)", 1, 15, 5)
    capital = montant_initial
    historique = []
    for annee in range(duree):
        capital = capital * (1 + taux / 100) + 12 * investissement_mensuel
        historique.append(capital)

    st.line_chart(historique)
    st.metric("Montant estimé à terme", f"{capital:,.2f} $")

# 4. Comparateur de Fonds
with tabs[3]:
    # Charger les tickers depuis le fichier CSV
    fnb_df = pd.read_csv("fnb_americains.csv")
    tickers = fnb_df["ticker"].tolist()

    # Section Streamlit
    st.header("🔍 Comparateur de FNB Américains")

    col1, col2 = st.columns(2)
    with col1:
        fond1 = st.selectbox("Choisir le premier FNB", tickers, key="fond1")
    with col2:
        fond2 = st.selectbox("Choisir le deuxième FNB", tickers, key="fond2", index=1)

    # Fonction pour extraire les données financières de base
    def extraire_infos(ticker):
        try:
            fnb = yf.Ticker(ticker)
            info = fnb.info

            return {
                "Nom complet": info.get("longName", "N/A"),
                "Symbole": info.get("symbol", "N/A"),
                "Catégorie": info.get("category", "N/A"),
                "Frais de gestion (%)": f"{info.get('expenseRatio', 0) * 100:.2f}%" if info.get('expenseRatio') else "N/A",
                "Actif net (G$)": f"{info.get('totalAssets', 0) / 1e9:.2f}" if info.get('totalAssets') else "N/A",
                "Rendement 1 an (%)": f"{info.get('threeYearAverageReturn', 0) * 100:.2f}%" if info.get('threeYearAverageReturn') else "N/A",
            }
        except Exception as e:
            return {"Nom complet": "Erreur", "Symbole": ticker}

    # Extraire les infos pour chaque fonds sélectionné
    data_fond1 = extraire_infos(fond1)
    data_fond2 = extraire_infos(fond2)

    # Créer un tableau comparatif
    comparaison = pd.DataFrame({
        "Paramètre": list(data_fond1.keys()),
        fond1: list(data_fond1.values()),
        fond2: list(data_fond2.values())
    })

    st.subheader("📊 Tableau comparatif")
    st.dataframe(comparaison, use_container_width=True)

# 5. Recherche d'Actions
with tabs[4]:
    st.header("📊 Recherche d'Actions")

    # Liste des 500 actions du S&P500
    sp500_df = pd.read_csv("tickers_sp500.csv")
       
    col1, col2 = st.columns(2)
    with col1:
        ticker = st.selectbox("Choisissez un ticker du S&P 500", sp500_df)

    with col2:
        periode = st.selectbox("Période à afficher", ["1mo", "6mo", "1y", "5y", "max"], index=2)

    if ticker:
        try:
            data = yf.Ticker(ticker)
            info = data.info
            hist = data.history(period=periode)

            st.subheader(info.get("longName", ticker))
            st.write(f"📈 Prix actuel : ${info.get('currentPrice', 'N/A')}")
            st.write(f"🏢 Secteur : {info.get('sector', 'N/A')}")
            st.write(f"📊 Capitalisation boursière : {info.get('marketCap', 'N/A'):,}")
            st.write(f"💰 Dividende : {info.get('dividendYield', 'N/A')}")
            st.write(f"🔍 Description : {info.get('longBusinessSummary', 'N/A')}")

            # Affichage du graphique de l’évolution des prix
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hist.index, y=hist["Close"], mode="lines", name="Prix de clôture"))
            fig.update_layout(title=f"Évolution du prix - {ticker}", xaxis_title="Date", yaxis_title="Prix ($)", height=400)
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Erreur lors de la récupération des données : {e}")

# 6. FAQ
with tabs[5]:
    st.header("❓ Questions fréquentes")
    with st.expander("C'est quoi un ETF?"):
        st.write("Un ETF (Exchange Traded Fund) est un fonds qui regroupe plusieurs actifs, comme des actions ou des obligations, et qui se transige en bourse comme une action.")
    with st.expander("Comment fonctionne le risque?"):
        st.write("Plus le rendement espéré est élevé, plus le risque de pertes est grand.")
    with st.expander("À quelle fréquence investir?"):
        st.write("Investir de manière périodique (ex: chaque mois) permet de réduire le risque.")
    with st.expander("Faut-il avoir une épargne d’urgence?"):
        st.write("Oui, avant d’investir à long terme, il est important d’avoir un coussin de sécurité.")

# 7. Analyse Technique
with tabs[6]:
    st.header("📉 Analyse Technique")

    st.info("Sélectionnez un actif et une plage de dates pour afficher son graphique technique.")

    try:
        sp500_df = pd.read_csv("tickers_sp500.csv")
        ticker = st.selectbox("Choisissez un ticker", sp500_df.squeeze().tolist())
    except Exception as e:
        st.error(f"Erreur lors du chargement des tickers : {e}")
        st.stop()

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Date de début", date.today() - timedelta(days=180))
    with col2:
        end_date = st.date_input("Date de fin", date.today())

    show_sma = st.checkbox("Afficher la moyenne mobile (SMA 20)", value=True)
    show_rsi = st.checkbox("Afficher le RSI (14)")
    show_macd = st.checkbox("Afficher le MACD")

    if start_date < end_date:
        df = yf.download(ticker, start=start_date, end=end_date)

        if not df.empty:
            # Calcul des indicateurs techniques
            df['SMA20'] = df['Close'].rolling(window=20).mean()

            try:
                delta = df['Close'].diff()
                gain = delta.copy()
                gain[delta < 0] = 0
                loss = -delta.copy()
                loss[delta > 0] = 0
                avg_gain = gain.rolling(window=14).mean()
                avg_loss = loss.rolling(window=14).mean()
                rs = avg_gain / avg_loss
                df['RSI'] = 100 - (100 / (1 + rs))
            except Exception as e:
                st.warning(f"RSI non calculé : {e}")

            df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
            df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = df['EMA12'] - df['EMA26']
            df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

            # --------- GRAPHIQUE PRINCIPAL -----------
            fig = go.Figure()

            # Ajout des chandeliers toujours
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'],
                name='Chandeliers'
            ))

            # Ajout conditionnel de la SMA
            if show_sma:
                fig.add_trace(go.Scatter(
                    x=df.index, y=df['SMA20'],
                    line=dict(color='blue', width=1),
                    name='SMA 20'
                ))

            # Ajout du volume (toujours pour embellir)
            fig.add_trace(go.Bar(
                x=df.index, y=df['Volume'],
                name='Volume',
                marker_opacity=0.3,
                yaxis='y2'
            ))

            # Layout
            fig.update_layout(
                title=f"Graphique de {ticker} - Chandeliers & Indicateurs",
                xaxis_rangeslider_visible=False,
                yaxis=dict(title="Prix ($)"),
                yaxis2=dict(title="Volume", overlaying='y', side='right', showgrid=False),
                height=600
            )

            st.plotly_chart(fig, use_container_width=True)

            # --------- GRAPHIQUE RSI -----------
            if show_rsi and 'RSI' in df:
                rsi_fig = go.Figure()
                rsi_fig.add_trace(go.Scatter(
                    x=df.index, y=df['RSI'],
                    line=dict(color='orange'), name='RSI'
                ))
                rsi_fig.update_layout(title="RSI (14)", yaxis_range=[0, 100], height=200)
                st.plotly_chart(rsi_fig, use_container_width=True)

            # --------- GRAPHIQUE MACD -----------
            if show_macd:
                macd_fig = go.Figure()
                macd_fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name="MACD", line=dict(color="green")))
                macd_fig.add_trace(go.Scatter(x=df.index, y=df['Signal'], name="Signal", line=dict(color="red")))
                macd_fig.update_layout(title="MACD", height=200)
                st.plotly_chart(macd_fig, use_container_width=True)

        else:
            st.warning("Aucune donnée disponible pour cette période.")
    else:
        st.error("La date de début doit être antérieure à la date de fin.")


# 8. Glossaire
with tabs[7]:
    st.header("\U0001F4D8 Glossaire Financier")

    st.markdown("**ETF** : Fonds négocié en bourse, panier d'actifs transigé comme une action.")
    st.markdown("**Fonds indiciel** : Réplique la performance d'un indice (ex : S&P 500).")
    st.markdown("**Diversification** : Répartir ses placements pour limiter les risques.")
    st.markdown("**Rendement** : Gain ou perte sur un investissement.")
    st.markdown("**Frais de gestion** : Coûts annuels d'un fonds, en pourcentage.")
    st.markdown("**Volatilité** : Mesure des variations de prix d’un actif sur une période donnée.")
    st.markdown("**Liquidité** : Facilité avec laquelle un actif peut être acheté ou vendu rapidement.")
    st.markdown("**Ratio cours/bénéfice (P/E)** : Rapport entre le prix d’une action et le bénéfice par action.")
    st.markdown("**Dividende** : Part des profits versée aux actionnaires.")
    st.markdown("**Capitalisation boursière** : Valeur totale de toutes les actions en circulation d’une entreprise.")
    st.markdown("**Alpha** : Surperformance d’un investissement par rapport à un indice de référence.")
    st.markdown("**Bêta** : Sensibilité d’un actif par rapport aux mouvements du marché.")
    st.markdown("**Ratio de Sharpe** : Mesure du rendement ajusté au risque d’un portefeuille.")
    st.markdown("**Obligation** : Instrument de dette émis par un gouvernement ou une entreprise pour emprunter des fonds.")
    st.markdown("**Action** : Titre représentant une part de propriété dans une entreprise.")
    st.markdown("**Portefeuille** : Ensemble des actifs détenus par un investisseur.")
    st.markdown("**Horizon de placement** : Durée pendant laquelle un investisseur prévoit de détenir un actif.")
    st.markdown("**SMA (Simple Moving Average)** : Moyenne des prix de clôture sur une période donnée, utilisée pour lisser les tendances.")
    st.markdown("**RSI (Relative Strength Index)** : Indicateur de momentum qui mesure la vitesse et le changement des mouvements de prix, sur une échelle de 0 à 100.")
    st.markdown("**MACD (Moving Average Convergence Divergence)** : Indicateur de suivi de tendance basé sur la différence entre deux moyennes mobiles exponentielles.")


# 9. Watchlist
with tabs[8]:
    st.header("\U0001F4DD Ma Watchlist")

    watchlist_input = st.text_area("Ajouter des actions à suivre (séparées par des virgules)", "")
    if watchlist_input:
        actions = [action.strip().upper() for action in watchlist_input.split(",") if action.strip()]
        st.write("### Liste de suivi :")
        st.write(", ".join(actions))

        # Export CSV
        df_watchlist = pd.DataFrame(actions, columns=["Ticker"])
        csv = df_watchlist.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger en CSV",
            data=csv,
            file_name='ma_watchlist.csv',
            mime='text/csv'
        )
    else:
        st.info("Ajoutez des tickers pour créer votre liste de suivi.")


# 10. Simulation Monte Carlo
with tabs[9]:
    st.header("🔮 Simulation Monte Carlo")
    st.markdown("Simulez des rendements futurs pour vos investissements.")

    num_simulations = st.number_input("Nombre de simulations", min_value=100, max_value=10000, value=1000)
    volatilite = st.slider("Volatilité (%)", min_value=1, max_value=50, value=20)
    rendement_moyen = st.slider("Rendement moyen annuel (%)", min_value=1, max_value=20, value=8)

    simulation_results = []
    for _ in range(num_simulations):
        capital_final = montant_initial
        historique_simulation = [capital_final]
        for _ in range(duree):
            rendement = np.random.normal(rendement_moyen / 100, volatilite / 100)
            capital_final *= (1 + rendement)
            historique_simulation.append(capital_final)
        simulation_results.append(historique_simulation)

    fig, ax = plt.subplots()
    for simulation in simulation_results[:50]:
        ax.plot(simulation, alpha=0.3)
    st.pyplot(fig)

# 11. Quiz Financier
with tabs[10]:
    st.header("\U0001F9E0 Quiz Financier")

    questions = [
        {
            "question": "Quel est l'objectif principal de la diversification ?",
            "options": ["Maximiser les rendements", "Minimiser les risques", "Augmenter les frais"],
            "answer": "Minimiser les risques"
        },
        {
            "question": "Le ratio cours/bénéfice (P/E) mesure :",
            "options": ["La rentabilité d'une entreprise", "La volatilité d'une action", "Le prix d'une action par rapport à ses bénéfices"],
            "answer": "Le prix d'une action par rapport à ses bénéfices"
        },
        {
            "question": "Un ETF est :",
            "options": ["Une obligation d'État", "Un fonds négocié en bourse", "Une entreprise technologique"],
            "answer": "Un fonds négocié en bourse"
        },
        {
            "question": "Le RSI est un indicateur de :",
            "options": ["Liquidité", "Momentum", "Croissance"],
            "answer": "Momentum"
        },
        {
            "question": "Quel indicateur aide à détecter les croisements de tendance ?",
            "options": ["RSI", "MACD", "P/E"],
            "answer": "MACD"
        }
    ]

    correct_answers = 0

    for i, q in enumerate(questions):
        st.subheader(f"Question {i+1}")
        response = st.radio(q["question"], q["options"], key=f"q{i}")

        if response:
            if response == q["answer"]:
                st.success("Bonne réponse!")
                correct_answers += 1
            else:
                st.error(f"Mauvaise réponse. La bonne réponse est : {q['answer']}")

    if len(questions) > 0:
        st.markdown(f"### Résultat : {correct_answers} / {len(questions)} bonnes réponses")

# 12. Cryptomonnaie
with tabs[11]:
    st.header("💰 Cryptomonnaie")
    st.write("""
    La cryptomonnaie est une monnaie numérique sécurisée par cryptographie. 
    Exemples populaires : Bitcoin (BTC), Ethereum (ETH), Litecoin (LTC).
    """)
    st.write("**Bitcoin (BTC)** : La première et la plus célèbre des cryptomonnaies.")
    st.write("**Ethereum (ETH)** : Utilisé pour des applications décentralisées.")
    st.write("**Litecoin (LTC)** : Une alternative plus rapide au Bitcoin.")