"""
WHO Data Processor - Streamlined for Streamlit
Fetches and processes WHO API data
"""

import pandas as pd
import requests
from config.settings import (
    WHO_API_BASE_URL,
    ALCOHOL_CONSUMPTION_INDICATOR,
    ALCOHOL_DISORDER_INDICATOR,
    GENDER_MAPPING,
    COUNTRY_NAME_MAPPING
)

class WHODataProcessor:
    def __init__(self):
        self.alcohol_consumption = None
        self.alcohol_disorder = None
        self.merged_data = None
    
    def fetch_all_data(self):
        """Fetch all WHO data"""
        try:
            self.fetch_alcohol_consumption()
            self.fetch_alcohol_disorder()
            return True
        except Exception as e:
            print(f"Error fetching data: {e}")
            return False
    
    def fetch_alcohol_consumption(self):
        """Fetch alcohol consumption data"""
        values_url = f"{WHO_API_BASE_URL}/{ALCOHOL_CONSUMPTION_INDICATOR}"
        locations_url = f"{WHO_API_BASE_URL}/DIMENSION/COUNTRY/DimensionValues"
        
        values_data = self._api_call(values_url)
        locations_data = self._api_call(locations_url)
        
        if not values_data or not locations_data:
            return None
        
        df_values = pd.DataFrame(values_data)
        df_locations = pd.DataFrame(locations_data)
        
        merged = pd.merge(df_values, df_locations, left_on='SpatialDim', right_on='Code', how='left')
        
        final_data = merged[['Title', 'ParentTitle', 'TimeDim', 'NumericValue']].copy()
        final_data.columns = ['country', 'region', 'year', 'alcohol_consumption']
        
        alcohol_wide = final_data.pivot_table(
            index=['country', 'region'],
            columns='year',
            values='alcohol_consumption',
            aggfunc='first'
        ).reset_index()
        
        year_columns = sorted([col for col in alcohol_wide.columns if str(col).isdigit()], 
                            key=lambda x: int(str(x)))
        column_order = ['country', 'region'] + year_columns
        alcohol_wide = alcohol_wide[column_order]
        alcohol_wide.columns = [str(col) for col in alcohol_wide.columns]
        
        # Impute missing 2005 with 2004
        if '2005' in alcohol_wide.columns and '2004' in alcohol_wide.columns:
            alcohol_wide['2005'] = alcohol_wide['2005'].fillna(alcohol_wide['2004'])
        
        self.alcohol_consumption = alcohol_wide
        return alcohol_wide
    
    def fetch_alcohol_disorder(self):
        """Fetch alcohol disorder data"""
        values_url = f"{WHO_API_BASE_URL}/{ALCOHOL_DISORDER_INDICATOR}"
        locations_url = f"{WHO_API_BASE_URL}/DIMENSION/COUNTRY/DimensionValues"
        gender_url = f"{WHO_API_BASE_URL}/DIMENSION/SEX/DimensionValues"
        
        values_data = self._api_call(values_url)
        locations_data = self._api_call(locations_url)
        gender_data = self._api_call(gender_url)
        
        if not values_data or not locations_data or not gender_data:
            return None
        
        df_values = pd.DataFrame(values_data)
        df_locations = pd.DataFrame(locations_data)
        df_gender = pd.DataFrame(gender_data)
        
        merged = pd.merge(df_values, df_locations, left_on='SpatialDim', right_on='Code', how='left')
        final_merged = pd.merge(merged, df_gender, left_on='Dim1', right_on='Code', how='left')
        
        disorder_data = final_merged[['Title_x', 'ParentTitle_x', 'Title_y', 'Value']].copy()
        disorder_data.columns = ['country', 'region', 'gender', 'alcohol_disorder']
        disorder_data['gender'] = disorder_data['gender'].map(GENDER_MAPPING)
        disorder_data['alcohol_disorder'] = pd.to_numeric(disorder_data['alcohol_disorder'], errors='coerce')
        
        self.alcohol_disorder = disorder_data
        return disorder_data
    
    def merge_consumption_disorder_data(self, year='2022'):
        """Merge consumption and disorder data"""
        if self.alcohol_consumption is None or self.alcohol_disorder is None:
            return None
        
        if year not in self.alcohol_consumption.columns:
            return None
        
        consumption_year = self.alcohol_consumption[['country', 'region', year]].copy()
        consumption_year.columns = ['country', 'region', 'consumption']
        consumption_year = consumption_year.dropna()
        
        consumption_std = self._standardize_names(consumption_year)
        disorder_std = self._standardize_names(self.alcohol_disorder)
        
        merged = pd.merge(
            disorder_std,
            consumption_std[['join_name', 'consumption']],
            on='join_name',
            how='inner'
        )
        
        merged['alcohol_disorder'] = pd.to_numeric(merged['alcohol_disorder'], errors='coerce')
        merged['consumption'] = pd.to_numeric(merged['consumption'], errors='coerce')
        merged = merged.dropna()
        
        self.merged_data = merged
        return merged
    
    def get_top_consumers(self, year='2022', n=10):
        """Get top N consuming countries"""
        if self.alcohol_consumption is None or year not in self.alcohol_consumption.columns:
            return None
        
        top_data = self.alcohol_consumption[['country', 'region', year]].copy()
        top_data.columns = ['country', 'region', 'consumption']
        return top_data.dropna().sort_values('consumption', ascending=False).head(n)
    
    def get_regional_averages(self, year='2022'):
        """Calculate regional averages"""
        if self.alcohol_consumption is None or year not in self.alcohol_consumption.columns:
            return None
        
        regional_avg = self.alcohol_consumption.groupby('region')[year].agg(['mean', 'count']).reset_index()
        regional_avg.columns = ['Region', 'Average_Consumption', 'Number_of_Countries']
        return regional_avg.sort_values('Average_Consumption', ascending=False)
    
    def get_europe_trend_data(self):
        """Get European trend data"""
        if self.alcohol_consumption is None:
            return None
        
        from config.settings import EU_PRE_1986
        
        europe_data = self.alcohol_consumption[
            (self.alcohol_consumption['region'] == 'Europe') &
            (self.alcohol_consumption['country'].isin(EU_PRE_1986))
        ].copy()
        
        year_columns = [col for col in europe_data.columns if col not in ['country', 'region'] and str(col).isdigit()]
        
        europe_long = pd.melt(
            europe_data,
            id_vars=['country', 'region'],
            value_vars=year_columns,
            var_name='year',
            value_name='alcohol_consumption'
        )
        europe_long['year'] = europe_long['year'].astype(int)
        
        return europe_long
    
    def _api_call(self, url, timeout=30):
        """Make API call with error handling"""
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()['value']
        except Exception as e:
            print(f"API error: {e}")
            return None
    
    def _standardize_names(self, df, country_col='country'):
        """Standardize country names"""
        df_copy = df.copy()
        df_copy['join_name'] = df_copy[country_col].replace(COUNTRY_NAME_MAPPING)
        return df_copy
