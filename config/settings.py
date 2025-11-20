"""
Configuration settings for WHO Alcohol Analysis
"""

# WHO API Configuration
WHO_API_BASE_URL = "https://ghoapi.azureedge.net/api"

# Indicators
ALCOHOL_CONSUMPTION_INDICATOR = "SA_0000001747"
ALCOHOL_DISORDER_INDICATOR = "SA_0000001462"

# EU Countries (Pre-1986)
EU_PRE_1986 = [
    "Belgium", "France", "Germany", "Italy", "Luxembourg", "Netherlands",
    "Denmark", "Ireland", "United Kingdom", "Greece"
]

# Country name standardization
COUNTRY_NAME_MAPPING = {
    "Russian Federation": "Russia",
    "Türkiye": "Turkey",
    "Iran (Islamic Republic of)": "Iran",
    "Venezuela (Bolivarian Republic of)": "Venezuela",
    "Bolivia (Plurinational State of)": "Bolivia",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "Republic of Korea": "South Korea",
    "Viet Nam": "Vietnam",
    "Democratic People's Republic of Korea": "North Korea",
    "Lao People's Democratic Republic": "Laos",
    "Congo": "Republic of the Congo",
    "Cote d'Ivoire": "Ivory Coast"
}

# Gender mapping
GENDER_MAPPING = {
    'Both sexes': 0,
    'Male': 1,
    'Female': 2
}

# Regional colors
REGION_COLORS = {
    'Europe': 'royalblue',
    'Eastern Mediterranean': 'burlywood',
    'Africa': 'forestgreen',
    'Americas': 'firebrick',
    'Western Pacific': 'orchid',
    'South-East Asia': 'orange'
}
