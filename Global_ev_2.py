def load_dataset(file_path, **kwargs):
    
    import pandas as pd
    from pathlib import Path

    import warnings
    warnings.filterwarnings("ignore")

    file_type = Path(file_path).suffix.lower()
    
    # Dictionary of different file handlers
    handlers = {
        '.csv': pd.read_csv,
        '.xlsx': pd.read_excel,
        '.json': pd.read_json,
        '.parquet': pd.read_parquet
    }
    
    # Get reader function
    reader = handlers.get(file_type)
    if reader is None:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    # Load data with common cleaning parameters
    df = reader(file_path, **kwargs)
    
    # cleaning steps

    df.columns = df.columns.str.strip().str.lower()  # Standardize column names
    df = df.replace('', pd.NA)  # Convert empty strings to NA
    df = df.drop_duplicates()   # Drop duplicate rows

    return df

    # Check for common issues
import pandas as pd
def initial_data_quality(df):
    # Store initial data quality metrics
    quality_report = {
        'missing_values': df.isnull().sum().to_dict(),
        'duplicates': df.duplicated().sum(),
        'total_rows': len(df),
        'memory_usage': df.memory_usage().sum() / 1024**2  # in MB
    }
    
    return quality_report
    
    
#standardize datatypes
import pandas as pd
def standardize_datatypes(df):
    for column in df.columns:
        # Try converting string dates to datetime
        if df[column].dtype == 'object':
            try:
                df[column] = pd.to_datetime(df[column])
                print(f"Converted {column} to datetime")
            except ValueError:
                # Try converting to numeric if datetime fails
                try:
                    df[column] = pd.to_numeric(df[column].str.replace('$', '').str.replace(',', ''))
                    print(f"Converted {column} to numeric")
                except:
                    pass
    return df

# Handle missing values
import pandas as pd
def handle_missing_values(df):
    # Handle numeric columns
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_columns) > 0:
        df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
    
    # Handle categorical columns
    categorical_columns = df.select_dtypes(include=['object']).columns
    if len(categorical_columns) > 0:
        df[categorical_columns] = df[categorical_columns].fillna(df[categorical_columns].mode().iloc[0])
    
    return df

# Remove outliers using IQR method
import pandas as pd
def remove_outliers(df):
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    outliers_removed = {}
    
    for column in numeric_columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Count outliers before removing
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)].shape[0]
        
        # Cap the values instead of removing them
        df[column] = df[column].clip(lower=lower_bound, upper=upper_bound)
        
        if outliers > 0:
            outliers_removed[column] = outliers
            
    return df, outliers_removed


def validate_cleaning(df, original_shape, cleaning_report):
    validation_results = {
        'rows_remaining': len(df),
        'missing_values_remaining': df.isnull().sum().sum(),
        'duplicates_remaining': df.duplicated().sum(),
        'data_loss_percentage': (1 - len(df)/original_shape[0]) * 100
    }
    
    # Add validation results to the cleaning report
    cleaning_report['validation'] = validation_results
    return cleaning_report
 
def automated_cleaning_pipeline(df):
    # Store original shape for reporting
    original_shape = df.shape
    
    # Initialize cleaning report
    cleaning_report = {}
    
    # Execute each step and collect metrics
    cleaning_report['initial_quality'] = initial_data_quality(df)
    df = standardize_datatypes(df)
    df = handle_missing_values(df)
    df, outliers = remove_outliers(df)
    cleaning_report['outliers_removed'] = outliers
    
    # Validate and finalize report
    cleaning_report = validate_cleaning(df, original_shape, cleaning_report)
    
    return df, cleaning_report


# Specify the path to your dataset
file_path = 'C:/Users/Douglas/OneDrive/Desktop/Global_EV_Charging_Stations/uncleaned_ev_charging_stations.csv'

# Load the dataset
df = load_dataset(file_path)

# Execute the automated cleaning pipeline
cleaned_df, cleaning_report = automated_cleaning_pipeline(df)

# Display the cleaned DataFrame and cleaning report
print("Cleaned DataFrame:")
print(cleaned_df.head())  # Display the first few rows of the cleaned DataFrame
print(cleaned_df.info())  # Display the info of the cleaned DataFrame
print(cleaned_df.describe().T)  # Display the transposed description of the cleaned DataFrame

print("\nCleaning Report:")
for key, value in cleaning_report.items():
    print(f"{key}: {value}")


