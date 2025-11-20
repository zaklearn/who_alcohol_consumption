"""
WHO Alcohol Data Analysis - Enhanced Streamlit Dashboard
Bilingual English/French Interface with Continental Analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.data_processor import WHODataProcessor
from core.report_generator import HTMLReportGenerator
from config.translations import TRANSLATIONS

st.set_page_config(
    page_title="WHO Alcohol Analysis",
    #page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'processor' not in st.session_state:
    st.session_state.processor = None

# Language selector
with st.sidebar:
    lang = st.selectbox(
        "Language / Langue",
        options=['en', 'fr'],
        format_func=lambda x: "🇬🇧 English" if x == 'en' else "🇫🇷 Français"
    )
    st.session_state.language = lang
    st.markdown("---")
    
    if st.button(TRANSLATIONS[lang]['load_data'], type="primary", width='stretch'):
        with st.spinner(TRANSLATIONS[lang]['loading']):
            processor = WHODataProcessor()
            if processor.fetch_all_data():
                st.session_state.processor = processor
                st.session_state.data_loaded = True
                st.success(TRANSLATIONS[lang]['data_loaded'])
                st.rerun()
            else:
                st.error(TRANSLATIONS[lang]['load_error'])

def t(key):
    return TRANSLATIONS[st.session_state.language].get(key, key)

st.title(f" {t('app_title')}")
st.markdown(f"*{t('subtitle')}*")

if not st.session_state.data_loaded:
    st.info(t('click_load'))
    st.stop()

processor = st.session_state.processor

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    t('overview'),
    t('consumption'),
    t('disorders'),
    t('correlations'),
    t('regional'),
    t('export')
])

# TAB 1: ENHANCED OVERVIEW
with tab1:
    st.header(t('overview'))
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_countries = len(processor.alcohol_consumption) if processor.alcohol_consumption is not None else 0
        st.metric(t('total_countries'), total_countries)
    with col2:
        if processor.alcohol_consumption is not None and '2022' in processor.alcohol_consumption.columns:
            avg_consumption = processor.alcohol_consumption['2022'].mean()
            st.metric(t('global_avg_2022'), f"{avg_consumption:.1f}L")
    with col3:
        if processor.alcohol_consumption is not None and '2022' in processor.alcohol_consumption.columns:
            max_consumption = processor.alcohol_consumption['2022'].max()
            st.metric(t('highest_consumption'), f"{max_consumption:.1f}L")
    with col4:
        if processor.alcohol_disorder is not None:
            avg_disorder = processor.alcohol_disorder[
                processor.alcohol_disorder['gender'] == 1
            ]['alcohol_disorder'].mean()
            st.metric(t('avg_disorders'), f"{avg_disorder:.1f}%")
    
    st.markdown("---")
    
    # Consumption by gender
    st.subheader(t('consumption_by_gender'))
    if processor.alcohol_disorder is not None:
        gender_map = {1: t('male'), 2: t('female')}
        gender_data = processor.alcohol_disorder[
            processor.alcohol_disorder['gender'].isin([1, 2])
        ].copy()
        gender_data['gender_name'] = gender_data['gender'].map(gender_map)
        
        global_gender = gender_data.groupby('gender_name')['alcohol_disorder'].mean().reset_index()
        
        fig = px.bar(
            global_gender,
            x='gender_name',
            y='alcohol_disorder',
            title=t('global_gender_disorders'),
            color='gender_name',
            labels={'alcohol_disorder': t('prevalence'), 'gender_name': t('gender')}
        )
        st.plotly_chart(fig, width='stretch')
    
    # Top countries by continent - trends over time
    st.subheader(t('continental_trends'))
    
    if processor.alcohol_consumption is not None:
        # Define continental mapping
        continent_map = {
            'Europe': ['Germany', 'France', 'United Kingdom', 'Italy', 'Spain', 'Poland'],
            'Americas': ['United States of America', 'Brazil', 'Mexico', 'Canada', 'Argentina'],
            'Africa': ['South Africa', 'Nigeria', 'Egypt', 'Kenya', 'Ethiopia'],
            'Asia': ['China', 'India', 'Japan', 'Republic of Korea', 'Indonesia'],
            'Oceania': ['Australia', 'New Zealand']
        }
        
        year_cols = [col for col in processor.alcohol_consumption.columns 
                    if col not in ['country', 'region'] and str(col).isdigit()]
        
        for continent, countries in continent_map.items():
            continent_data = processor.alcohol_consumption[
                processor.alcohol_consumption['country'].isin(countries)
            ].copy()
            
            if not continent_data.empty:
                # Melt to long format
                long_data = pd.melt(
                    continent_data,
                    id_vars=['country'],
                    value_vars=year_cols,
                    var_name='year',
                    value_name='consumption'
                )
                long_data['year'] = long_data['year'].astype(int)
                long_data = long_data.dropna()
                
                if not long_data.empty:
                    fig = px.line(
                        long_data,
                        x='year',
                        y='consumption',
                        color='country',
                        title=f"{t('trends')} - {continent}",
                        markers=True,
                        labels={'consumption': t('consumption_litres'), 'year': t('year')},
                        color_discrete_sequence=px.colors.qualitative.Vivid
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, width='stretch')

# TAB 2: ENHANCED CONSUMPTION
with tab2:
    st.header(t('alcohol_consumption'))
    
    # Top 10 countries
    st.subheader(t('top_10_countries'))
    top10 = processor.get_top_consumers('2022', 10)
    if top10 is not None:
        fig = px.bar(
            top10,
            x='country',
            y='consumption',
            color='region',
            title=t('top_10_title'),
            labels={'consumption': t('consumption_litres'), 'country': t('country')},
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        fig.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig, width='stretch')
    
    # World map - FULL WIDTH
    st.subheader(t('world_map'))
    if processor.alcohol_consumption is not None and '2022' in processor.alcohol_consumption.columns:
        map_data = processor.alcohol_consumption[['country', '2022']].dropna()
        
        fig = px.choropleth(
            map_data,
            locations='country',
            locationmode='country names',
            color='2022',
            hover_name='country',
            color_continuous_scale='Blues',
            title=t('global_consumption_map')
        )
        fig.update_layout(height=600, geo=dict(showframe=False, showcoastlines=True))
        st.plotly_chart(fig, width='stretch')
    
    # Continental trends
    st.subheader(t('continental_trends'))
    
    # Europe
    europe_data = processor.get_europe_trend_data()
    if europe_data is not None:
        fig = px.line(
            europe_data,
            x='year',
            y='alcohol_consumption',
            color='country',
            title=t('europe_evolution'),
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, width='stretch')
    
    # Other continents
    if processor.alcohol_consumption is not None:
        continent_regions = {
            'Americas': ['United States of America', 'Brazil', 'Mexico', 'Canada', 'Argentina', 'Chile'],
            'Africa': ['South Africa', 'Nigeria', 'Egypt', 'Kenya', 'Ethiopia', 'Morocco'],
            'Asia': ['China', 'India', 'Japan', 'Republic of Korea', 'Indonesia', 'Thailand']
        }
        
        year_cols = [col for col in processor.alcohol_consumption.columns 
                    if col not in ['country', 'region'] and str(col).isdigit()]
        
        for continent, countries in continent_regions.items():
            cont_data = processor.alcohol_consumption[
                processor.alcohol_consumption['country'].isin(countries)
            ].copy()
            
            if not cont_data.empty:
                long_data = pd.melt(
                    cont_data,
                    id_vars=['country'],
                    value_vars=year_cols,
                    var_name='year',
                    value_name='consumption'
                )
                long_data['year'] = long_data['year'].astype(int)
                long_data = long_data.dropna()
                
                if not long_data.empty:
                    fig = px.line(
                        long_data,
                        x='year',
                        y='consumption',
                        color='country',
                        title=f"{t('trends')} - {continent}",
                        markers=True,
                        color_discrete_sequence=px.colors.qualitative.Bold
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, width='stretch')

# TAB 3: DISORDERS
with tab3:
    st.header(t('alcohol_disorders'))
    
    if processor.alcohol_disorder is not None:
        st.subheader(t('gender_comparison'))
        
        gender_map = {1: t('male'), 2: t('female')}
        disorder_data = processor.alcohol_disorder[
            processor.alcohol_disorder['gender'].isin([1, 2])
        ].copy()
        disorder_data['gender_name'] = disorder_data['gender'].map(gender_map)
        
        regional_gender = disorder_data.groupby(['region', 'gender_name'])['alcohol_disorder'].mean().reset_index()
        
        fig = px.bar(
            regional_gender,
            x='region',
            y='alcohol_disorder',
            color='gender_name',
            title=t('disorders_by_region_gender'),
            barmode='group',
            labels={'alcohol_disorder': t('prevalence'), 'region': t('region')}
        )
        fig.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig, width='stretch')

# TAB 4: CORRELATIONS
with tab4:
    st.header(t('correlation_analysis'))
    
    merged_data = processor.merge_consumption_disorder_data('2022')
    
    if merged_data is not None:
        male_data = merged_data[merged_data['gender'] == 1].copy()
        
        if len(male_data) > 0:
            from scipy.stats import linregress
            import numpy as np
            
            slope, intercept, r_value, p_value, _ = linregress(
                male_data['consumption'],
                male_data['alcohol_disorder']
            )
            r_squared = r_value ** 2
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(t('correlation'), f"{r_value:.3f}")
            with col2:
                st.metric(t('r_squared'), f"{r_squared:.3f}")
            with col3:
                significance = '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns'
                st.metric(t('significance'), significance)
            
            x_range = np.linspace(male_data['consumption'].min(), male_data['consumption'].max(), 100)
            y_pred = slope * x_range + intercept
            
            fig = px.scatter(
                male_data,
                x='consumption',
                y='alcohol_disorder',
                color='region',
                hover_name='country',
                title=t('consumption_vs_disorders'),
                labels={
                    'consumption': t('consumption_litres'),
                    'alcohol_disorder': t('disorders_percentage')
                },
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            
            fig.add_trace(
                go.Scatter(
                    x=x_range,
                    y=y_pred,
                    mode='lines',
                    name=f'{t("regression_line")} (R² = {r_squared:.3f})',
                    line=dict(color='gray', dash='dash')
                )
            )
            
            fig.update_layout(height=600)
            st.plotly_chart(fig, width='stretch')

# TAB 5: REGIONAL
with tab5:
    st.header(t('regional_analysis'))
    
    if processor.alcohol_consumption is not None and '2022' in processor.alcohol_consumption.columns:
        regional_data = processor.get_regional_averages('2022')
        
        if regional_data is not None:
            st.dataframe(regional_data, width='stretch')
            
            fig = px.bar(
                regional_data,
                x='Region',
                y='Average_Consumption',
                title=t('regional_comparison'),
                color='Average_Consumption',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, width='stretch')

# TAB 6: EXPORT
with tab6:
    st.header(t('export_report'))
    st.markdown(t('export_description'))
    
    report_name = st.text_input(
        t('report_name'),
        value=f"WHO_Alcohol_Report_{st.session_state.language}",
        help=t('report_help')
    )
    
    if st.button(t('generate_report'), type="primary", width='stretch'):
        with st.spinner(t('generating_report')):
            try:
                figures = {}
                
                # Top 10
                top10 = processor.get_top_consumers('2022', 10)
                if top10 is not None:
                    fig = px.bar(top10, x='country', y='consumption', color='region',
                               color_discrete_sequence=px.colors.qualitative.Plotly)
                    figures['top10'] = fig
                
                # World map
                if processor.alcohol_consumption is not None and '2022' in processor.alcohol_consumption.columns:
                    map_data = processor.alcohol_consumption[['country', '2022']].dropna()
                    fig = px.choropleth(
                        map_data,
                        locations='country',
                        locationmode='country names',
                        color='2022',
                        color_continuous_scale='Blues'
                    )
                    figures['world_map'] = fig
                
                # Continental trends - flatten to individual figures
                continent_regions = {
                    'Europe': processor.get_europe_trend_data(),
                    'Americas': ['United States of America', 'Brazil', 'Mexico', 'Canada'],
                    'Africa': ['South Africa', 'Nigeria', 'Egypt', 'Kenya'],
                    'Asia': ['China', 'India', 'Japan', 'Republic of Korea']
                }
                
                for continent, data_or_countries in continent_regions.items():
                    if continent == 'Europe' and data_or_countries is not None:
                        fig = px.line(data_or_countries, x='year', y='alcohol_consumption', color='country',
                                    color_discrete_sequence=px.colors.qualitative.Set2)
                        figures[f'trends_{continent.lower()}'] = fig
                    elif continent != 'Europe':
                        year_cols = [col for col in processor.alcohol_consumption.columns 
                                    if col not in ['country', 'region'] and str(col).isdigit()]
                        cont_data = processor.alcohol_consumption[
                            processor.alcohol_consumption['country'].isin(data_or_countries)
                        ].copy()
                        
                        if not cont_data.empty:
                            long_data = pd.melt(cont_data, id_vars=['country'], 
                                              value_vars=year_cols, var_name='year', value_name='consumption')
                            long_data['year'] = long_data['year'].astype(int)
                            long_data = long_data.dropna()
                            
                            if not long_data.empty:
                                fig = px.line(long_data, x='year', y='consumption', color='country',
                                            color_discrete_sequence=px.colors.qualitative.Bold)
                                figures[f'trends_{continent.lower()}'] = fig
                
                # Scatter
                merged_data = processor.merge_consumption_disorder_data('2022')
                if merged_data is not None:
                    male_data = merged_data[merged_data['gender'] == 1]
                    if len(male_data) > 0:
                        fig = px.scatter(male_data, x='consumption', y='alcohol_disorder', 
                                       color='region', hover_name='country',
                                       color_discrete_sequence=px.colors.qualitative.Safe)
                        figures['scatter'] = fig
                
                # Generate report
                report_gen = HTMLReportGenerator(language=st.session_state.language)
                output_dir = os.path.join(os.getcwd(), 'reports')
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, f"{report_name}.html")
                
                report_gen.generate_report(processor, figures, output_path)
                
                st.success(t('report_generated'))
                
                with open(output_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                st.download_button(
                    label=t('download_report'),
                    data=html_content,
                    file_name=f"{report_name}.html",
                    mime="text/html",
                    width='stretch'
                )
                
            except Exception as e:
                st.error(f"{t('export_error')}: {str(e)}")

st.markdown("---")
st.markdown(f"*{t('footer')}*")