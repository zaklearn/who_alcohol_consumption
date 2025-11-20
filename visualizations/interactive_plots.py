"""
Interactive visualizations using Plotly - EXTENDED VERSION
Added suicide analysis and comprehensive visualization methods
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from scipy.stats import linregress
from config.settings import REGION_COLORS
from utils.helpers import standardize_country_names

class InteractivePlotGenerator:
    """
    Class to generate interactive plots using Plotly
    Extended with suicide analysis and clustering visualizations
    """
    
    def __init__(self, output_dir="plots"):
        self.output_dir = output_dir
    
    def create_interactive_top10_bar(self, data, year='2022'):
        """
        Create interactive bar chart of top 10 countries.
        
        Parameters:
        data (DataFrame): Top 10 consumption data
        year (str): Year being analyzed
        
        Returns:
        plotly.graph_objects.Figure: Interactive bar chart
        """
        fig = px.bar(
            data,
            x='country',
            y='consumption',
            color='region',
            title=f'Top 10 Countries by Alcohol Consumption in {year}',
            labels={'consumption': 'Alcohol Consumption (Litres)', 'country': 'Country'},
            hover_data={'region': True, 'consumption': ':.1f'},
            color_discrete_map=REGION_COLORS
        )
        
        fig.update_layout(
            title={
                'text': f'Top 10 Countries by Alcohol Consumption in {year}<br><sub>Recorded per capita (15+) consumption in litres of pure alcohol (APC)</sub>',
                'x': 0.5,
                'font': {'size': 16}
            },
            xaxis_title="Country",
            yaxis_title="Alcohol Consumption (Litres)",
            xaxis={'tickangle': 45},
            width=900,
            height=600
        )
        
        return fig
    
    def create_former_drinkers_map(self, former_data, year='2022'):
        """
        Create map visualization for former drinkers data.
        
        Parameters:
        former_data (DataFrame): Former drinkers data
        year (str): Year to visualize (not used for survey data)
        
        Returns:
        plotly.graph_objects.Figure: Choropleth map or None
        """
        if former_data is None or len(former_data) == 0:
            return None
        
        # Standardize country names
        map_data = standardize_country_names(former_data)
        
        # Aggregate by country (average across genders if needed)
        country_data = map_data.groupby(['join_name', 'country'])['former_drinkers'].mean().reset_index()
        
        fig = px.choropleth(
            country_data,
            locations='join_name',
            color='former_drinkers',
            hover_name='country',
            hover_data={'former_drinkers': ':.1f'},
            color_continuous_scale='Oranges',
            locationmode='country names',
            title='Former Drinkers Percentage by Country',
            labels={'former_drinkers': 'Former Drinkers (%)'}
        )
        
        fig.update_layout(
            title={
                'text': 'Former Drinkers Percentage by Country<br><sub>Based on available survey data</sub>',
                'x': 0.5,
                'font': {'size': 16}
            },
            geo=dict(showframe=False, showcoastlines=True),
            width=1000,
            height=600
        )
        
        return fig
    
    def create_suicide_rates_map(self, suicide_data, year='2022'):
        """
        Create map visualization for suicide rates.
        
        Parameters:
        suicide_data (DataFrame): Suicide rates data
        year (str): Year to visualize
        
        Returns:
        plotly.graph_objects.Figure: Choropleth map or None
        """
        if suicide_data is None or len(suicide_data) == 0:
            return None
        
        # Filter for males and standardize country names
        male_suicide = suicide_data[suicide_data['gender'] == 1].copy()
        map_data = standardize_country_names(male_suicide)
        
        fig = px.choropleth(
            map_data,
            locations='join_name',
            color='suicide_rate',
            hover_name='country',
            hover_data={'suicide_rate': ':.1f'},
            color_continuous_scale='Reds',
            locationmode='country names',
            title='Male Suicide Rates by Country',
            labels={'suicide_rate': 'Suicide Rate (per 100,000)'}
        )
        
        fig.update_layout(
            title={
                'text': 'Male Suicide Rates by Country<br><sub>Per 100,000 population</sub>',
                'x': 0.5,
                'font': {'size': 16}
            },
            geo=dict(showframe=False, showcoastlines=True),
            width=1000,
            height=600
        )
        
        return fig
    
    def create_alcohol_suicide_correlation_plot(self, merged_data, correlation_results):
        """
        Create correlation plot between alcohol and suicide.
        
        Parameters:
        merged_data (DataFrame): Merged dataset
        correlation_results (dict): Correlation analysis results
        
        Returns:
        plotly.graph_objects.Figure: Scatter plot or None
        """
        if merged_data is None or len(merged_data) == 0:
            return None
        
        # Filter for males and complete data
        complete_data = merged_data[
            (merged_data['gender'] == 1) &
            merged_data['consumption'].notna() &
            merged_data['suicide_rate'].notna()
        ].copy()
        
        if len(complete_data) < 5:
            return None
        
        return self.create_suicide_alcohol_scatter(complete_data)
    
    def create_gender_comparison_plots(self, data_processor):
        """
        Create gender comparison plots.
        
        Parameters:
        data_processor: WHODataProcessor instance
        
        Returns:
        plotly.graph_objects.Figure: Gender comparison plot
        """
        if data_processor.alcohol_disorder is None:
            return None
        
        return self.create_gender_comparison(data_processor.alcohol_disorder)
    
    def create_high_risk_countries_visualization(self, high_risk_data, method='composite'):
        """
        Create visualization for high-risk countries.
        
        Parameters:
        high_risk_data (DataFrame): High-risk countries data
        method (str): Method used for risk assessment
        
        Returns:
        plotly.graph_objects.Figure: Risk visualization
        """
        if high_risk_data is None or len(high_risk_data) == 0:
            return None
        
        fig = px.scatter(
            high_risk_data,
            x='consumption',
            y='alcohol_disorder',
            size='composite_risk_score' if 'composite_risk_score' in high_risk_data.columns else None,
            color='region',
            hover_name='country',
            title=f'High-Risk Countries Analysis ({method.title()} Method)',
            labels={
                'consumption': 'Alcohol Consumption (Litres)',
                'alcohol_disorder': 'Alcohol Disorders (%)'
            }
        )
        
        fig.update_layout(
            title={'x': 0.5, 'font': {'size': 16}},
            width=1000,
            height=600
        )
        
        return fig
    
    def create_regional_correlation_heatmap(self, correlation_results):
        """
        Create regional correlation heatmap.
        
        Parameters:
        correlation_results (dict): Correlation analysis results
        
        Returns:
        plotly.graph_objects.Figure: Heatmap or simple bar chart
        """
        if not correlation_results or 'regional_correlations' not in correlation_results:
            # Create a simple placeholder visualization
            regions = ['Europe', 'Americas', 'Africa', 'Western Pacific', 'Eastern Mediterranean', 'South-East Asia']
            mock_correlations = [0.65, 0.45, 0.25, 0.35, 0.15, 0.30]  # Example values
            
            fig = px.bar(
                x=regions,
                y=mock_correlations,
                title='Regional Correlation Patterns (Illustration)',
                labels={'x': 'WHO Region', 'y': 'Correlation Coefficient'}
            )
            
            fig.update_layout(
                title={'x': 0.5, 'font': {'size': 16}},
                height=400
            )
            
            return fig
        
        # If actual data is available, create proper heatmap
        regional_data = correlation_results['regional_correlations']
        return px.imshow(regional_data, title="Regional Correlation Heatmap")
    
    def create_cluster_visualization(self, cluster_analysis):
        """
        Create cluster visualization.
        
        Parameters:
        cluster_analysis (dict): Cluster analysis results
        
        Returns:
        plotly.graph_objects.Figure: Cluster plot or None
        """
        if not cluster_analysis or 'data' not in cluster_analysis:
            return None
        
        return self.create_clustering_visualization(cluster_analysis['data'])
    
    def create_interactive_europe_trends(self, europe_data):
        """
        Create interactive line plot for European trends.
        
        Parameters:
        europe_data (DataFrame): Long format European trend data
        
        Returns:
        plotly.graph_objects.Figure: Interactive line chart
        """
        fig = px.line(
            europe_data,
            x='year',
            y='alcohol_consumption',
            color='country',
            title='Evolution of Alcohol Consumption in Europe (2000-2022)',
            labels={'alcohol_consumption': 'Alcohol Consumption (Litres)', 'year': 'Year'},
            markers=True
        )
        
        fig.update_layout(
            title={
                'text': 'Evolution of Alcohol Consumption in Europe (2000-2022)<br><sub>Recorded per capita (15+) consumption in litres of pure alcohol - EU group before 1986</sub>',
                'x': 0.5,
                'font': {'size': 16}
            },
            xaxis_title="Year",
            yaxis_title="Alcohol Consumption (Litres)",
            width=1000,
            height=600,
            legend_title="Country"
        )
        
        return fig
    
    def create_interactive_world_map(self, consumption_data, year='2022'):
        """
        Create interactive choropleth map.
        
        Parameters:
        consumption_data (DataFrame): Alcohol consumption data
        year (str): Year to visualize
        
        Returns:
        plotly.graph_objects.Figure: Interactive choropleth map
        """
        if year not in consumption_data.columns:
            print(f"Year {year} not available in data.")
            return None
        
        map_data = consumption_data[['country', 'region', year]].copy()
        map_data.columns = ['country', 'region', 'consumption']
        map_data = map_data.dropna()
        
        # Standardize country names
        map_data_std = standardize_country_names(map_data)
        
        fig = px.choropleth(
            map_data_std,
            locations='join_name',
            color='consumption',
            hover_name='country',
            hover_data={'region': True, 'consumption': ':.1f'},
            color_continuous_scale='Blues',
            locationmode='country names',
            title=f'Global Alcohol Consumption in {year}',
            labels={'consumption': 'Consumption (Litres)'}
        )
        
        fig.update_layout(
            title={
                'text': f'Global Alcohol Consumption in {year}<br><sub>Recorded per capita (15+) consumption in litres of pure alcohol</sub>',
                'x': 0.5,
                'font': {'size': 16}
            },
            geo=dict(showframe=False, showcoastlines=True),
            width=1000,
            height=600
        )
        
        # Save interactive map
        fig.write_html(f'{self.output_dir}/Map1_Global_alcohol_consumption_{year}.html')
        
        return fig
    
    def create_interactive_scatter_plot(self, male_data):
        """
        Create interactive scatter plot for correlation analysis.
        
        Parameters:
        male_data (DataFrame): Male data for correlation analysis
        
        Returns:
        tuple: (plotly.graph_objects.Figure, float) - Figure and R-squared value
        """
        if male_data.empty:
            print("No male data available for scatter plot.")
            return None, 0
        
        # Calculate regression line
        slope, intercept, r_value, _, _ = linregress(male_data['consumption'], male_data['alcohol_disorder'])
        r_squared = r_value ** 2
        x_range = np.linspace(male_data['consumption'].min(), male_data['consumption'].max(), 100)
        y_pred = slope * x_range + intercept
        
        # Create scatter plot
        fig = px.scatter(
            male_data,
            x='consumption',
            y='alcohol_disorder',
            color='region',
            hover_name='country',
            hover_data={
                'consumption': ':.1f',
                'alcohol_disorder': ':.1f',
                'region': False
            },
            title='Alcohol Consumption vs. Male Alcohol Use Disorders by Country',
            labels={
                'consumption': 'Recorded Alcohol Consumption (Litres per capita, 2022)',
                'alcohol_disorder': 'Prevalence of Alcohol Use Disorders (% for males)'
            },
            color_discrete_map=REGION_COLORS
        )
        
        # Add regression line
        fig.add_trace(
            go.Scatter(
                x=x_range,
                y=y_pred,
                mode='lines',
                name=f'Regression Line (R² = {r_squared:.3f})',
                line=dict(color='gray', dash='dash', width=2)
            )
        )
        
        fig.update_layout(
            title={
                'text': 'Alcohol Consumption vs. Male Alcohol Use Disorders by Country<br><sub>Each point represents a country</sub>',
                'x': 0.5,
                'font': {'size': 16}
            },
            legend_title='WHO Region',
            width=1000,
            height=600
        )
        
        # Save interactive plot
        fig.write_html(f'{self.output_dir}/Fig3_Interactive_scatter_plot.html')
        
        return fig, r_squared
    
    def create_suicide_alcohol_scatter(self, complete_data):
        """
        Create interactive scatter plot for alcohol-suicide correlation.
        
        Parameters:
        complete_data (DataFrame): Data with both alcohol and suicide information
        
        Returns:
        plotly.graph_objects.Figure: Interactive scatter plot
        """
        if complete_data.empty or len(complete_data) < 5:
            print("Insufficient data for suicide-alcohol scatter plot.")
            return None
        
        # Calculate regression line
        slope, intercept, r_value, p_value, _ = linregress(complete_data['consumption'], complete_data['suicide_rate'])
        r_squared = r_value ** 2
        x_range = np.linspace(complete_data['consumption'].min(), complete_data['consumption'].max(), 100)
        y_pred = slope * x_range + intercept
        
        # Create scatter plot
        fig = px.scatter(
            complete_data,
            x='consumption',
            y='suicide_rate',
            color='region',
            hover_name='country',
            hover_data={
                'consumption': ':.1f',
                'suicide_rate': ':.1f',
                'region': False
            },
            title='Alcohol Consumption vs. Suicide Rates by Country (Males)',
            labels={
                'consumption': 'Alcohol Consumption (Litres per capita, 2022)',
                'suicide_rate': 'Suicide Rate (per 100,000 population, males)'
            },
            color_discrete_map=REGION_COLORS
        )
        
        # Add regression line
        fig.add_trace(
            go.Scatter(
                x=x_range,
                y=y_pred,
                mode='lines',
                name=f'Regression Line (R² = {r_squared:.3f})',
                line=dict(color='red', dash='dash', width=2),
                hovertemplate='<b>Regression Line</b><br>R² = {:.3f}<br>p-value = {:.3f}<extra></extra>'.format(r_squared, p_value)
            )
        )
        
        fig.update_layout(
            title={
                'text': 'Alcohol Consumption vs. Suicide Rates by Country (Males)<br><sub>Each point represents a country</sub>',
                'x': 0.5,
                'font': {'size': 16}
            },
            legend_title='WHO Region',
            width=1000,
            height=600
        )
        
        # Save interactive plot
        fig.write_html(f'{self.output_dir}/Fig4_Suicide_alcohol_correlation.html')
        
        return fig
    
    def create_gender_comparison(self, disorder_data):
        """
        Create gender comparison visualization for alcohol disorders.
        
        Parameters:
        disorder_data (DataFrame): Alcohol disorder data by gender
        
        Returns:
        plotly.graph_objects.Figure: Gender comparison chart
        """
        if disorder_data is None or len(disorder_data) == 0:
            print("No disorder data available for gender comparison.")
            return None
        
        # Prepare data for gender comparison
        gender_map = {0: 'Both sexes', 1: 'Male', 2: 'Female'}
        disorder_data_viz = disorder_data.copy()
        disorder_data_viz['gender_name'] = disorder_data_viz['gender'].map(gender_map)
        
        # Calculate regional averages by gender
        regional_gender_avg = disorder_data_viz.groupby(['region', 'gender_name'])['alcohol_disorder'].mean().reset_index()
        
        fig = px.bar(
            regional_gender_avg,
            x='region',
            y='alcohol_disorder',
            color='gender_name',
            title='Alcohol Use Disorders by WHO Region and Gender',
            labels={
                'alcohol_disorder': 'Prevalence of Alcohol Use Disorders (%)',
                'region': 'WHO Region',
                'gender_name': 'Gender'
            },
            barmode='group'
        )
        
        fig.update_layout(
            title={
                'text': 'Alcohol Use Disorders by WHO Region and Gender<br><sub>Average prevalence across countries in each region</sub>',
                'x': 0.5,
                'font': {'size': 16}
            },
            xaxis_title="WHO Region",
            yaxis_title="Prevalence of Alcohol Use Disorders (%)",
            xaxis={'tickangle': 45},
            width=1000,
            height=600,
            legend_title="Gender"
        )
        
        # Save visualization
        fig.write_html(f'{self.output_dir}/Fig8_Gender_comparison_analysis.html')
        
        return fig
    
    def create_clustering_visualization(self, clustering_data):
        """
        Create clustering visualization.
        
        Parameters:
        clustering_data (DataFrame): Data with cluster assignments
        
        Returns:
        plotly.graph_objects.Figure: Clustering visualization
        """
        if clustering_data.empty:
            print("No clustering data available.")
            return None
        
        # Create scatter plot with cluster colors
        fig = px.scatter(
            clustering_data,
            x='consumption',
            y='alcohol_disorder',
            color='cluster',
            hover_name='country',
            hover_data={'region': True, 'consumption': ':.1f', 'alcohol_disorder': ':.1f'},
            title='Country Clustering Based on Alcohol Patterns',
            labels={
                'consumption': 'Alcohol Consumption (Litres per capita)',
                'alcohol_disorder': 'Alcohol Use Disorders (%)',
                'cluster': 'Cluster'
            },
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            title={
                'text': 'Country Clustering Based on Alcohol Patterns<br><sub>K-means clustering of countries by consumption and disorders</sub>',
                'x': 0.5,
                'font': {'size': 16}
            },
            width=1000,
            height=600
        )
        
        # Save visualization
        fig.write_html(f'{self.output_dir}/Fig9_Clustering_analysis.html')
        
        return fig
    
    def create_comprehensive_dashboard(self, data_processor):
        """
        Create comprehensive dashboard with all available indicators.
        
        Parameters:
        data_processor: WHODataProcessor instance with all data
        
        Returns:
        plotly.graph_objects.Figure: Comprehensive dashboard
        """
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Regional Alcohol Consumption', 'Top 10 vs Bottom 10 Countries',
                'Alcohol Disorders by Gender', 'Suicide Rates by Region',
                'Alcohol-Suicide Correlation', 'Trends Over Time'
            ),
            specs=[
                [{"type": "bar"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "bar"}],
                [{"type": "scatter"}, {"type": "scatter"}]
            ]
        )
        
        # 1. Regional averages
        if data_processor.alcohol_consumption is not None and '2022' in data_processor.alcohol_consumption.columns:
            regional_avg = data_processor.alcohol_consumption.groupby('region')['2022'].mean().sort_values(ascending=False)
            fig.add_trace(
                go.Bar(
                    x=regional_avg.index,
                    y=regional_avg.values,
                    name="Regional Avg",
                    marker_color='steelblue'
                ),
                row=1, col=1
            )
        
        # 2. Top vs Bottom countries
        if data_processor.alcohol_consumption is not None and '2022' in data_processor.alcohol_consumption.columns:
            sorted_data = data_processor.alcohol_consumption[['country', '2022']].dropna().sort_values('2022')
            top5 = sorted_data.tail(5)
            bottom5 = sorted_data.head(5)
            
            fig.add_trace(
                go.Bar(
                    x=top5['country'],
                    y=top5['2022'],
                    name="Top 5",
                    marker_color="darkred"
                ),
                row=1, col=2
            )
            fig.add_trace(
                go.Bar(
                    x=bottom5['country'],
                    y=bottom5['2022'],
                    name="Bottom 5",
                    marker_color="lightblue"
                ),
                row=1, col=2
            )
        
        # 3. Alcohol disorders by gender
        if data_processor.alcohol_disorder is not None:
            gender_map = {1: 'Male', 2: 'Female'}
            gender_avg = data_processor.alcohol_disorder[data_processor.alcohol_disorder['gender'].isin([1, 2])]
            gender_summary = gender_avg.groupby('gender')['alcohol_disorder'].mean()
            
            fig.add_trace(
                go.Bar(
                    x=[gender_map[g] for g in gender_summary.index],
                    y=gender_summary.values,
                    name="By Gender",
                    marker_color=['blue', 'pink']
                ),
                row=2, col=1
            )
        
        # 4. Suicide rates by region (if available)
        if (hasattr(data_processor, 'suicide_data') and 
            data_processor.suicide_data is not None and 
            len(data_processor.suicide_data) > 0):
            
            suicide_regional = data_processor.suicide_data[
                data_processor.suicide_data['gender'] == 1
            ].groupby('region')['suicide_rate'].mean().sort_values(ascending=False)
            
            fig.add_trace(
                go.Bar(
                    x=suicide_regional.index,
                    y=suicide_regional.values,
                    name="Suicide Rates",
                    marker_color='crimson'
                ),
                row=2, col=2
            )
        
        # 5. Alcohol-suicide correlation (if available)
        if (hasattr(data_processor, 'comprehensive_data') and 
            data_processor.comprehensive_data is not None):
            
            complete_data = data_processor.comprehensive_data[
                data_processor.comprehensive_data['consumption'].notna() &
                data_processor.comprehensive_data['suicide_rate'].notna() &
                (data_processor.comprehensive_data['gender'] == 1)
            ]
            
            if len(complete_data) >= 5:
                fig.add_trace(
                    go.Scatter(
                        x=complete_data['consumption'],
                        y=complete_data['suicide_rate'],
                        mode='markers',
                        name="Countries",
                        text=complete_data['country'],
                        marker=dict(color='orange', size=8)
                    ),
                    row=3, col=1
                )
        
        # 6. Time trends for selected countries
        if data_processor.alcohol_consumption is not None:
            selected_countries = ['France', 'Germany', 'United States of America', 'Russian Federation']
            year_cols = [col for col in data_processor.alcohol_consumption.columns if str(col).isdigit()]
            years = sorted([int(col) for col in year_cols])
            
            for country in selected_countries:
                country_data = data_processor.alcohol_consumption[
                    data_processor.alcohol_consumption['country'] == country
                ]
                if not country_data.empty:
                    values = [
                        country_data[str(year)].iloc[0] if str(year) in country_data.columns 
                        else None for year in years
                    ]
                    fig.add_trace(
                        go.Scatter(
                            x=years,
                            y=values,
                            mode='lines+markers',
                            name=country,
                            line=dict(width=2)
                        ),
                        row=3, col=2
                    )
        
        # Update layout
        fig.update_layout(
            height=1000,
            showlegend=True,
            title_text="WHO Alcohol & Mental Health Comprehensive Dashboard",
            title_x=0.5,
            title_font_size=20
        )
        
        # Save dashboard
        fig.write_html(f'{self.output_dir}/Comprehensive_Dashboard.html')
        
        return fig
    
    def create_dashboard(self, consumption_data):
        """
        Create a dashboard with multiple visualizations (legacy method for compatibility).
        
        Parameters:
        consumption_data (DataFrame): Alcohol consumption data
        
        Returns:
        plotly.graph_objects.Figure: Dashboard figure
        """
        if consumption_data is None or '2022' not in consumption_data.columns:
            return None
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Regional Averages 2022', 'Consumption Distribution', 
                          'Top 5 vs Bottom 5', 'Trend Over Time (Selected Countries)'),
            specs=[[{"type": "bar"}, {"type": "histogram"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Regional averages
        regional_avg = consumption_data.groupby('region')['2022'].mean().sort_values(ascending=False)
        fig.add_trace(
            go.Bar(x=regional_avg.index, y=regional_avg.values, name="Regional Avg"),
            row=1, col=1
        )
        
        # Distribution histogram
        consumption_2022 = consumption_data['2022'].dropna()
        fig.add_trace(
            go.Histogram(x=consumption_2022, nbinsx=20, name="Distribution"),
            row=1, col=2
        )
        
        # Top 5 vs Bottom 5
        sorted_data = consumption_data[['country', '2022']].dropna().sort_values('2022')
        top5 = sorted_data.tail(5)
        bottom5 = sorted_data.head(5)
        
        fig.add_trace(
            go.Bar(x=top5['country'], y=top5['2022'], name="Top 5", marker_color="red"),
            row=2, col=1
        )
        fig.add_trace(
            go.Bar(x=bottom5['country'], y=bottom5['2022'], name="Bottom 5", marker_color="lightblue"),
            row=2, col=1
        )
        
        # Time trend for selected countries
        selected_countries = ['France', 'Germany', 'United States of America', 'Russian Federation']
        year_cols = [col for col in consumption_data.columns if str(col).isdigit()]
        years = sorted([int(col) for col in year_cols])
        
        for country in selected_countries:
            country_data = consumption_data[consumption_data['country'] == country]
            if not country_data.empty:
                values = [country_data[str(year)].iloc[0] if str(year) in country_data.columns else None 
                         for year in years]
                fig.add_trace(
                    go.Scatter(x=years, y=values, mode='lines+markers', name=country),
                    row=2, col=2
                )
        
        fig.update_layout(height=800, showlegend=True, title_text="Alcohol Consumption Dashboard")
        
        return fig
    
    def create_regional_comparison_interactive(self, regional_data):
        """
        Create interactive regional comparison chart.
        
        Parameters:
        regional_data (DataFrame): Regional averages data
        
        Returns:
        plotly.graph_objects.Figure: Interactive bar chart
        """
        fig = px.bar(
            regional_data,
            x='Region',
            y='Average_Consumption',
            title='Average Alcohol Consumption by WHO Region (2022)',
            labels={'Average_Consumption': 'Average Consumption (Litres)', 'Region': 'WHO Region'},
            hover_data={'Number_of_Countries': True},
            color='Average_Consumption',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            title={'x': 0.5, 'font': {'size': 16}},
            xaxis_title="WHO Region",
            yaxis_title="Average Alcohol Consumption (Litres)",
            xaxis={'tickangle': 45},
            width=800,
            height=500
        )
        
        return fig
        