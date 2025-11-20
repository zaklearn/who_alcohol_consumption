"""
Utility functions for WHO Alcohol Analysis
"""

import pandas as pd
import requests
import os
from config.settings import COUNTRY_NAME_MAPPING

def create_output_directory(output_dir):
    """
    Create output directory if it doesn't exist.
    
    Parameters:
    output_dir (str): Path to output directory
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

def fetch_who_api(endpoint, timeout=30):
    """
    Fetch data from WHO API endpoint.
    
    Parameters:
    endpoint (str): API endpoint URL
    timeout (int): Request timeout in seconds
    
    Returns:
    dict or None: API response data or None if error
    """
    try:
        response = requests.get(endpoint, timeout=timeout)
        response.raise_for_status()
        return response.json()['value']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {endpoint}: {e}")
        return None

def standardize_country_names(df, country_col='country'):
    """
    Standardize country names for consistent merging across datasets.
    
    Parameters:
    df (DataFrame): DataFrame containing country names
    country_col (str): Name of the country column
    
    Returns:
    DataFrame: DataFrame with standardized country names
    """
    df_copy = df.copy()
    df_copy['join_name'] = df_copy[country_col].replace(COUNTRY_NAME_MAPPING)
    return df_copy

def safe_numeric_conversion(series, errors='coerce'):
    """
    Safely convert a pandas series to numeric values.
    
    Parameters:
    series (pd.Series): Series to convert
    errors (str): How to handle conversion errors
    
    Returns:
    pd.Series: Converted series
    """
    return pd.to_numeric(series, errors=errors)

def filter_year_columns(df, exclude_cols=None):
    """
    Filter columns that represent years (4-digit numbers).
    
    Parameters:
    df (DataFrame): Input dataframe
    exclude_cols (list): Columns to exclude from filtering
    
    Returns:
    list: List of year columns
    """
    if exclude_cols is None:
        exclude_cols = ['country', 'region']
    
    return [col for col in df.columns 
            if col not in exclude_cols and str(col).isdigit() and len(str(col)) == 4]

def sort_year_columns(columns):
    """
    Sort year columns in chronological order.
    
    Parameters:
    columns (list): List of column names
    
    Returns:
    list: Sorted column names
    """
    return sorted(columns, key=lambda x: int(str(x)) if str(x).isdigit() else 0)

def validate_data_completeness(df, required_columns=None):
    """
    Validate data completeness and report missing values.
    
    Parameters:
    df (DataFrame): DataFrame to validate
    required_columns (list): Required columns to check
    
    Returns:
    dict: Validation report
    """
    report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict()
    }
    
    if required_columns:
        missing_required = [col for col in required_columns if col not in df.columns]
        report['missing_required_columns'] = missing_required
    
    return report

def print_data_summary(df, name="Dataset"):
    """
    Print a summary of the dataset.
    
    Parameters:
    df (DataFrame): DataFrame to summarize
    name (str): Name of the dataset
    """
    print(f"\n{name} Summary:")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Missing values: {df.isnull().sum().sum()}")
    
    if '2022' in df.columns:
        print(f"  2022 data available: {df['2022'].notna().sum()} countries")
