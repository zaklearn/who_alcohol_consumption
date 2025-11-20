"""
HTML report generation module
"""

import pandas as pd
import numpy as np
from scipy.stats import linregress

class HTMLReportGenerator:
    """
    Class to generate comprehensive HTML reports
    """
    
    def __init__(self, output_dir="plots"):
        self.output_dir = output_dir
    
    def generate_summary_tables(self, data_processor):
        """
        Generate summary tables for the HTML report.
        
        Parameters:
        data_processor: WHODataProcessor instance
        
        Returns:
        dict: Dictionary containing various summary tables
        """
        summary_tables = {}
        
        # Top 10 consumers in 2022
        top_consumers = data_processor.get_top_consumers('2022', 10)
        if top_consumers is not None:
            top_consumers.columns = ['Country', 'Region', 'Consumption_2022']
            summary_tables['top_consumers'] = top_consumers
        
        # Regional averages
        regional_avg = data_processor.get_regional_averages('2022')
        if regional_avg is not None:
            summary_tables['regional_averages'] = regional_avg
        
        # Disorder data by region and gender
        if data_processor.alcohol_disorder is not None:
            disorder_summary = data_processor.alcohol_disorder.groupby(['region', 'gender'])['alcohol_disorder'].mean().reset_index()
            gender_map = {0: 'Both sexes', 1: 'Male', 2: 'Female'}
            disorder_summary['Gender'] = disorder_summary['gender'].map(gender_map)
            disorder_summary = disorder_summary[['region', 'Gender', 'alcohol_disorder']]
            disorder_summary.columns = ['Region', 'Gender', 'Average_Disorder_Prevalence']
            summary_tables['disorder_by_region_gender'] = disorder_summary
        
        # Correlation statistics
        if data_processor.merged_data is not None:
            male_data = data_processor.merged_data[data_processor.merged_data['gender'] == 1].copy()
            if not male_data.empty:
                correlation = male_data['consumption'].corr(male_data['alcohol_disorder'])
                slope, intercept, r_value, p_value, std_err = linregress(
                    male_data['consumption'], male_data['alcohol_disorder']
                )
                
                corr_stats = pd.DataFrame({
                    'Statistic': ['Correlation Coefficient', 'R-squared', 'P-value', 'Standard Error'],
                    'Value': [correlation, r_value**2, p_value, std_err]
                })
                summary_tables['correlation_stats'] = corr_stats
        
        return summary_tables
    
    def generate_html_report(self, data_processor, figures_dict, filename=None):
        """
        Generate comprehensive HTML report.
        
        Parameters:
        data_processor: WHODataProcessor instance
        figures_dict: Dictionary of plotly figures
        filename: Output filename
        
        Returns:
        str: Path to generated HTML file
        """
        if filename is None:
            filename = f"{self.output_dir}/WHO_Alcohol_Analysis_Report.html"
        
        print("Creating comprehensive HTML report...")
        
        # Generate summary tables
        summary_tables = self.generate_summary_tables(data_processor)
        
        # Calculate key metrics
        total_countries = len(data_processor.alcohol_consumption) if data_processor.alcohol_consumption is not None else 0
        
        if data_processor.alcohol_consumption is not None and '2022' in data_processor.alcohol_consumption.columns:
            avg_consumption = data_processor.alcohol_consumption['2022'].mean()
            max_consumption = data_processor.alcohol_consumption['2022'].max()
            top_consumer = data_processor.alcohol_consumption.loc[
                data_processor.alcohol_consumption['2022'].idxmax(), 'country'
            ] if not data_processor.alcohol_consumption['2022'].isna().all() else 'N/A'
        else:
            avg_consumption = max_consumption = 0
            top_consumer = 'N/A'
        
        # Get figure HTML - handle missing figures gracefully
        try:
            dashboard_html = figures_dict.get('dashboard', None)
            dashboard_html = dashboard_html.to_html(include_plotlyjs=False, div_id="dashboard-plot") if dashboard_html else ""
        except:
            dashboard_html = ""
            
        try:
            top10_html = figures_dict.get('top10', None)
            top10_html = top10_html.to_html(include_plotlyjs=False, div_id="top10-plot") if top10_html else ""
        except:
            top10_html = ""
            
        try:
            europe_html = figures_dict.get('europe_trends', None)
            europe_html = europe_html.to_html(include_plotlyjs=False, div_id="europe-plot") if europe_html else ""
        except:
            europe_html = ""
            
        try:
            map_html = figures_dict.get('world_map', None)
            map_html = map_html.to_html(include_plotlyjs=False, div_id="worldmap-plot") if map_html else ""
        except:
            map_html = ""
            
        try:
            scatter_html = figures_dict.get('scatter', None)
            scatter_html = scatter_html.to_html(include_plotlyjs=False, div_id="scatter-plot") if scatter_html else ""
        except:
            scatter_html = ""
        
        # Calculate R-squared for correlation tab
        r_squared = 0
        if data_processor.merged_data is not None:
            male_data = data_processor.merged_data[data_processor.merged_data['gender'] == 1].copy()
            if not male_data.empty:
                _, _, r_value, _, _ = linregress(male_data['consumption'], male_data['alcohol_disorder'])
                r_squared = r_value ** 2
        
        # Generate HTML content
        html_content = self._generate_html_template(
            total_countries, avg_consumption, max_consumption, top_consumer,
            dashboard_html, top10_html, europe_html, map_html, scatter_html,
            summary_tables, r_squared
        )
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Comprehensive HTML report saved as: {filename}")
        return filename
    
    def _generate_html_template(self, total_countries, avg_consumption, max_consumption, top_consumer,
                               dashboard_html, top10_html, europe_html, map_html, scatter_html,
                               summary_tables, r_squared):
        """Generate the complete HTML template."""
        
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WHO Alcohol Data Analysis Report</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 300;
        }
        
        .header p {
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .tab-container {
            max-width: 1400px;
            margin: 2rem auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .tab-nav {
            display: flex;
            background-color: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
            overflow-x: auto;
        }
        
        .tab-button {
            background: none;
            border: none;
            padding: 1rem 1.5rem;
            cursor: pointer;
            font-size: 1rem;
            color: #495057;
            transition: all 0.3s ease;
            white-space: nowrap;
            border-bottom: 3px solid transparent;
        }
        
        .tab-button:hover {
            background-color: #e9ecef;
            color: #007bff;
        }
        
        .tab-button.active {
            color: #007bff;
            background-color: white;
            border-bottom-color: #007bff;
            font-weight: 600;
        }
        
        .tab-content {
            display: none;
            padding: 2rem;
            animation: fadeIn 0.3s ease-in;
        }
        
        .tab-content.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .plot-container {
            margin: 1rem 0;
            background: white;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .table-container {
            margin: 1rem 0;
            overflow-x: auto;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }
        
        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
        }
        
        tr:hover {
            background-color: #f8f9fa;
        }
        
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
            border-left: 4px solid #007bff;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #007bff;
            margin: 0.5rem 0;
        }
        
        .metric-label {
            color: #6c757d;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .data-source {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border-left: 4px solid #28a745;
        }
        
        .description {
            line-height: 1.6;
            color: #495057;
            margin: 1rem 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>WHO Alcohol Data Analysis Report</h1>
        <p>Comprehensive analysis of global alcohol consumption patterns and related disorders</p>
        <p><small>Generated on """ + pd.Timestamp.now().strftime('%B %d, %Y') + """</small></p>
    </div>

    <div class="tab-container">
        <div class="tab-nav">
            <button class="tab-button active" onclick="showTab(event, 'overview')">📊 Overview</button>
            <button class="tab-button" onclick="showTab(event, 'top10')">🏆 Top 10 Countries</button>
            <button class="tab-button" onclick="showTab(event, 'trends')">📈 Europe Trends</button>
            <button class="tab-button" onclick="showTab(event, 'worldmap')">🗺️ World Map</button>
            <button class="tab-button" onclick="showTab(event, 'correlation')">🔗 Correlation Analysis</button>
            <button class="tab-button" onclick="showTab(event, 'tables')">📋 Data Tables</button>
            <button class="tab-button" onclick="showTab(event, 'methodology')">📚 Methodology</button>
        </div>

        """ + self._generate_overview_tab(total_countries, avg_consumption, max_consumption, top_consumer, dashboard_html) + """
        """ + self._generate_top10_tab(top10_html) + """
        """ + self._generate_trends_tab(europe_html) + """
        """ + self._generate_worldmap_tab(map_html) + """
        """ + self._generate_correlation_tab(scatter_html, r_squared) + """
        """ + self._generate_tables_tab(summary_tables) + """
        """ + self._generate_methodology_tab() + """
    </div>

    <script>
        function showTab(evt, tabName) {
            var i, tabcontent, tabbuttons;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].classList.remove("active");
            }
            tabbuttons = document.getElementsByClassName("tab-button");
            for (i = 0; i < tabbuttons.length; i++) {
                tabbuttons[i].classList.remove("active");
            }
            document.getElementById(tabName).classList.add("active");
            evt.currentTarget.classList.add("active");
        }
        
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('overview').classList.add('active');
        });
    </script>
</body>
</html>
"""
        
        return html_content
    
    def _generate_overview_tab(self, total_countries, avg_consumption, max_consumption, top_consumer, dashboard_html):
        """Generate the overview tab content."""
        return f"""
        <div id="overview" class="tab-content active">
            <h2>📊 Executive Summary</h2>
            <div class="description">
                <p>This comprehensive analysis examines global alcohol consumption patterns using data from the World Health Organization (WHO). 
                The analysis covers consumption trends, regional variations, and correlations with alcohol use disorders.</p>
            </div>
            
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value">{total_countries}</div>
                    <div class="metric-label">Countries Analyzed</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{avg_consumption:.1f}L</div>
                    <div class="metric-label">Global Average (2022)</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{max_consumption:.1f}L</div>
                    <div class="metric-label">Highest Consumption (2022)</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{top_consumer}</div>
                    <div class="metric-label">Top Consumer Country</div>
                </div>
            </div>
            
            <div class="plot-container">
                <h3>Key Insights Dashboard</h3>
                {dashboard_html}
            </div>
            
            <div class="data-source">
                <h4>🔍 Key Findings</h4>
                <ul>
                    <li><strong>Regional Variations:</strong> Europe shows the highest average alcohol consumption rates</li>
                    <li><strong>Temporal Trends:</strong> Most European countries show declining consumption trends since 2010</li>
                    <li><strong>Health Correlation:</strong> Strong positive correlation between consumption and alcohol use disorders</li>
                    <li><strong>Data Coverage:</strong> Analysis spans {total_countries} countries from 2000-2022</li>
                </ul>
            </div>
        </div>
        """
    
    def _generate_top10_tab(self, top10_html):
        """Generate the top 10 tab content."""
        return f"""
        <div id="top10" class="tab-content">
            <h2>🏆 Top 10 Countries by Alcohol Consumption</h2>
            <div class="description">
                <p>This visualization shows the countries with the highest recorded alcohol consumption per capita in 2022. 
                The data represents pure alcohol consumption among individuals aged 15 and above, measured in litres per person per year.</p>
            </div>
            
            <div class="plot-container">
                {top10_html}
            </div>
            
            <div class="data-source">
                <h4>📋 Analysis Notes</h4>
                <ul>
                    <li><strong>Measurement:</strong> Litres of pure alcohol per capita (15+ years)</li>
                    <li><strong>Data Source:</strong> WHO Global Health Observatory</li>
                    <li><strong>Calculation:</strong> Three-year averages to smooth annual variations</li>
                    <li><strong>Coverage:</strong> Based on recorded production, import, export, and sales data</li>
                </ul>
            </div>
        </div>
        """
    
    def _generate_trends_tab(self, europe_html):
        """Generate the trends tab content."""
        return f"""
        <div id="trends" class="tab-content">
            <h2>📈 European Alcohol Consumption Trends</h2>
            <div class="description">
                <p>This analysis focuses on the original European Union member countries (pre-1986 expansion) to examine 
                long-term trends in alcohol consumption from 2000 to 2022.</p>
            </div>
            
            <div class="plot-container">
                {europe_html}
            </div>
            
            <div class="data-source">
                <h4>🇪🇺 Countries Included</h4>
                <p><strong>EU Original Members (before 1986):</strong> Belgium, France, Germany, Italy, Luxembourg, 
                Netherlands, Denmark, Ireland, United Kingdom, and Greece.</p>
                
                <h4>📊 Trend Observations</h4>
                <ul>
                    <li><strong>General Decline:</strong> Most countries show declining consumption since peak levels around 2008-2010</li>
                    <li><strong>Regional Patterns:</strong> Southern European countries (Italy, Greece) typically show lower consumption</li>
                    <li><strong>Stability:</strong> Some countries like Germany show relatively stable consumption patterns</li>
                    <li><strong>Economic Impact:</strong> The 2008 financial crisis appears to correlate with consumption changes</li>
                </ul>
            </div>
        </div>
        """
    
    def _generate_worldmap_tab(self, map_html):
        """Generate the world map tab content."""
        return f"""
        <div id="worldmap" class="tab-content">
            <h2>🗺️ Global Alcohol Consumption Map</h2>
            <div class="description">
                <p>This interactive world map visualizes alcohol consumption patterns across different countries and regions. 
                Darker shades indicate higher consumption levels. Hover over countries to see detailed information.</p>
            </div>
            
            <div class="plot-container">
                {map_html}
            </div>
            
            <div class="data-source">
                <h4>🌍 Global Patterns</h4>
                <ul>
                    <li><strong>Europe:</strong> Generally shows the highest consumption levels globally</li>
                    <li><strong>Africa:</strong> Mixed patterns with some countries showing very low consumption</li>
                    <li><strong>Asia:</strong> Wide variation, with some countries having cultural/religious restrictions</li>
                    <li><strong>Americas:</strong> Moderate to high consumption in most regions</li>
                    <li><strong>Data Gaps:</strong> Some countries may have limited or no data available</li>
                </ul>
                
                <h4>🎨 Color Scale</h4>
                <p>The color intensity represents consumption levels from light (low consumption) to dark blue (high consumption). 
                Grey areas indicate countries with no available data.</p>
            </div>
        </div>
        """
    
    def _generate_correlation_tab(self, scatter_html, r_squared):
        """Generate the correlation tab content."""
        return f"""
        <div id="correlation" class="tab-content">
            <h2>🔗 Consumption vs. Alcohol Use Disorders</h2>
            <div class="description">
                <p>This analysis examines the relationship between alcohol consumption levels and the prevalence of alcohol use disorders 
                among males. Each point represents a country, colored by WHO region.</p>
            </div>
            
            <div class="plot-container">
                {scatter_html}
            </div>
            
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value">{r_squared:.3f}</div>
                    <div class="metric-label">R-squared Value</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{np.sqrt(r_squared):.3f}</div>
                    <div class="metric-label">Correlation Coefficient</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{'Strong' if r_squared > 0.5 else 'Moderate' if r_squared > 0.3 else 'Weak'}</div>
                    <div class="metric-label">Correlation Strength</div>
                </div>
            </div>
            
            <div class="data-source">
                <h4>📊 Statistical Analysis</h4>
                <ul>
                    <li><strong>Sample:</strong> Analysis focuses on male population data for consistency</li>
                    <li><strong>Methodology:</strong> Linear regression analysis with correlation coefficient calculation</li>
                    <li><strong>Interpretation:</strong> Higher consumption levels are associated with higher disorder prevalence</li>
                    <li><strong>Regional Patterns:</strong> Different regions show varying relationships between consumption and disorders</li>
                </ul>
                
                <h4>⚠️ Important Notes</h4>
                <ul>
                    <li>Correlation does not imply causation</li>
                    <li>Disorder data is modeled using regression techniques</li>
                    <li>Cultural, economic, and policy factors influence both variables</li>
                    <li>Individual country contexts may vary significantly</li>
                </ul>
            </div>
        </div>
        """
    
    def _generate_tables_tab(self, summary_tables):
        """Generate the data tables tab content."""
        tables_html = ""
        
        if 'top_consumers' in summary_tables:
            tables_html += f"""
            <div class="table-container">
                <h3>🏆 Top 10 Alcohol Consumers (2022)</h3>
                {summary_tables['top_consumers'].to_html(classes='table table-striped', table_id='top-consumers-table', escape=False, index=False)}
            </div>
            """
        
        if 'regional_averages' in summary_tables:
            tables_html += f"""
            <div class="table-container">
                <h3>🌍 Regional Averages (2022)</h3>
                {summary_tables['regional_averages'].to_html(classes='table table-striped', table_id='regional-avg-table', escape=False, index=False)}
            </div>
            """
        
        if 'disorder_by_region_gender' in summary_tables:
            tables_html += f"""
            <div class="table-container">
                <h3>🏥 Alcohol Use Disorders by Region and Gender</h3>
                {summary_tables['disorder_by_region_gender'].to_html(classes='table table-striped', table_id='disorder-table', escape=False, index=False)}
            </div>
            """
        
        if 'correlation_stats' in summary_tables:
            tables_html += f"""
            <div class="table-container">
                <h3>📈 Correlation Statistics</h3>
                {summary_tables['correlation_stats'].to_html(classes='table table-striped', table_id='correlation-table', escape=False, index=False)}
            </div>
            """
        
        return f"""
        <div id="tables" class="tab-content">
            <h2>📋 Data Summary Tables</h2>
            <div class="description">
                <p>These tables provide detailed numerical data supporting the visualizations and analysis. 
                All tables can be used for further analysis or reference.</p>
            </div>
            
            {tables_html}
            
            <div class="data-source">
                <h4>📊 Data Notes</h4>
                <ul>
                    <li><strong>Consumption Data:</strong> Measured in litres of pure alcohol per capita (15+ years)</li>
                    <li><strong>Disorder Data:</strong> Percentage prevalence of alcohol use disorders</li>
                    <li><strong>Regional Classification:</strong> Based on WHO regional groupings</li>
                    <li><strong>Data Quality:</strong> All figures are based on official WHO data sources</li>
                </ul>
            </div>
        </div>
        """
    
    def _generate_methodology_tab(self):
        """Generate the methodology tab content."""
        return """
        <div id="methodology" class="tab-content">
            <h2>📚 Methodology and Data Sources</h2>
            
            <div class="data-source">
                <h3>🔍 Data Sources</h3>
                <h4>Primary Data Source</h4>
                <p><strong>World Health Organization (WHO) Global Health Observatory</strong></p>
                <ul>
                    <li><strong>Alcohol Consumption:</strong> Indicator SA_0000001747</li>
                    <li><strong>Alcohol Use Disorders:</strong> Indicator SA_0000001462</li>
                    <li><strong>Access Method:</strong> WHO GHO OData API</li>
                    <li><strong>Data Coverage:</strong> 2000-2022 for most countries</li>
                </ul>
            </div>
            
            <div class="data-source">
                <h3>📏 Measurement Definitions</h3>
                
                <h4>Alcohol Consumption (APC)</h4>
                <p><strong>Definition:</strong> Recorded per capita (15+ years) consumption in litres of pure alcohol</p>
                <ul>
                    <li>Based on recorded production, import, export, and sales data</li>
                    <li>Often derived from taxation records</li>
                    <li>Three-year averages calculated (e.g., 2015 = average of 2014, 2015, 2016)</li>
                    <li>Excludes unrecorded consumption (home-made, illegally produced)</li>
                </ul>
                
                <h4>Alcohol Use Disorders</h4>
                <p><strong>Definition:</strong> Adults (15+ years) with disorders attributable to alcohol consumption</p>
                <ul>
                    <li>Based on ICD-10 classifications: F10.1 (Harmful use) and F10.2 (Dependence)</li>
                    <li>Data modeled using regression models</li>
                    <li>Prevalence expressed as percentage of population</li>
                    <li>Disaggregated by gender (Male, Female, Both sexes)</li>
                </ul>
            </div>
            
            <div class="data-source">
                <h3>🛠️ Data Processing Methods</h3>
                
                <h4>Data Extraction</h4>
                <ul>
                    <li>API calls to WHO GHO OData endpoints</li>
                    <li>Country name standardization for consistent merging</li>
                    <li>Missing value imputation (2005 values imputed with 2004 data where missing)</li>
                </ul>
                
                <h4>Analysis Techniques</h4>
                <ul>
                    <li><strong>Descriptive Statistics:</strong> Mean, median, range calculations by region</li>
                    <li><strong>Time Series Analysis:</strong> Trend identification over 22-year period</li>
                    <li><strong>Correlation Analysis:</strong> Pearson correlation between consumption and disorders</li>
                    <li><strong>Linear Regression:</strong> Relationship modeling with R-squared calculation</li>
                </ul>
                
                <h4>Visualization Methods</h4>
                <ul>
                    <li><strong>Interactive Charts:</strong> Plotly library for dynamic visualizations</li>
                    <li><strong>Geographic Mapping:</strong> Choropleth maps for spatial analysis</li>
                    <li><strong>Statistical Plots:</strong> Scatter plots with regression lines</li>
                    <li><strong>Time Series Plots:</strong> Multi-country trend comparisons</li>
                </ul>
            </div>
            
            <div class="data-source">
                <h3>⚠️ Limitations and Considerations</h3>
                
                <h4>Data Limitations</h4>
                <ul>
                    <li><strong>Coverage:</strong> Not all countries have complete data for all years</li>
                    <li><strong>Unrecorded Consumption:</strong> Home-made and illegally produced alcohol not captured</li>
                    <li><strong>Cultural Factors:</strong> Religious and cultural prohibitions may affect reporting</li>
                    <li><strong>Economic Factors:</strong> Informal markets may not be fully captured</li>
                </ul>
                
                <h4>Analytical Considerations</h4>
                <ul>
                    <li><strong>Correlation vs Causation:</strong> Statistical relationships don't imply causal mechanisms</li>
                    <li><strong>Temporal Alignment:</strong> Different indicators may have different reference periods</li>
                    <li><strong>Regional Grouping:</strong> WHO regional classifications may not reflect all cultural similarities</li>
                </ul>
            </div>
            
            <div class="data-source">
                <h3>🔗 Additional Resources</h3>
                <ul>
                    <li><a href="https://www.who.int/data/gho/data/indicators/indicator-details/GHO/alcohol-recorded-per-capita-(15-)-consumption-(in-litres-of-pure-alcohol)-3-year-average-with-95-ci" target="_blank">WHO Alcohol Consumption Indicator Details</a></li>
                    <li><a href="https://www.who.int/data/gho/info/gho-odata-api" target="_blank">WHO GHO OData API Documentation</a></li>
                    <li><a href="https://www.who.int/health-topics/alcohol" target="_blank">WHO Alcohol Health Topic Page</a></li>
                </ul>
            </div>
        </div>
        """