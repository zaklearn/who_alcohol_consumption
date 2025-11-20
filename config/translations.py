"""
Bilingual translations for WHO Alcohol Analysis Dashboard
English / French
"""

TRANSLATIONS = {
    'en': {
        # App
        'app_title': 'WHO Alcohol Data Analysis',
        'subtitle': 'Global alcohol consumption patterns and health indicators',
        'footer': 'Data source: WHO Global Health Observatory | Analysis powered by Streamlit',
        
        # Sidebar
        'load_data': '📥 Load WHO Data',
        'loading': 'Loading data from WHO API...',
        'data_loaded': '✅ Data loaded successfully!',
        'load_error': '❌ Failed to load data. Check your connection.',
        'click_load': '👈 Click "Load WHO Data" in the sidebar to begin',
        
        # Tabs
        'overview': '📊 Overview',
        'consumption': '🍷 Consumption',
        'disorders': '🏥 Disorders',
        'correlations': '🔗 Correlations',
        'regional': '🌍 Regional',
        'export': '📄 Export',
        
        # Metrics
        'total_countries': 'Countries Analyzed',
        'global_avg_2022': 'Global Average (2022)',
        'highest_consumption': 'Highest Consumption',
        'avg_disorders': 'Avg. Disorders (Male)',
        
        # Charts
        'regional_averages': 'Regional Averages',
        'regional_consumption_2022': 'Average Alcohol Consumption by WHO Region (2022)',
        'alcohol_consumption': 'Alcohol Consumption Analysis',
        'top_10_countries': 'Top 10 Countries',
        'top_10_title': 'Top 10 Countries by Alcohol Consumption (2022)',
        'world_map': 'World Map',
        'global_consumption_map': 'Global Alcohol Consumption (2022)',
        'europe_trends': 'European Trends',
        'europe_evolution': 'Evolution of Alcohol Consumption in Europe (2000-2022)',
        
        # Disorders
        'alcohol_disorders': 'Alcohol Use Disorders Analysis',
        'gender_comparison': 'Gender Comparison',
        'disorders_by_region_gender': 'Alcohol Use Disorders by Region and Gender',
        'male': 'Male',
        'female': 'Female',
        
        # Correlations
        'correlation_analysis': 'Correlation Analysis',
        'consumption_vs_disorders': 'Alcohol Consumption vs. Male Alcohol Use Disorders',
        'correlation': 'Correlation',
        'r_squared': 'R²',
        'significance': 'Significance',
        'regression_line': 'Regression Line',
        
        # Regional
        'regional_analysis': 'Regional Analysis',
        'regional_comparison': 'Regional Comparison',
        
        # Labels
        'consumption_litres': 'Consumption (Litres)',
        'country': 'Country',
        'region': 'Region',
        'prevalence': 'Prevalence (%)',
        'disorders_percentage': 'Disorders (%)',
        'year': 'Year',
        'gender': 'Gender',
        'trends': 'Trends',
        'consumption_by_gender': 'Alcohol Consumption by Gender',
        'global_gender_disorders': 'Global Alcohol Disorders by Gender',
        'continental_trends': 'Continental Trends - Top Countries',
        
        # Export
        'export_report': 'Export HTML Report',
        'export_description': '**Generate a comprehensive HTML report** with all visualizations and analysis. The report can be opened in any web browser.',
        'report_name': 'Report Name',
        'report_help': 'Enter filename without extension',
        'generate_report': '📊 Generate Full Report',
        'generating_report': 'Generating comprehensive report...',
        'report_generated': '✅ Report generated successfully!',
        'download_report': '⬇️ Download Report',
        'export_error': 'Error generating report',
    },
    
    'fr': {
        # App
        'app_title': 'Analyse des données OMS sur l\'alcool',
        'subtitle': 'Modèles mondiaux de consommation d\'alcool et indicateurs de santé',
        'footer': 'Source des données : Observatoire mondial de la santé de l\'OMS | Analyse propulsée par Streamlit',
        
        # Sidebar
        'load_data': '📥 Charger les données OMS',
        'loading': 'Chargement des données depuis l\'API OMS...',
        'data_loaded': '✅ Données chargées avec succès !',
        'load_error': '❌ Échec du chargement des données. Vérifiez votre connexion.',
        'click_load': '👈 Cliquez sur "Charger les données OMS" dans la barre latérale pour commencer',
        
        # Tabs
        'overview': '📊 Aperçu',
        'consumption': '🍷 Consommation',
        'disorders': '🏥 Troubles',
        'correlations': '🔗 Corrélations',
        'regional': '🌍 Régional',
        'export': '📄 Exporter',
        
        # Metrics
        'total_countries': 'Pays analysés',
        'global_avg_2022': 'Moyenne mondiale (2022)',
        'highest_consumption': 'Consommation la plus élevée',
        'avg_disorders': 'Moy. troubles (Homme)',
        
        # Charts
        'regional_averages': 'Moyennes régionales',
        'regional_consumption_2022': 'Consommation moyenne d\'alcool par région OMS (2022)',
        'alcohol_consumption': 'Analyse de la consommation d\'alcool',
        'top_10_countries': 'Top 10 des pays',
        'top_10_title': 'Top 10 des pays par consommation d\'alcool (2022)',
        'world_map': 'Carte mondiale',
        'global_consumption_map': 'Consommation mondiale d\'alcool (2022)',
        'europe_trends': 'Tendances européennes',
        'europe_evolution': 'Évolution de la consommation d\'alcool en Europe (2000-2022)',
        
        # Disorders
        'alcohol_disorders': 'Analyse des troubles liés à l\'alcool',
        'gender_comparison': 'Comparaison par sexe',
        'disorders_by_region_gender': 'Troubles liés à l\'alcool par région et sexe',
        'male': 'Homme',
        'female': 'Femme',
        
        # Correlations
        'correlation_analysis': 'Analyse de corrélation',
        'consumption_vs_disorders': 'Consommation d\'alcool vs. Troubles liés à l\'alcool (Hommes)',
        'correlation': 'Corrélation',
        'r_squared': 'R²',
        'significance': 'Significativité',
        'regression_line': 'Ligne de régression',
        
        # Regional
        'regional_analysis': 'Analyse régionale',
        'regional_comparison': 'Comparaison régionale',
        
        # Labels
        'consumption_litres': 'Consommation (Litres)',
        'country': 'Pays',
        'region': 'Région',
        'prevalence': 'Prévalence (%)',
        'disorders_percentage': 'Troubles (%)',
        'year': 'Année',
        'gender': 'Sexe',
        'trends': 'Tendances',
        'consumption_by_gender': 'Consommation d\'alcool par sexe',
        'global_gender_disorders': 'Troubles liés à l\'alcool par sexe (Mondial)',
        'continental_trends': 'Tendances continentales - Principaux pays',
        
        # Export
        'export_report': 'Exporter le rapport HTML',
        'export_description': '**Générez un rapport HTML complet** avec toutes les visualisations et analyses. Le rapport peut être ouvert dans n\'importe quel navigateur web.',
        'report_name': 'Nom du rapport',
        'report_help': 'Entrez le nom du fichier sans extension',
        'generate_report': '📊 Générer le rapport complet',
        'generating_report': 'Génération du rapport complet...',
        'report_generated': '✅ Rapport généré avec succès !',
        'download_report': '⬇️ Télécharger le rapport',
        'export_error': 'Erreur lors de la génération du rapport',
    }
}