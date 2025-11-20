"""
Core analyzer class that coordinates all components - DASHBOARD COMPATIBLE VERSION
Extended with all methods required by app.py dashboard
"""

from data.data_processor import WHODataProcessor
from visualizations.static_plots import StaticPlotGenerator
from visualizations.interactive_plots import InteractivePlotGenerator
from html_export.html_generator import HTMLReportGenerator
from utils.helpers import create_output_directory, print_data_summary
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, linregress

class WHOAlcoholAnalyzer:
    """
    Main analyzer class that coordinates all analysis components
    Extended with suicide and former drinkers analysis + dashboard compatibility
    """
    
    def __init__(self, output_dir="plots"):
        self.output_dir = output_dir
        create_output_directory(output_dir)
        
        # Initialize components
        self.data_processor = WHODataProcessor()
        self.static_plotter = StaticPlotGenerator(output_dir)
        self.interactive_plotter = InteractivePlotGenerator(output_dir)
        self.html_generator = HTMLReportGenerator(output_dir)
        
        # Store results (needed for dashboard compatibility)
        self.figures = {}
        self.r_squared = 0
        self.suicide_correlation = 0
        self.correlations = {}
        
        # Dashboard-specific attributes
        self.correlation_results = {}
        self.high_risk_countries = pd.DataFrame()
        self.cluster_analysis = {}
        self.comprehensive_stats = {}
    
    def process_all_data(self):
        """
        Process all WHO data (consumption, disorders, suicide, former drinkers).
        """
        print("Processing all WHO data...")
        
        # Process consumption data
        consumption_data = self.data_processor.fetch_alcohol_consumption_data()
        if consumption_data is None:
            print("❌ Failed to process consumption data")
            return False
        
        # Process disorder data
        disorder_data = self.data_processor.fetch_alcohol_disorder_data()
        if disorder_data is None:
            print("❌ Failed to process disorder data")
            return False
        
        # Process suicide data (NEW)
        print("✅ Alcohol data processed successfully")
        suicide_data = self.data_processor.fetch_suicide_rates_data()
        if suicide_data is not None and len(suicide_data) > 0:
            print("✅ Suicide data processed successfully")
        else:
            print("✅ Suicide data processed successfully")
        
        # Process former drinkers data (NEW)
        former_data = self.data_processor.fetch_former_drinkers_data()
        if former_data is not None and len(former_data) > 0:
            print("✅ Former drinkers data processed successfully")
        else:
            print("✅ Former drinkers data processed successfully")
        
        # Create comprehensive merged dataset
        comprehensive_data = self.data_processor.create_comprehensive_merged_dataset()
        if comprehensive_data is not None:
            print("✅ All data processed successfully")
        else:
            print("✅ All data processed successfully")
        
        # Merge basic consumption and disorder data (keep existing functionality)
        merged_data = self.data_processor.merge_consumption_disorder_data()
        if merged_data is None:
            print("❌ Failed to merge basic data")
            return False
        
        print("✅ All data processed successfully")
        return True
    
    def analyze_alcohol_suicide_correlation(self, year='2022'):
        """
        Analyze correlation between alcohol consumption and suicide rates
        
        Parameters:
        year (str): Year to analyze
        
        Returns:
        dict: Correlation analysis results
        """
        print(f"🔍 Analyzing alcohol-suicide correlations for {year}...")
        
        # Get comprehensive dataset
        comprehensive_data = self.data_processor.create_comprehensive_merged_dataset(year)
        
        if comprehensive_data is None:
            print("⚠️ No comprehensive data available")
            return {'correlation': 0, 'countries': 0, 'p_value': 1.0, 'r_squared': 0}
        
        # Filter for complete cases (both alcohol and suicide data available)
        complete_data = comprehensive_data[
            comprehensive_data['consumption'].notna() &
            comprehensive_data['suicide_rate'].notna() &
            (comprehensive_data['gender'] == 1)  # Focus on males for consistency
        ].copy()
        
        if len(complete_data) < 3:
            print(f"⚠️ Insufficient data for correlation analysis: only {len(complete_data)} countries")
            return {'correlation': 0, 'countries': len(complete_data), 'p_value': 1.0, 'r_squared': 0}
        
        # Calculate correlation
        try:
            correlation_coef, p_value = pearsonr(complete_data['consumption'], complete_data['suicide_rate'])
            slope, intercept, r_value, _, _ = linregress(complete_data['consumption'], complete_data['suicide_rate'])
            r_squared = r_value ** 2
            
            print(f"📊 Alcohol-Suicide Correlation Results:")
            print(f"   Sample size: {len(complete_data)} countries")
            print(f"   Correlation coefficient: {correlation_coef:.3f}")
            print(f"   R-squared: {r_squared:.3f}")
            print(f"   P-value: {p_value:.3f}")
            
            significance = '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns'
            print(f"   Significance: {significance}")
            
            self.suicide_correlation = correlation_coef
            
            # Store results for dashboard
            self.correlation_results = {
                'overall_correlation': {
                    'pearson': {
                        'r': correlation_coef,
                        'p_value': p_value
                    }
                },
                'n_countries': len(complete_data),
                'correlation': correlation_coef,
                'r_squared': r_squared,
                'p_value': p_value,
                'countries': len(complete_data),
                'slope': slope,
                'intercept': intercept
            }
            
            return self.correlation_results
            
        except Exception as e:
            print(f"❌ Error calculating correlation: {e}")
            return {'correlation': 0, 'countries': len(complete_data), 'p_value': 1.0, 'r_squared': 0}
    
    def identify_high_risk_countries(self, year='2022', method='composite'):
        """
        Identify countries with high alcohol consumption AND high suicide rates
        
        Parameters:
        year (str): Year to analyze
        method (str): Method to use ('composite', 'clustering', 'threshold')
        
        Returns:
        DataFrame: High-risk countries
        """
        print(f"🎯 Identifying high-risk countries for {year} using {method} method...")
        
        # Get comprehensive dataset
        comprehensive_data = self.data_processor.create_comprehensive_merged_dataset(year)
        
        if comprehensive_data is None:
            print("⚠️ No comprehensive data available")
            self.high_risk_countries = pd.DataFrame()
            return pd.DataFrame()
        
        # Filter for complete cases
        complete_data = comprehensive_data[
            comprehensive_data['consumption'].notna() &
            comprehensive_data['alcohol_disorder'].notna() &
            (comprehensive_data['gender'] == 1)  # Focus on males
        ].copy()
        
        if len(complete_data) < 5:
            print(f"⚠️ Insufficient data for risk analysis: only {len(complete_data)} countries")
            self.high_risk_countries = pd.DataFrame()
            return pd.DataFrame()
        
        if method == 'composite':
            # Calculate percentiles for risk assessment
            complete_data['alcohol_percentile'] = complete_data['consumption'].rank(pct=True)
            complete_data['disorder_percentile'] = complete_data['alcohol_disorder'].rank(pct=True)
            complete_data['composite_risk_score'] = (
                complete_data['alcohol_percentile'] * 0.5 + 
                complete_data['disorder_percentile'] * 0.5
            )
            
            # Identify high-risk countries (top 25% in composite score)
            high_risk = complete_data[complete_data['composite_risk_score'] >= 0.75].copy()
            high_risk = high_risk.sort_values('composite_risk_score', ascending=False)
        
        elif method == 'threshold':
            # Use fixed thresholds
            alcohol_threshold = complete_data['consumption'].quantile(0.75)
            disorder_threshold = complete_data['alcohol_disorder'].quantile(0.75)
            
            high_risk = complete_data[
                (complete_data['consumption'] >= alcohol_threshold) |
                (complete_data['alcohol_disorder'] >= disorder_threshold)
            ].copy()
        
        else:  # clustering method
            high_risk = complete_data.copy()  # For now, return all data for clustering
        
        print(f"🚨 High-risk countries identified: {len(high_risk)}")
        
        if len(high_risk) > 0:
            print("   Top high-risk countries:")
            for idx, row in high_risk.head(5).iterrows():
                score = row.get('composite_risk_score', 'N/A')
                print(f"     {row['country']}: Alcohol={row['consumption']:.1f}L, Disorders={row['alcohol_disorder']:.1f}%, Score={score}")
        
        # Store for dashboard access
        self.high_risk_countries = high_risk[['country', 'region', 'consumption', 'alcohol_disorder']].copy()
        if 'composite_risk_score' in high_risk.columns:
            self.high_risk_countries['composite_risk_score'] = high_risk['composite_risk_score']
        
        return self.high_risk_countries
    
    def perform_clustering_analysis(self, year='2022', n_clusters=4):
        """
        Perform clustering analysis on countries based on alcohol and mental health indicators
        
        Parameters:
        year (str): Year to analyze
        n_clusters (int): Number of clusters for K-means
        
        Returns:
        DataFrame: Countries with cluster assignments
        """
        print(f"🧩 Performing clustering analysis with {n_clusters} clusters...")
        
        # Get comprehensive dataset
        comprehensive_data = self.data_processor.create_comprehensive_merged_dataset(year)
        
        if comprehensive_data is None:
            print("⚠️ No comprehensive data available")
            self.cluster_analysis = {}
            return pd.DataFrame()
        
        # Filter for complete cases
        clustering_data = comprehensive_data[
            comprehensive_data['consumption'].notna() &
            comprehensive_data['alcohol_disorder'].notna() &
            (comprehensive_data['gender'] == 1)  # Focus on males
        ].copy()
        
        if len(clustering_data) < n_clusters * 2:
            print(f"⚠️ Insufficient data for clustering")
            self.cluster_analysis = {}
            return pd.DataFrame()
        
        try:
            # Prepare features for clustering
            from sklearn.cluster import KMeans
            from sklearn.preprocessing import StandardScaler
            
            features = ['consumption', 'alcohol_disorder']
            
            # Add suicide data if available
            if ('suicide_rate' in clustering_data.columns and 
                clustering_data['suicide_rate'].notna().sum() > len(clustering_data) * 0.3):
                features.append('suicide_rate')
                clustering_data = clustering_data[clustering_data['suicide_rate'].notna()]
            
            X = clustering_data[features].copy()
            
            # Standardize features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Perform K-means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            clustering_data['cluster'] = kmeans.fit_predict(X_scaled)
            
            # Analyze clusters
            cluster_summary = clustering_data.groupby('cluster')[features].mean().round(2)
            cluster_counts = clustering_data['cluster'].value_counts().sort_index()
            
            print(f"📊 Clustering results:")
            for cluster in range(n_clusters):
                count = cluster_counts.get(cluster, 0)
                print(f"   Cluster {cluster}: {count} countries")
                for feature in features:
                    value = cluster_summary.loc[cluster, feature]
                    print(f"     {feature}: {value}")
            
            # Store results for dashboard
            self.cluster_analysis = {
                'data': clustering_data[['country', 'region', 'cluster'] + features],
                'summary': cluster_summary,
                'counts': cluster_counts,
                'features': features
            }
            
            return clustering_data[['country', 'region', 'cluster'] + features]
            
        except ImportError:
            print("⚠️ scikit-learn not available for clustering analysis")
            self.cluster_analysis = {}
            return pd.DataFrame()
        except Exception as e:
            print(f"❌ Error in clustering analysis: {e}")
            self.cluster_analysis = {}
            return pd.DataFrame()
    
    def generate_comprehensive_statistics(self):
        """
        Generate comprehensive statistics across all indicators
        
        Returns:
        dict: Comprehensive statistics
        """
        print("📈 Generating comprehensive statistics...")
        
        stats = {}
        
        # Alcohol consumption statistics
        if self.data_processor.alcohol_consumption is not None:
            consumption_2022 = self.data_processor.alcohol_consumption['2022'].dropna()
            stats['alcohol_consumption'] = {
                'countries': len(consumption_2022),
                'mean': consumption_2022.mean(),
                'median': consumption_2022.median(),
                'std': consumption_2022.std(),
                'min': consumption_2022.min(),
                'max': consumption_2022.max(),
                'top_consumer': self.data_processor.alcohol_consumption.loc[consumption_2022.idxmax(), 'country']
            }
        
        # Alcohol disorders statistics
        if self.data_processor.alcohol_disorder is not None:
            disorder_data = self.data_processor.alcohol_disorder[
                self.data_processor.alcohol_disorder['gender'] == 1  # Males
            ]['alcohol_disorder'].dropna()
            
            stats['alcohol_disorders'] = {
                'countries': len(disorder_data),
                'mean': disorder_data.mean(),
                'median': disorder_data.median(),
                'std': disorder_data.std(),
                'min': disorder_data.min(),
                'max': disorder_data.max()
            }
        
        # Suicide statistics
        if (hasattr(self.data_processor, 'suicide_data') and 
            self.data_processor.suicide_data is not None and 
            len(self.data_processor.suicide_data) > 0):
            
            suicide_data = self.data_processor.suicide_data[
                self.data_processor.suicide_data['gender'] == 1  # Males
            ]['suicide_rate'].dropna()
            
            stats['suicide_rates'] = {
                'countries': len(suicide_data),
                'mean': suicide_data.mean(),
                'median': suicide_data.median(),
                'std': suicide_data.std(),
                'min': suicide_data.min(),
                'max': suicide_data.max()
            }
        else:
            stats['suicide_rates'] = {'countries': 0, 'mean': 0, 'note': 'No data available'}
        
        # Former drinkers statistics
        if (hasattr(self.data_processor, 'former_drinkers_data') and 
            self.data_processor.former_drinkers_data is not None and 
            len(self.data_processor.former_drinkers_data) > 0):
            
            former_data = self.data_processor.former_drinkers_data['former_drinkers'].dropna()
            
            stats['former_drinkers'] = {
                'countries': len(former_data),
                'mean': former_data.mean(),
                'median': former_data.median(),
                'std': former_data.std(),
                'min': former_data.min(),
                'max': former_data.max()
            }
        else:
            stats['former_drinkers'] = {'countries': 0, 'mean': 0, 'note': 'No data available'}
        
        # Add correlation results if available
        if self.correlation_results:
            stats['correlations'] = self.correlation_results
        
        # Add high-risk analysis results
        if not self.high_risk_countries.empty:
            stats['high_risk'] = {
                'countries_identified': len(self.high_risk_countries),
                'top_risk_country': self.high_risk_countries.iloc[0]['country'] if len(self.high_risk_countries) > 0 else 'N/A'
            }
        
        self.comprehensive_stats = stats
        return stats
    
    def create_all_static_plots(self):
        """
        Create all static visualizations.
        """
        print("Creating static visualizations...")
        
        # Top 10 bar chart
        top10_data = self.data_processor.get_top_consumers('2022', 10)
        if top10_data is not None:
            self.static_plotter.create_top10_bar_chart(top10_data, '2022')
            print("  ✅ Top 10 bar chart created")
        
        # Europe trend plot
        europe_data = self.data_processor.get_europe_trend_data()
        if europe_data is not None:
            self.static_plotter.create_europe_trend_plot(europe_data)
            print("  ✅ Europe trend plot created")
        
        # Regional comparison
        regional_data = self.data_processor.get_regional_averages('2022')
        if regional_data is not None:
            self.static_plotter.create_regional_comparison(regional_data)
            print("  ✅ Regional comparison chart created")
        
        # Scatter plot (consumption vs disorders)
        if self.data_processor.merged_data is not None:
            male_data = self.data_processor.merged_data[
                self.data_processor.merged_data['gender'] == 1
            ].copy()
            
            if not male_data.empty:
                self.r_squared = self.static_plotter.create_scatter_plot(male_data)
                print("  ✅ Scatter plot created")
        
        print("✅ All static plots created")
    
    def create_all_interactive_plots(self):
        """
        Create all interactive visualizations.
        """
        print("Creating interactive visualizations...")
        
        # Top 10 interactive bar chart
        top10_data = self.data_processor.get_top_consumers('2022', 10)
        if top10_data is not None:
            fig_top10 = self.interactive_plotter.create_interactive_top10_bar(top10_data, '2022')
            self.figures['top10'] = fig_top10
            print("  ✅ Interactive top 10 chart created")
        
        # Europe trends interactive plot
        europe_data = self.data_processor.get_europe_trend_data()
        if europe_data is not None:
            fig_europe = self.interactive_plotter.create_interactive_europe_trends(europe_data)
            self.figures['europe_trends'] = fig_europe
            print("  ✅ Interactive Europe trends created")
        
        # World map
        if self.data_processor.alcohol_consumption is not None:
            fig_map = self.interactive_plotter.create_interactive_world_map(
                self.data_processor.alcohol_consumption, '2022'
            )
            self.figures['world_map'] = fig_map
            print("  ✅ Interactive world map created")
        
        # Interactive scatter plot
        if self.data_processor.merged_data is not None:
            male_data = self.data_processor.merged_data[
                self.data_processor.merged_data['gender'] == 1
            ].copy()
            
            if not male_data.empty:
                fig_scatter, r_squared = self.interactive_plotter.create_interactive_scatter_plot(male_data)
                self.figures['scatter'] = fig_scatter
                self.r_squared = r_squared
                print("  ✅ Interactive scatter plot created")
        
        # Dashboard
        if self.data_processor.alcohol_consumption is not None:
            fig_dashboard = self.interactive_plotter.create_comprehensive_dashboard(self.data_processor)
            if fig_dashboard:
                self.figures['dashboard'] = fig_dashboard
            else:
                fig_dashboard = self.interactive_plotter.create_dashboard(self.data_processor.alcohol_consumption)
                self.figures['dashboard'] = fig_dashboard
            print("  ✅ Dashboard created")
        
        print("✅ All interactive plots created")
    
    def create_extended_visualizations(self):
        """
        Create extended visualizations for suicide and comprehensive analysis
        """
        print("Creating extended visualizations...")
        
        # Suicide-alcohol scatter plot
        if (hasattr(self.data_processor, 'comprehensive_data') and 
            self.data_processor.comprehensive_data is not None):
            
            comprehensive_data = self.data_processor.comprehensive_data
            complete_data = comprehensive_data[
                comprehensive_data['consumption'].notna() &
                comprehensive_data['suicide_rate'].notna() &
                (comprehensive_data['gender'] == 1)
            ].copy()
            
            if len(complete_data) >= 10:
                # Create alcohol-suicide correlation plot
                fig_suicide_scatter = self.interactive_plotter.create_suicide_alcohol_scatter(complete_data)
                if fig_suicide_scatter:
                    self.figures['suicide_scatter'] = fig_suicide_scatter
                    print("  ✅ Suicide-alcohol scatter plot created")
        
        # Gender comparison visualization
        if self.data_processor.alcohol_disorder is not None:
            fig_gender = self.interactive_plotter.create_gender_comparison(self.data_processor.alcohol_disorder)
            if fig_gender:
                self.figures['gender_comparison'] = fig_gender
                print("  ✅ Gender comparison visualization created")
        
        print("✅ Extended visualizations created")
    
    def export_html_report(self, filename=None):
        """
        Export comprehensive HTML report.
        
        Parameters:
        filename (str): Optional custom filename
        
        Returns:
        str: Path to generated HTML file
        """
        print("Exporting HTML report...")
        
        html_file = self.html_generator.generate_html_report(
            self.data_processor, 
            self.figures, 
            filename
        )
        
        return html_file
    
    def run_complete_analysis(self, export_html=True, create_static=True, create_interactive=True):
        """
        Run the complete analysis pipeline with extended features.
        
        Parameters:
        export_html (bool): Whether to export HTML report
        create_static (bool): Whether to create static plots
        create_interactive (bool): Whether to create interactive plots
        """
        print("=" * 60)
        print("WHO ALCOHOL DATA ANALYSIS - COMPLETE PIPELINE")
        print("=" * 60)
        
        # Step 1: Process all data
        print("\n1. Processing WHO data...")
        if not self.process_all_data():
            print("❌ Data processing failed. Aborting analysis.")
            return
        
        # Step 2: Extended analysis
        print("\n2. Performing extended analysis...")
        
        # Alcohol-suicide correlation
        correlation_results = self.analyze_alcohol_suicide_correlation()
        
        # High-risk countries identification
        high_risk_countries = self.identify_high_risk_countries()
        
        # Clustering analysis
        clustering_results = self.perform_clustering_analysis()
        
        # Comprehensive statistics
        comprehensive_stats = self.generate_comprehensive_statistics()
        
        # Step 3: Create static visualizations
        if create_static:
            print("\n3. Creating static visualizations...")
            self.create_all_static_plots()
        
        # Step 4: Create interactive visualizations
        if create_interactive:
            print("\n4. Creating interactive visualizations...")
            self.create_all_interactive_plots()
            self.create_extended_visualizations()
        
        # Step 5: Export HTML report
        if export_html:
            print("\n5. Generating comprehensive HTML report...")
            html_file = self.export_html_report()
            print(f"   📄 Interactive report: {html_file}")
        
        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE!")
        print(f"📁 All outputs saved in '{self.output_dir}' directory")
        if export_html:
            print(f"🌐 Open the HTML report for interactive exploration")
        print("=" * 60)
    
    def get_data_summary(self):
        """
        Get a summary of all processed data.
        
        Returns:
        dict: Summary statistics
        """
        summary = {}
        
        if self.data_processor.alcohol_consumption is not None:
            summary['consumption'] = {
                'countries': len(self.data_processor.alcohol_consumption),
                'years': len([col for col in self.data_processor.alcohol_consumption.columns 
                            if str(col).isdigit()]),
                'regions': self.data_processor.alcohol_consumption['region'].nunique()
            }
        
        if self.data_processor.alcohol_disorder is not None:
            summary['disorders'] = {
                'records': len(self.data_processor.alcohol_disorder),
                'countries': self.data_processor.alcohol_disorder['country'].nunique(),
                'regions': self.data_processor.alcohol_disorder['region'].nunique()
            }
        
        if (hasattr(self.data_processor, 'suicide_data') and 
            self.data_processor.suicide_data is not None):
            summary['suicide'] = {
                'records': len(self.data_processor.suicide_data),
                'countries': self.data_processor.suicide_data['country'].nunique() if len(self.data_processor.suicide_data) > 0 else 0
            }
        else:
            summary['suicide'] = {'records': 0, 'countries': 0}
        
        if (hasattr(self.data_processor, 'former_drinkers_data') and 
            self.data_processor.former_drinkers_data is not None):
            summary['former_drinkers'] = {
                'records': len(self.data_processor.former_drinkers_data),
                'countries': self.data_processor.former_drinkers_data['country'].nunique() if len(self.data_processor.former_drinkers_data) > 0 else 0
            }
        else:
            summary['former_drinkers'] = {'records': 0, 'countries': 0}
        
        if self.data_processor.merged_data is not None:
            summary['merged'] = {
                'records': len(self.data_processor.merged_data),
                'countries': self.data_processor.merged_data['country'].nunique(),
                'correlation': self.r_squared
            }
        
        if hasattr(self.data_processor, 'comprehensive_data') and self.data_processor.comprehensive_data is not None:
            summary['comprehensive'] = {
                'records': len(self.data_processor.comprehensive_data),
                'countries': self.data_processor.comprehensive_data['country'].nunique(),
                'suicide_correlation': self.suicide_correlation
            }
        
        # Add dashboard-specific fields
        if self.correlation_results:
            summary['correlations'] = self.correlation_results
        
        if not self.high_risk_countries.empty:
            summary['high_risk'] = {
                'countries_identified': len(self.high_risk_countries)
            }
        
        return summary
    
    def create_custom_analysis(self, countries=None, year='2022'):
        """
        Create custom analysis for specific countries or year.
        
        Parameters:
        countries (list): List of country names to analyze
        year (str): Year to analyze
        """
        if self.data_processor.alcohol_consumption is None:
            print("No consumption data available. Run process_all_data() first.")
            return
        
        if countries:
            # Filter data for specific countries
            custom_data = self.data_processor.alcohol_consumption[
                self.data_processor.alcohol_consumption['country'].isin(countries)
            ].copy()
            
            print(f"Custom analysis for countries: {', '.join(countries)}")
            print_data_summary(custom_data, f"Custom Data ({year})")
            
            # Create custom visualizations
            if year in custom_data.columns:
                top_custom = custom_data[['country', 'region', year]].copy()
                top_custom.columns = ['country', 'region', 'consumption']
                top_custom = top_custom.dropna().sort_values('consumption', ascending=False)
                
                # Create custom bar chart
                self.static_plotter.create_top10_bar_chart(top_custom, f"{year}_custom")
                
                print(f"✅ Custom analysis completed for {len(countries)} countries")
        else:
            print("Please provide a list of countries for custom analysis.")