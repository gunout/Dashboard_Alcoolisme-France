import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Alcool France - Analyse Stratégique",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(45deg, #8B4513, #D2691E, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        padding: 1rem;
    }
    .section-header {
        color: #8B4513;
        border-bottom: 3px solid #D2691E;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-size: 1.8rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .impact-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid;
    }
    .impact-health { border-left-color: #dc3545; background-color: rgba(220, 53, 69, 0.1); }
    .impact-economic { border-left-color: #28a745; background-color: rgba(40, 167, 69, 0.1); }
    .impact-social { border-left-color: #ffc107; background-color: rgba(255, 193, 7, 0.1); }
    .policy-card {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    .policy-prevention { border-left-color: #28a745; background-color: rgba(40, 167, 69, 0.1); }
    .policy-tax { border-left-color: #007bff; background-color: rgba(0, 123, 255, 0.1); }
    .policy-regulation { border-left-color: #6f42c1; background-color: rgba(111, 66, 193, 0.1); }
    .policy-ban { border-left-color: #dc3545; background-color: rgba(220, 53, 69, 0.1); }
</style>
""", unsafe_allow_html=True)

class AlcoholDashboard:
    def __init__(self):
        self.historical_data = self.initialize_historical_data()
        self.policy_timeline = self.initialize_policy_timeline()
        self.regional_data = self.initialize_regional_data()
        self.international_comparison = self.initialize_international_comparison()
        self.health_impact_data = self.initialize_health_impact_data()
        
    def initialize_historical_data(self):
        """Initialise les données historiques de la consommation d'alcool"""
        years = list(range(2000, 2024))
        
        # Données simulées basées sur les tendances historiques réelles
        alcohol_consumption = [
            13.5, 13.2, 12.9, 12.6, 12.3, 12.0, 11.8, 11.5, 11.3, 11.1,  # 2000-2009 (litres/personne/an)
            10.9, 10.7, 10.5, 10.3, 10.1, 9.9, 9.7, 9.5, 9.3, 9.1,  # 2010-2019
            8.9, 8.7, 8.5, 8.3  # 2020-2023
        ]
        
        daily_drinkers = [
            15.2, 14.8, 14.4, 14.0, 13.6, 13.2, 12.8, 12.4, 12.0, 11.6,  # 2000-2009 (% population)
            11.2, 10.8, 10.4, 10.0, 9.6, 9.2, 8.8, 8.4, 8.0, 7.6,  # 2010-2019
            7.2, 6.8, 6.4, 6.0  # 2020-2023
        ]
        
        binge_drinking = [
            18.5, 18.8, 19.1, 19.4, 19.7, 20.0, 20.3, 20.6, 20.9, 21.2,  # 2000-2009 (% population)
            21.5, 21.8, 22.1, 22.4, 22.7, 23.0, 23.3, 23.6, 23.9, 24.2,  # 2010-2019
            24.5, 24.8, 25.1, 25.4  # 2020-2023
        ]
        
        wine_consumption = [
            58.2, 56.8, 55.5, 54.2, 52.9, 51.6, 50.3, 49.0, 47.7, 46.4,  # 2000-2009 (% consommation totale)
            45.1, 43.8, 42.5, 41.2, 39.9, 38.6, 37.3, 36.0, 34.7, 33.4,  # 2010-2019
            32.1, 30.8, 29.5, 28.2  # 2020-2023
        ]
        
        tax_revenue = [
            3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1,  # 2000-2009 (milliards €)
            4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1,  # 2010-2019
            5.2, 5.3, 5.4, 5.5  # 2020-2023
        ]
        
        return pd.DataFrame({
            'annee': years,
            'consommation_alcool': alcohol_consumption,
            'buveurs_quotidiens': daily_drinkers,
            'binge_drinking': binge_drinking,
            'part_vin': wine_consumption,
            'recettes_fiscales': tax_revenue
        })
    
    def initialize_policy_timeline(self):
        """Initialise la timeline des politiques sur l'alcool"""
        return [
            {'date': '1991-01-01', 'type': 'regulation', 'titre': 'Loi Évin - Alcool', 
             'description': 'Encadrement de la publicité pour les boissons alcoolisées'},
            {'date': '2009-07-21', 'type': 'ban', 'titre': 'Loi Bachelot', 
             'description': 'Interdiction de la vente d\'alcool aux mineurs et limitation de la publicité'},
            {'date': '2015-01-01', 'type': 'regulation', 'titre': 'Alcootest obligatoire', 
             'description': 'Obligation de posséder un éthylotest dans tous les véhicules'},
            {'date': '2016-01-01', 'type': 'tax', 'titre': 'Augmentation des taxes', 
             'description': 'Hausse des taxes sur les boissons alcoolisées'},
            {'date': '2018-03-01', 'type': 'prevention', 'titre': 'Campagne "Avec modération"', 
             'description': 'Lancement des campagnes nationales de prévention'},
            {'date': '2019-07-22', 'type': 'regulation', 'titre': 'Loi Santé', 
             'description': 'Renforcement de l\'encadrement de la publicité pour l\'alcool'},
            {'date': '2020-01-01', 'type': 'prevention', 'titre': 'Programme "Alcool Info Service"', 
             'description': 'Renforcement des services d\'aide et d\'information'},
            {'date': '2021-11-01', 'type': 'regulation', 'titre': 'Interdiction publicité réseaux sociaux', 
             'description': 'Interdiction de la publicité pour l\'alcool sur les réseaux sociaux'},
            {'date': '2023-01-01', 'type': 'tax', 'titre': 'Nouvelle hausse des taxes', 
             'description': 'Augmentation ciblée sur les boissons les plus consommées'},
        ]
    
    def initialize_regional_data(self):
        """Initialise les données régionales de consommation"""
        regions = [
            'Île-de-France', 'Auvergne-Rhône-Alpes', 'Nouvelle-Aquitaine', 
            'Occitanie', 'Hauts-de-France', 'Provence-Alpes-Côte d\'Azur',
            'Pays de la Loire', 'Bretagne', 'Normandie', 'Grand Est',
            'Bourgogne-Franche-Comté', 'Centre-Val de Loire', 'Corse'
        ]
        
        data = {
            'region': regions,
            'consommation_2023': [7.8, 9.2, 8.9, 9.5, 10.1, 8.4, 8.1, 9.8, 8.7, 9.4, 8.6, 8.3, 11.2],
            'evolution_2010_2023': [-2.1, -1.8, -1.9, -2.2, -1.5, -2.0, -2.3, -1.7, -1.8, -1.6, -2.1, -2.0, -0.9],
            'buveurs_quotidiens': [4.2, 6.8, 6.1, 7.2, 8.5, 5.3, 4.9, 7.9, 6.4, 7.1, 6.2, 5.8, 9.8],
            'binge_drinking': [22.1, 25.6, 24.8, 26.3, 28.7, 23.4, 21.9, 27.2, 25.1, 26.8, 24.5, 23.2, 30.5]
        }
        
        return pd.DataFrame(data)
    
    def initialize_international_comparison(self):
        """Initialise les données comparatives internationales"""
        countries = ['France', 'Allemagne', 'Royaume-Uni', 'Espagne', 'Italie', 'États-Unis', 'Russie', 'Japon']
        
        data = {
            'pays': countries,
            'consommation_alcool': [8.3, 10.6, 9.8, 7.5, 6.9, 8.9, 11.7, 7.2],
            'prix_biere_eur': [2.5, 1.8, 3.2, 1.2, 1.5, 2.8, 1.1, 3.5],
            'mortalite_liee_alcool': [41, 79, 52, 28, 35, 88, 152, 23],  # milliers
            'depenses_prevention': [0.4, 0.3, 0.8, 0.2, 0.3, 1.2, 0.1, 0.5],  # € par habitant
            'age_legal_consommation': [18, 16, 18, 18, 18, 21, 18, 20]
        }
        
        return pd.DataFrame(data)
    
    def initialize_health_impact_data(self):
        """Initialise les données d'impact sur la santé"""
        years = list(range(2010, 2024))
        
        data = {
            'annee': years,
            'deces_alcool': [49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36],  # milliers
            'cancers_digesifs': [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],  # milliers
            'maladies_foie': [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0.9, 0.8],  # milliers
            'couts_sante': [18.5, 18.8, 19.1, 19.4, 19.7, 20.0, 20.3, 20.6, 20.9, 21.2, 21.5, 21.8, 22.1, 22.4],  # milliards €
            'accidents_routiers': [3.2, 3.0, 2.8, 2.6, 2.4, 2.2, 2.0, 1.8, 1.6, 1.4, 1.2, 1.0, 0.8, 0.6]  # milliers
        }
        
        return pd.DataFrame(data)
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown(
            '<h1 class="main-header">🍷 DASHBOARD STRATÉGIQUE - ALCOOL EN FRANCE</h1>', 
            unsafe_allow_html=True
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                '<div style="text-align: center; background: linear-gradient(45deg, #8B4513, #D2691E); '
                'color: white; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">'
                '<h3>📊 ANALYSE DE LA CONSOMMATION, POLITIQUES ET IMPACTS SANITAIRES</h3>'
                '</div>', 
                unsafe_allow_html=True
            )
        
        current_time = datetime.now().strftime('%H:%M:%S')
        st.sidebar.markdown(f"**🕐 Dernière mise à jour: {current_time}**")
    
    def display_key_metrics(self):
        """Affiche les métriques clés de l'alcool en France"""
        st.markdown('<h3 class="section-header">📊 INDICATEURS CLÉS DE L\'ALCOOL EN FRANCE</h3>', 
                   unsafe_allow_html=True)
        
        current_data = self.historical_data[self.historical_data['annee'] == 2023].iloc[0]
        previous_data = self.historical_data[self.historical_data['annee'] == 2022].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Consommation d'alcool",
                f"{current_data['consommation_alcool']:.1f}L/pers/an",
                f"{(current_data['consommation_alcool'] - previous_data['consommation_alcool']):+.1f}L vs 2022",
                delta_color="inverse"
            )
        
        with col2:
            st.metric(
                "Buveurs Quotidiens",
                f"{current_data['buveurs_quotidiens']:.1f}%",
                f"{(current_data['buveurs_quotidiens'] - previous_data['buveurs_quotidiens']):+.1f}% vs 2022",
                delta_color="inverse"
            )
        
        with col3:
            st.metric(
                "Binge Drinking",
                f"{current_data['binge_drinking']:.1f}%",
                f"{(current_data['binge_drinking'] - previous_data['binge_drinking']):+.1f}% vs 2022",
                delta_color="inverse"
            )
        
        with col4:
            st.metric(
                "Recettes Fiscales",
                f"{current_data['recettes_fiscales']:.1f}Md€",
                f"{(current_data['recettes_fiscales'] - previous_data['recettes_fiscales']):+.1f}Md€ vs 2022"
            )
    
    def create_historical_analysis(self):
        """Crée l'analyse historique de la consommation"""
        st.markdown('<h3 class="section-header">📈 ÉVOLUTION HISTORIQUE DE LA CONSOMMATION</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Consommation", "Types de Consommateurs", "Impact Santé"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution de la consommation
                fig = px.line(self.historical_data, 
                             x='annee', 
                             y='consommation_alcool',
                             title='Évolution de la Consommation d\'Alcool (litres/personne/an) - 2000-2023',
                             markers=True)
                fig.update_layout(yaxis_title="Litres d'alcool pur/pers/an", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Part du vin dans la consommation
                fig = px.area(self.historical_data, 
                             x='annee', 
                             y='part_vin',
                             title='Part du Vin dans la Consommation Totale (%) - 2000-2023')
                fig.update_layout(yaxis_title="Part du vin (%)", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Buveurs quotidiens vs occasionnels
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=self.historical_data['annee'], 
                                       y=self.historical_data['buveurs_quotidiens'],
                                       name='Buveurs quotidiens',
                                       line=dict(color='brown')))
                
                fig.update_layout(title='Évolution des Buveurs Quotidiens',
                                yaxis_title="Pourcentage (%)", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Binge drinking
                fig = px.line(self.historical_data, 
                             x='annee', 
                             y='binge_drinking',
                             title='Évolution du Binge Drinking (%) - 2000-2023',
                             markers=True)
                fig.update_layout(yaxis_title="Binge drinking (%)", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Impact sur la santé
                fig = px.line(self.health_impact_data, 
                             x='annee', 
                             y=['deces_alcool', 'cancers_digesifs', 'maladies_foie'],
                             title='Mortalité Liée à l\'Alcool (milliers) - 2010-2023',
                             markers=True)
                fig.update_layout(yaxis_title="Nombre de décès (milliers)", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Coûts sanitaires
                fig = px.area(self.health_impact_data, 
                             x='annee', 
                             y='couts_sante',
                             title='Coûts Sanitaires Liés à l\'Alcool (milliards €) - 2010-2023')
                fig.update_layout(yaxis_title="Coûts (milliards €)", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
    
    def create_policy_analysis(self):
        """Analyse des politiques sur l'alcool"""
        st.markdown('<h3 class="section-header">🏛️ ANALYSE DES POLITIQUES SUR L\'ALCOOL</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Timeline des Politiques", "Impact des Mesures", "Efficacité Comparée"])
        
        with tab1:
            # Timeline interactive des politiques
            policy_df = pd.DataFrame(self.policy_timeline)
            policy_df['date'] = pd.to_datetime(policy_df['date'])
            policy_df['annee'] = policy_df['date'].dt.year
            
            # Fusion avec données historiques
            merged_data = pd.merge(self.historical_data, policy_df, on='annee', how='left')
            
            fig = px.scatter(merged_data, 
                           x='annee', 
                           y='consommation_alcool',
                           color='type',
                           size_max=20,
                           hover_name='titre',
                           hover_data={'description': True, 'type': True},
                           title='Impact des Politiques sur la Consommation d\'Alcool')
            
            # Ajouter la ligne de tendance
            fig.add_trace(go.Scatter(x=self.historical_data['annee'], 
                                   y=self.historical_data['consommation_alcool'],
                                   mode='lines',
                                   name='Consommation alcool',
                                   line=dict(color='gray', width=2)))
            
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
            
            # Légende des types de politiques
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown('<div class="policy-card policy-prevention">Prévention</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="policy-card policy-tax">Fiscalité</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="policy-card policy-regulation">Réglementation</div>', unsafe_allow_html=True)
            with col4:
                st.markdown('<div class="policy-card policy-ban">Interdiction</div>', unsafe_allow_html=True)
        
        with tab2:
            # Analyse d'impact des politiques majeures
            st.subheader("Impact des Politiques Clés")
            
            impact_analysis = [
                {'politique': 'Loi Évin (1991)', 'impact_consommation': -0.8, 'delai_impact': 3},
                {'politique': 'Loi Bachelot (2009)', 'impact_consommation': -0.5, 'delai_impact': 2},
                {'politique': 'Alcootest obligatoire (2015)', 'impact_consommation': -0.3, 'delai_impact': 1},
                {'politique': 'Hausse taxes 2016', 'impact_consommation': -0.4, 'delai_impact': 2},
                {'politique': 'Campagne modération (2018)', 'impact_consommation': -0.2, 'delai_impact': 1},
            ]
            
            impact_df = pd.DataFrame(impact_analysis)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(impact_df, 
                            x='politique', 
                            y='impact_consommation',
                            title='Impact sur la Consommation (litres/pers/an)',
                            color='impact_consommation',
                            color_continuous_scale='RdYlGn')
                fig.update_layout(xaxis_tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # CORRECTION : Utiliser la valeur absolue pour la taille
                impact_df['impact_absolu'] = impact_df['impact_consommation'].abs()
                
                fig = px.scatter(impact_df, 
                               x='delai_impact', 
                               y='impact_consommation',
                               size='impact_absolu',  # Utiliser les valeurs absolues
                               color='politique',
                               hover_name='politique',
                               title='Délai vs Amplitude des Impacts',
                               size_max=30)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Efficacité comparée des politiques
            st.subheader("Efficacité des Différentes Stratégies")
            
            strategies = [
                {'strategie': 'Augmentation des prix', 'efficacite': 8.2, 'cout': 3, 'acceptabilite': 4},
                {'strategie': 'Limitation publicité', 'efficacite': 6.8, 'cout': 2, 'acceptabilite': 7},
                {'strategie': 'Contrôles routiers', 'efficacite': 7.5, 'cout': 4, 'acceptabilite': 6},
                {'strategie': 'Interdiction vente mineurs', 'efficacite': 6.2, 'cout': 2, 'acceptabilite': 8},
                {'strategie': 'Campagnes prévention', 'efficacite': 5.8, 'cout': 5, 'acceptabilite': 9},
                {'strategie': 'Services d\'aide', 'efficacite': 6.5, 'cout': 6, 'acceptabilite': 8},
            ]
            
            strategy_df = pd.DataFrame(strategies)
            
            fig = px.scatter(strategy_df, 
                           x='cout', 
                           y='efficacite',
                           size='acceptabilite',
                           color='strategie',
                           hover_name='strategie',
                           title='Efficacité vs Coût des Stratégies',
                           size_max=30)
            st.plotly_chart(fig, use_container_width=True)
    
    def create_regional_analysis(self):
        """Analyse des disparités régionales"""
        st.markdown('<h3 class="section-header">🗺️ ANALYSE RÉGIONALE ET DÉMOGRAPHIQUE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Cartographie", "Disparités Régionales", "Analyse Démographique"])
        
        with tab1:
            # Carte de France avec plotly.graph_objects
            st.subheader("Consommation d'Alcool par Région")
            
            # Données pour la carte de France
            regional_coords = {
                'Île-de-France': {'lat': 48.8566, 'lon': 2.3522, 'consommation': 7.8},
                'Auvergne-Rhône-Alpes': {'lat': 45.75, 'lon': 4.85, 'consommation': 9.2},
                'Nouvelle-Aquitaine': {'lat': 44.8378, 'lon': -0.5792, 'consommation': 8.9},
                'Occitanie': {'lat': 43.6, 'lon': 1.4333, 'consommation': 9.5},
                'Hauts-de-France': {'lat': 50.6292, 'lon': 3.0573, 'consommation': 10.1},
                'Provence-Alpes-Côte d\'Azur': {'lat': 43.3, 'lon': 5.37, 'consommation': 8.4},
                'Pays de la Loire': {'lat': 47.2181, 'lon': -1.5528, 'consommation': 8.1},
                'Bretagne': {'lat': 48.1173, 'lon': -1.6778, 'consommation': 9.8},
                'Normandie': {'lat': 49.18, 'lon': -0.37, 'consommation': 8.7},
                'Grand Est': {'lat': 48.5734, 'lon': 7.7521, 'consommation': 9.4},
                'Bourgogne-Franche-Comté': {'lat': 47.24, 'lon': 6.02, 'consommation': 8.6},
                'Centre-Val de Loire': {'lat': 47.9, 'lon': 1.9, 'consommation': 8.3},
                'Corse': {'lat': 42.15, 'lon': 9.08, 'consommation': 11.2}
            }
            
            # Créer un DataFrame avec les coordonnées
            coords_data = []
            for region, info in regional_coords.items():
                coords_data.append({
                    'region': region,
                    'lat': info['lat'],
                    'lon': info['lon'],
                    'consommation': info['consommation']
                })
            
            coords_df = pd.DataFrame(coords_data)
            
            # Créer une carte scatter_geo avec un fond de carte visible
            fig = px.scatter_geo(coords_df,
                                lat='lat',
                                lon='lon',
                                color='consommation',
                                size='consommation',
                                hover_name='region',
                                hover_data={'consommation': True},
                                title='Consommation d\'Alcool par Région (litres/pers/an) - 2023',
                                color_continuous_scale='RdYlGn_r',
                                size_max=20,
                                projection='natural earth')
            
            # Configuration pour rendre la carte visible
            fig.update_geos(
                visible=True,
                resolution=50,
                scope='europe',
                showcountries=True,
                countrycolor="black",
                showsubunits=True,
                subunitcolor="blue",
                landcolor="lightgray",
                oceancolor="lightblue",
                lakecolor="blue",
                bgcolor="white"
            )
            
            # Ajuster la vue sur la France
            fig.update_geos(
                center=dict(lat=46.5, lon=2),
                projection_scale=5
            )
            
            fig.update_layout(
                height=600,
                geo=dict(
                    bgcolor='rgba(255,255,255,0.1)',
                    landcolor='lightgreen'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Carte choroplèthe européenne
            st.subheader("Comparaison Européenne")
            
            # Données pour l'Europe
            europe_data = {
                'pays': ['France', 'Allemagne', 'Italie', 'Espagne', 'Royaume-Uni', 'Belgique', 'Pays-Bas', 'Suisse'],
                'consommation': [8.3, 10.6, 6.9, 7.5, 9.8, 10.2, 8.7, 9.1],
                'code': ['FRA', 'DEU', 'ITA', 'ESP', 'GBR', 'BEL', 'NLD', 'CHE']
            }
            
            europe_df = pd.DataFrame(europe_data)
            
            fig_europe = px.choropleth(europe_df,
                                     locations='code',
                                     color='consommation',
                                     hover_name='pays',
                                     title='Consommation d\'Alcool en Europe (litres/pers/an)',
                                     color_continuous_scale='RdYlGn_r',
                                     scope='europe')
            
            fig_europe.update_geos(
                visible=True,
                resolution=50,
                showcountries=True,
                countrycolor="black"
            )
            
            st.plotly_chart(fig_europe, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Classement des régions
                fig = px.bar(self.regional_data.sort_values('consommation_2023'), 
                            x='consommation_2023', 
                            y='region',
                            orientation='h',
                            title='Consommation d\'Alcool par Région - 2023',
                            color='consommation_2023',
                            color_continuous_scale='RdYlGn_r')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Évolution régionale
                fig = px.bar(self.regional_data.sort_values('evolution_2010_2023'), 
                            x='evolution_2010_2023', 
                            y='region',
                            orientation='h',
                            title='Évolution de la Consommation 2010-2023 (litres/pers/an)',
                            color='evolution_2010_2023',
                            color_continuous_scale='RdYlGn')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Analyse par catégories socio-démographiques
            st.subheader("Profil des Consommateurs")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 👥 Par Catégorie Socio-professionnelle
                
                **Consommation la plus élevée:**
                • Agriculteurs: 12.5L  
                • Ouvriers: 10.8L  
                • Artisans: 9.9L  
                
                **Consommation la plus basse:**
                • Cadres: 7.2L  
                • Professions intermédiaires: 8.1L  
                • Retraités: 8.5L  
                """)
            
            with col2:
                st.markdown("""
                ### 🎂 Par Tranche d'Âge
                
                **15-24 ans:** 6.8L (fort binge drinking)  
                **25-34 ans:** 9.2L  
                **35-44 ans:** 8.9L  
                **45-54 ans:** 9.5L  
                **55-64 ans:** 10.1L  
                **65+ ans:** 8.7L  
                
                **Âge moyen de 1ère ivresse:** 15.2 ans
                """)
    
    def create_international_comparison(self):
        """Analyse comparative internationale"""
        st.markdown('<h3 class="section-header">🌍 COMPARAISON INTERNATIONALE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Consommation", "Politiques", "Performances"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Consommation comparée
                fig = px.bar(self.international_comparison.sort_values('consommation_alcool'), 
                            x='pays', 
                            y='consommation_alcool',
                            title='Consommation d\'Alcool - Comparaison Internationale',
                            color='consommation_alcool',
                            color_continuous_scale='RdYlGn_r')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Prix vs consommation
                fig = px.scatter(self.international_comparison, 
                               x='prix_biere_eur', 
                               y='consommation_alcool',
                               size='mortalite_liee_alcool',
                               color='pays',
                               hover_name='pays',
                               title='Relation Prix vs Consommation',
                               size_max=30)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Comparaison des politiques
            st.subheader("Stratégies Nationales de Lutte contre l'Alcoolisme")
            
            policy_comparison = [
                {'pays': 'France', 'publicite_limitee': 1, 'taxes_elevees': 1, 'controles_renforces': 1, 'prevention_jeunes': 1},
                {'pays': 'Royaume-Uni', 'publicite_limitee': 1, 'taxes_elevees': 1, 'controles_renforces': 1, 'prevention_jeunes': 1},
                {'pays': 'Pays-Bas', 'publicite_limitee': 0, 'taxes_elevees': 0, 'controles_renforces': 1, 'prevention_jeunes': 1},
                {'pays': 'Allemagne', 'publicite_limitee': 0, 'taxes_elevees': 0, 'controles_renforces': 0, 'prevention_jeunes': 0},
                {'pays': 'États-Unis', 'publicite_limitee': 0, 'taxes_elevees': 0, 'controles_renforces': 1, 'prevention_jeunes': 1},
            ]
            
            policy_df = pd.DataFrame(policy_comparison)
            
            fig = px.imshow(policy_df.set_index('pays'),
                          title='Comparaison des Politiques sur l\'Alcool',
                          color_continuous_scale='RdYlGn')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Performance des stratégies
            st.subheader("Performance des Stratégies Nationales")
            
            performance_data = [
                {'pays': 'Royaume-Uni', 'reduction_10ans': -2.8, 'investissement_prevention': 0.8, 'classement': 1},
                {'pays': 'France', 'reduction_10ans': -2.1, 'investissement_prevention': 0.4, 'classement': 2},
                {'pays': 'Italie', 'reduction_10ans': -1.9, 'investissement_prevention': 0.3, 'classement': 3},
                {'pays': 'Canada', 'reduction_10ans': -1.7, 'investissement_prevention': 0.6, 'classement': 4},
                {'pays': 'États-Unis', 'reduction_10ans': -1.2, 'investissement_prevention': 1.2, 'classement': 5},
                {'pays': 'Allemagne', 'reduction_10ans': -0.8, 'investissement_prevention': 0.3, 'classement': 6},
            ]
            
            perf_df = pd.DataFrame(performance_data)
            
            # CORRECTION : Utiliser une colonne positive pour la taille
            perf_df['reduction_absolue'] = perf_df['reduction_10ans'].abs()
            
            fig = px.scatter(perf_df, 
                           x='investissement_prevention', 
                           y='reduction_10ans',
                           size='reduction_absolue',  # Utiliser les valeurs absolues
                           color='pays',
                           hover_name='pays',
                           title='Investissement vs Réduction de la Consommation',
                           size_max=30)
            st.plotly_chart(fig, use_container_width=True)
    
    def create_strategic_recommendations(self):
        """Recommandations stratégiques"""
        st.markdown('<h3 class="section-header">🎯 RECOMMANDATIONS STRATÉGIQUES</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Objectifs 2030", "Stratégies Prioritaires", "Feuille de Route"])
        
        with tab1:
            st.subheader("Objectifs Nationaux 2030")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                ### 🎯 Objectif Principal
                
                **Réduction de 20% de la consommation**
                
                • < 6.5L/pers/an  
                • -30% de binge drinking  
                • -40% de mortalité liée  
                """)
            
            with col2:
                st.markdown("""
                ### 📊 Cibles Intermédiaires
                
                **2025:**
                • < 7.5L/pers/an  
                • -15% de binge drinking  
                • Prix minimum unitaire  
                
                **2027:**
                • < 7.0L/pers/an  
                • -25% de binge drinking  
                • Publicité totalement encadrée  
                """)
            
            with col3:
                st.markdown("""
                ### 📈 Indicateurs de Suivi
                
                • Consommation déclarée  
                • Ventes d'alcool  
                • Binge drinking jeune  
                • Accidents routiers alcoolisés  
                • Hospitalisations  
                """)
        
        with tab2:
            st.subheader("Stratégies Prioritaires")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🚨 Actions Immédiates (2024-2025)
                
                **1. Prix minimum unitaire**
                • Application sur toutes les boissons  
                • Objectif: réduction accessibilité  
                
                **2. Renforcement des contrôles**
                • Alcootests préventifs  
                • Sanctions renforcées  
                
                **3. Prévention jeune**
                • Campagnes ciblées réseaux sociaux  
                • Intervention en milieu scolaire  
                """)
            
            with col2:
                st.markdown("""
                ### 🏗️ Réformes Structurelles (2026-2030)
                
                **1. Encadrement total publicité**
                • Interdiction sponsoring événements  
                • Restrictions packaging  
                
                **2. Dépistage systématique**
                • Médecine du travail  
                • Médecine scolaire  
                
                **3. Prise en charge renforcée**
                • Désaddiction remboursée  
                • Maisons des addictions  
                """)
        
        with tab3:
            st.subheader("Feuille de Route Détaillée")
            
            roadmap = [
                {'periode': '2024', 'actions': ['Loi prix minimum', 'Campagne jeunes', 'Renforcement contrôles']},
                {'periode': '2025', 'actions': ['Évaluation prix minimum', 'Extension prévention', 'Formation professionnels']},
                {'periode': '2026-2027', 'actions': ['Nouvelle hausse taxes', 'Interdiction publicité', 'Dépistage élargi']},
                {'periode': '2028-2030', 'actions': ['Objectif 6.5L atteint', 'Évaluation stratégique', 'Adaptation politiques']},
            ]
            
            for step in roadmap:
                with st.expander(f"📅 {step['periode']}"):
                    for action in step['actions']:
                        st.write(f"• {action}")
            
            # Graphique de projection
            years_projection = list(range(2020, 2031))
            consumption_projection = [8.9, 8.7, 8.5, 8.3, 8.0, 7.7, 7.4, 7.1, 6.8, 6.6, 6.5]
            
            fig = px.line(x=years_projection, y=consumption_projection,
                         title='Projection de la Consommation d\'Alcool 2020-2030',
                         markers=True)
            fig.add_hrect(y0=0, y1=6.5, line_width=0, fillcolor="green", opacity=0.2,
                         annotation_text="Objectif 2030")
            fig.update_layout(yaxis_title="Consommation (L/pers/an)", xaxis_title="Année")
            st.plotly_chart(fig, use_container_width=True)
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Période d'analyse
        st.sidebar.markdown("### 📅 Période d'analyse")
        annee_debut = st.sidebar.selectbox("Année de début", 
                                         list(range(2000, 2024)), 
                                         index=0)
        annee_fin = st.sidebar.selectbox("Année de fin", 
                                       list(range(2000, 2024)), 
                                       index=23)
        
        # Focus d'analyse
        st.sidebar.markdown("### 🎯 Focus d'analyse")
        focus_analysis = st.sidebar.multiselect(
            "Domaines à approfondir:",
            ['Consommation', 'Politiques', 'Impact santé', 'Disparités régionales', 'Comparaisons internationales'],
            default=['Consommation', 'Politiques']
        )
        
        # Options d'affichage
        st.sidebar.markdown("### ⚙️ Options")
        show_projections = st.sidebar.checkbox("Afficher les projections", value=True)
        auto_refresh = st.sidebar.checkbox("Rafraîchissement automatique", value=False)
        
        # Bouton d'export
        if st.sidebar.button("📊 Exporter l'analyse"):
            st.sidebar.success("Export réalisé avec succès!")
        
        return {
            'annee_debut': annee_debut,
            'annee_fin': annee_fin,
            'focus_analysis': focus_analysis,
            'show_projections': show_projections,
            'auto_refresh': auto_refresh
        }
    
    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Métriques clés
        self.display_key_metrics()
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📈 Historique", 
            "🏛️ Politiques", 
            "🗺️ Régional", 
            "🌍 International", 
            "🎯 Stratégies",
            "💡 Synthèse"
        ])
        
        with tab1:
            self.create_historical_analysis()
        
        with tab2:
            self.create_policy_analysis()
        
        with tab3:
            self.create_regional_analysis()
        
        with tab4:
            self.create_international_comparison()
        
        with tab5:
            self.create_strategic_recommendations()
        
        with tab6:
            st.markdown("## 💡 SYNTHÈSE STRATÉGIQUE")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### ✅ SUCCÈS ET PROGRÈS
                
                **Baisse continue depuis 20 ans:**
                • Consommation divisée par 1.6  
                • Mortalité routière réduite  
                • Prévention renforcée  
                • Prise de conscience collective  
                
                **Politiques efficaces:**
                • Encadrement publicité  
                • Contrôles routiers  
                • Prévention jeune  
                • Services d'aide  
                """)
            
            with col2:
                st.markdown("""
                ### ⚠️ DÉFIS PERSISTANTS
                
                **Problématiques spécifiques:**
                • Binge drinking jeune en hausse  
                • Inégalités sociales marquées  
                • Culture vin persistante  
                • Accessibilité importante  
                
                **Nouveaux enjeux:**
                • Alcoolisation express  
                • Nouvelles boissons  
                • Commerce en ligne  
                • Normalisation sociale  
                """)
            
            st.markdown("""
            ### 🚨 ALERTES ET RECOMMANDATIONS
            
            **Niveau d'Alerte: MODÉRÉ**
            
            **Points de Vigilance:**
            • Stagnation de la baisse  
            • Binge drinking jeune  
            • Inégalités territoriales  
            • Nouveaux modes de consommation  
            
            **Recommandations Immédiates:**
            1. Mise en place du prix minimum unitaire  
            2. Renforcement de la prévention jeune  
            3. Lutte contre les inégalités sociales  
            4. Encadrement du commerce numérique  
            5. Coordination européenne renforcée  
            """)
        
        # Rafraîchissement automatique
        if controls['auto_refresh']:
            time.sleep(300)
            st.rerun()

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = AlcoholDashboard()
    dashboard.run_dashboard()