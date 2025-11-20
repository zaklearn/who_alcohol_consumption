"""
HTML Report Generator - Bilingual support
"""

import pandas as pd
from datetime import datetime
from config.translations import TRANSLATIONS

class HTMLReportGenerator:
    def __init__(self, language='en'):
        self.language = language
    
    def t(self, key):
        """Get translation"""
        return TRANSLATIONS[self.language].get(key, key)
    
    def generate_report(self, processor, figures, output_path):
        """Generate complete HTML report"""
        
        # Calculate statistics
        stats = self._calculate_stats(processor)
        
        # Convert figures to HTML
        figures_html = {}
        for name, fig in figures.items():
            if fig is not None:
                figures_html[name] = fig.to_html(include_plotlyjs='cdn', div_id=f"{name}-plot")
        
        # Generate HTML content
        html = self._generate_html_template(stats, figures_html)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_path
    
    def _calculate_stats(self, processor):
        """Calculate key statistics"""
        stats = {}
        
        if processor.alcohol_consumption is not None:
            stats['total_countries'] = len(processor.alcohol_consumption)
            if '2022' in processor.alcohol_consumption.columns:
                stats['avg_consumption'] = processor.alcohol_consumption['2022'].mean()
                stats['max_consumption'] = processor.alcohol_consumption['2022'].max()
                top = processor.alcohol_consumption.loc[processor.alcohol_consumption['2022'].idxmax()]
                stats['top_country'] = top['country']
        
        if processor.alcohol_disorder is not None:
            male_disorders = processor.alcohol_disorder[processor.alcohol_disorder['gender'] == 1]
            stats['avg_disorders'] = male_disorders['alcohol_disorder'].mean()
        
        return stats
    
    def _generate_html_template(self, stats, figures):
        """Generate HTML template"""
        
        lang = self.language
        
        html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.t('app_title')}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            color: #333;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5rem;
            font-weight: 300;
        }}
        
        .header p {{
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 1rem;
        }}
        
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }}
        
        .metric-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
            border-left: 4px solid #007bff;
        }}
        
        .metric-value {{
            font-size: 2rem;
            font-weight: bold;
            color: #007bff;
            margin: 0.5rem 0;
        }}
        
        .metric-label {{
            color: #666;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .section {{
            background: white;
            padding: 2rem;
            margin: 2rem 0;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .section h2 {{
            margin-top: 0;
            color: #007bff;
            border-bottom: 2px solid #007bff;
            padding-bottom: 0.5rem;
        }}
        
        .plot-container {{
            margin: 1rem 0;
        }}
        
        .footer {{
            text-align: center;
            padding: 2rem;
            color: #666;
            font-size: 0.9rem;
        }}
        
        @media print {{
            .header {{
                background: #667eea;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🍷 {self.t('app_title')}</h1>
        <p>{self.t('subtitle')}</p>
        <p><small>{datetime.now().strftime('%B %d, %Y')}</small></p>
    </div>

    <div class="container">
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-value">{stats.get('total_countries', 0)}</div>
                <div class="metric-label">{self.t('total_countries')}</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{stats.get('avg_consumption', 0):.1f}L</div>
                <div class="metric-label">{self.t('global_avg_2022')}</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{stats.get('max_consumption', 0):.1f}L</div>
                <div class="metric-label">{self.t('highest_consumption')}</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{stats.get('top_country', 'N/A')}</div>
                <div class="metric-label">{self.t('country')}</div>
            </div>
        </div>

        <div class="section">
            <h2>{self.t('top_10_countries')}</h2>
            <div class="plot-container">
                {figures.get('top10', '<p>No data available</p>')}
            </div>
        </div>

        <div class="section">
            <h2>{self.t('world_map')}</h2>
            <div class="plot-container">
                {figures.get('world_map', '<p>No data available</p>')}
            </div>
        </div>

        <div class="section">
            <h2>{self.t('europe_trends')}</h2>
            <div class="plot-container">
                {figures.get('trends_europe', '<p>No data available</p>')}
            </div>
        </div>

        <div class="section">
            <h2>{self.t('continental_trends')}</h2>
            <div class="plot-container">
                <h3>Americas</h3>
                {figures.get('trends_americas', '<p>No data available</p>')}
            </div>
            <div class="plot-container">
                <h3>Africa</h3>
                {figures.get('trends_africa', '<p>No data available</p>')}
            </div>
            <div class="plot-container">
                <h3>Asia</h3>
                {figures.get('trends_asia', '<p>No data available</p>')}
            </div>
        </div>

        <div class="section">
            <h2>{self.t('correlation_analysis')}</h2>
            <div class="plot-container">
                {figures.get('scatter', '<p>No data available</p>')}
            </div>
        </div>
    </div>

    <div class="footer">
        <p>{self.t('footer')}</p>
    </div>
</body>
</html>"""
        
        return html