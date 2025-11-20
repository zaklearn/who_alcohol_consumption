"""
Static visualizations using Matplotlib and Seaborn
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import linregress
from config.settings import PLOT_SETTINGS, REGION_COLORS, EU_PRE_1986

plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class StaticPlotGenerator:
    """
    Class to generate static plots using Matplotlib/Seaborn
    """
    
    def __init__(self, output_dir="plots"):
        self.output_dir = output_dir
    
    def create_top10_bar_chart(self, data, year='2022'):
        """
        Create bar chart of top 10 countries by alcohol consumption.
        
        Parameters:
        data (DataFrame): Top 10 consumption data
        year (str): Year being analyzed
        """
        plt.figure(figsize=PLOT_SETTINGS['figure_size'])
        
        bars = plt.bar(range(len(data)), data['consumption'], 
                      color='steelblue', alpha=0.8)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height - height*0.1,
                    f'{height:.1f}', ha='center', va='top', 
                    color='white', fontweight='bold', fontsize=10)
        
        plt.xlabel('Country', fontsize=PLOT_SETTINGS['font_size'], fontweight='bold')
        plt.ylabel('Alcohol Consumption (Litres)', fontsize=PLOT_SETTINGS['font_size'], fontweight='bold')
        plt.title(f'Top 10 Countries by Alcohol Consumption in {year}', 
                 fontsize=PLOT_SETTINGS['title_size'], fontweight='bold')
        plt.xticks(range(len(data)), data['country'], rotation=45, ha='right')
        
        # Add subtitle and caption
        plt.figtext(0.5, 0.92, 'Recorded per capita (15+) consumption in litres of pure alcohol (APC)', 
                   ha='center', fontsize=12, style='italic')
        plt.figtext(0.1, 0.02, 
                   'Note: Recorded APC is pure alcohol consumption (15 years old+) derived from recorded production and sales data.\n' +
                   'Three-year averages are calculated (e.g., 2015 is the average of 2014, 2015, 2016).\n' +
                   'Source: WHO database, accessed August 25, 2025.',
                   ha='left', fontsize=9, wrap=True)
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.2)
        
        # Save plot
        plt.savefig(f'{self.output_dir}/Fig1_Top10_Alcohol_consumption_{year}.png', 
                   dpi=PLOT_SETTINGS['dpi'], bbox_inches='tight')
        plt.show()
    
    def create_europe_trend_plot(self, europe_data):
        """
        Create line plot showing European alcohol consumption trends.
        
        Parameters:
        europe_data (DataFrame): Long format European trend data
        """
        plt.figure(figsize=PLOT_SETTINGS['figure_size'])
        
        for country in EU_PRE_1986:
            country_data = europe_data[europe_data['country'] == country]
            if not country_data.empty:
                plt.plot(country_data['year'], country_data['alcohol_consumption'], 
                        marker='o', label=country, linewidth=2, markersize=4)
        
        plt.xlabel('Year', fontsize=PLOT_SETTINGS['font_size'], fontweight='bold')
        plt.ylabel('Alcohol Consumption (Litres)', fontsize=PLOT_SETTINGS['font_size'], fontweight='bold')
        plt.title('Evolution of Alcohol Consumption in Europe (2000-2022)', 
                 fontsize=PLOT_SETTINGS['title_size'], fontweight='bold')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        
        # Add subtitle and caption
        plt.figtext(0.5, 0.92, 'Recorded per capita (15+) consumption in litres of pure alcohol - EU group before 1986', 
                   ha='center', fontsize=12, style='italic')
        plt.figtext(0.1, 0.02, 
                   'Note: Recorded APC is pure alcohol consumption (15 years old+) derived from recorded production and sales data.\n' +
                   'Three-year averages are calculated (e.g., 2015 is the average of 2014, 2015, 2016).\n' +
                   'Source: WHO database, accessed August 25, 2025.',
                   ha='left', fontsize=9, wrap=True)
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.2, right=0.85)
        
        # Save plot
        plt.savefig(f'{self.output_dir}/Fig2_Europe_alcohol_trend.png', 
                   dpi=PLOT_SETTINGS['dpi'], bbox_inches='tight')
        plt.show()
    
    def create_scatter_plot(self, male_data):
        """
        Create scatter plot of consumption vs disorders.
        
        Parameters:
        male_data (DataFrame): Male data for correlation analysis
        
        Returns:
        float: R-squared value
        """
        if male_data.empty:
            print("No male data available for scatter plot.")
            return 0
        
        # Calculate regression statistics
        slope, intercept, r_value, p_value, std_err = linregress(
            male_data['consumption'], male_data['alcohol_disorder']
        )
        r_squared = r_value ** 2
        
        # Create scatter plot
        plt.figure(figsize=PLOT_SETTINGS['figure_size'])
        
        for region in male_data['region'].unique():
            region_data = male_data[male_data['region'] == region]
            plt.scatter(region_data['consumption'], region_data['alcohol_disorder'],
                       c=REGION_COLORS.get(region, 'gray'), label=region, alpha=0.7, s=60)
        
        # Add regression line
        x_range = np.linspace(male_data['consumption'].min(), male_data['consumption'].max(), 100)
        y_pred = slope * x_range + intercept
        plt.plot(x_range, y_pred, color='gray', linestyle='--', alpha=0.8, linewidth=2)
        
        # Add R-squared annotation
        plt.text(0.02, 0.98, f'R-squared = {r_squared:.3f}', 
                transform=plt.gca().transAxes, fontsize=12, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.xlabel('Recorded Alcohol Consumption (Litres per capita, 2022)', 
                  fontsize=PLOT_SETTINGS['font_size'], fontweight='bold')
        plt.ylabel('Prevalence of Alcohol Use Disorders (% for males)', 
                  fontsize=PLOT_SETTINGS['font_size'], fontweight='bold')
        plt.title('Alcohol Consumption vs. Male Alcohol Use Disorders by Country', 
                 fontsize=PLOT_SETTINGS['title_size'], fontweight='bold')
        plt.legend(title='WHO Region', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        
        # Add subtitle
        plt.figtext(0.5, 0.92, 'Each point represents a country', 
                   ha='center', fontsize=12, style='italic')
        
        plt.tight_layout()
        plt.subplots_adjust(right=0.85)
        
        # Save plot
        plt.savefig(f'{self.output_dir}/Fig3_Consumption_vs_Disorder_scatter.png', 
                   dpi=PLOT_SETTINGS['dpi'], bbox_inches='tight')
        plt.show()
        
        return r_squared
    
    def create_regional_comparison(self, regional_data):
        """
        Create bar chart comparing regional averages.
        
        Parameters:
        regional_data (DataFrame): Regional averages data
        """
        plt.figure(figsize=PLOT_SETTINGS['figure_size'])
        
        bars = plt.bar(regional_data['Region'], regional_data['Average_Consumption'], 
                      color='lightblue', alpha=0.8)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.xlabel('WHO Region', fontsize=PLOT_SETTINGS['font_size'], fontweight='bold')
        plt.ylabel('Average Alcohol Consumption (Litres)', 
                  fontsize=PLOT_SETTINGS['font_size'], fontweight='bold')
        plt.title('Average Alcohol Consumption by WHO Region (2022)', 
                 fontsize=PLOT_SETTINGS['title_size'], fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Save plot
        plt.savefig(f'{self.output_dir}/Fig4_Regional_comparison.png', 
                   dpi=PLOT_SETTINGS['dpi'], bbox_inches='tight')
        plt.show()
