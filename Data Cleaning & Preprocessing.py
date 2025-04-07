import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset with your specific file path
df = pd.read_csv(r'C:\Users\saura\OneDrive\Documents\Task1\marketing_campaign.csv', sep=';')  # Note: try with tab separator

# Initial exploration
print("Dataset dimensions:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

# Check data types and null values
print("\nDataset info:")
print(df.info())

# Count missing values in each column
print("\nMissing values per column:")
print(df.isnull().sum())

# Check for duplicates
duplicate_count = df.duplicated().sum()
print(f"\nNumber of duplicate rows: {duplicate_count}")

# Handle missing values
missing_columns = df.columns[df.isnull().any()].tolist()
print("Columns with missing values:", missing_columns)

for col in missing_columns:
    # For numerical columns
    if df[col].dtype in ['int64', 'float64']:
        median_value = df[col].median()
        print(f"Filling missing values in {col} with median: {median_value}")
        df[col] = df[col].fillna(median_value)
    # For categorical columns
    else:
        mode_value = df[col].mode()[0]
        print(f"Filling missing values in {col} with mode: {mode_value}")
        df[col] = df[col].fillna(mode_value)

# Remove duplicate rows
original_row_count = df.shape[0]
df = df.drop_duplicates()
new_row_count = df.shape[0]
print(f"Removed {original_row_count - new_row_count} duplicate rows")

# Standardize text values - especially for Education and Marital_Status
if 'Education' in df.columns:
    # Make consistent lowercase first, then capitalize properly
    df['Education'] = df['Education'].str.lower()
    # Create mapping for education standardization
    education_mapping = {
        'basic': 'Basic',
        'graduation': 'Graduation',
        '2n cycle': '2n Cycle',
        'master': 'Master',
        'phd': 'PhD'
    }
    df['Education'] = df['Education'].map(education_mapping).fillna(df['Education'].str.capitalize())

if 'Marital_Status' in df.columns:
    # Standardize marital status
    df['Marital_Status'] = df['Marital_Status'].str.lower()
    marital_mapping = {
        'single': 'Single',
        'married': 'Married',
        'together': 'Together',
        'divorced': 'Divorced',
        'widow': 'Widow'
    }
    df['Marital_Status'] = df['Marital_Status'].map(marital_mapping).fillna(df['Marital_Status'].str.capitalize())

# Convert date formats
if 'Dt_Customer' in df.columns:
    # Convert to datetime format - try different formats
    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], errors='coerce')
    print("\nDate column 'Dt_Customer' converted to datetime format")
    print(df['Dt_Customer'].head())
    
    # Extract date components
    df['Customer_Year'] = df['Dt_Customer'].dt.year
    df['Customer_Month'] = df['Dt_Customer'].dt.month
    df['Customer_Day'] = df['Dt_Customer'].dt.day

# Handle outliers in numerical columns
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
# Exclude ID or date columns
numerical_cols = [col for col in numerical_cols if not col.lower().startswith(('id', 'dt'))]

print("\nNumerical columns for outlier treatment:", numerical_cols)


# Function to handle outliers
def handle_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Count outliers
    outliers_count = ((df[column] < lower_bound) | (df[column] > upper_bound)).sum()
    
    if outliers_count > 0:
        print(f"Found {outliers_count} outliers in {column}")
        # Cap the outliers
        df[column] = np.where(df[column] > upper_bound, upper_bound, df[column])
        df[column] = np.where(df[column] < lower_bound, lower_bound, df[column])
    
    return df

# Apply outlier handling to numerical columns
for col in numerical_cols:
    if col in df.columns:  # Make sure column exists
        df = handle_outliers(df, col)

# Feature engineering
# Calculate age from Year_Birth
if 'Year_Birth' in df.columns:
    df['Age'] = 2024 - df['Year_Birth']
    print("\nCreated 'Age' column")

# Total spending across categories
spending_cols = [col for col in df.columns if col.startswith('Mnt')]
if spending_cols:
    # Check if these columns exist and have values
    if all(col in df.columns for col in spending_cols):
        df['Total_Spending'] = df[spending_cols].sum(axis=1)
        print(f"\nCreated 'Total_Spending' column from {spending_cols}")

# Save the properly cleaned dataset
cleaned_file_path = r'C:\Users\saura\OneDrive\Documents\Task1\cleaned_marketing_campaign.csv'
df.to_csv(cleaned_file_path, index=False)
print(f"\nCleaned dataset saved to: {cleaned_file_path}")

# Create a detailed cleaning summary
with open(r'C:\Users\saura\OneDrive\Documents\Task1\cleaning_summary.md', 'w') as f:
    f.write("# Data Cleaning and Preprocessing Summary\n\n")
    f.write("## Dataset: Customer Personality Analysis\n\n")
    
    f.write("### Original Dataset\n")
    f.write(f"- Rows: {original_row_count}\n")
    f.write(f"- Columns: {len(df.columns)}\n")
    f.write(f"- Missing values: {', '.join(missing_columns) if missing_columns else 'None'}\n")
    f.write(f"- Duplicates: {duplicate_count}\n\n")
    
    f.write("### Cleaning Steps Performed\n")
    f.write("1. Handled missing values in the following columns:\n")
    for col in missing_columns:
        f.write(f"   - {col}\n")
    
    f.write(f"\n2. Removed {original_row_count - new_row_count} duplicate rows\n")
    
    f.write("\n3. Standardized text values in the following columns:\n")
    if 'Education' in df.columns:
        f.write("   - Education\n")
    if 'Marital_Status' in df.columns:
        f.write("   - Marital_Status\n")
    
    if 'Dt_Customer' in df.columns:
        f.write("\n4. Converted 'Dt_Customer' to datetime format and created year, month, day columns\n")
    
    f.write("\n5. Handled outliers in numerical columns using IQR method\n")
    
    f.write("\n6. Created new features:\n")
    if 'Age' in df.columns:
        f.write("   - Age (calculated from Year_Birth)\n")
    if 'Total_Spending' in df.columns:
        f.write("   - Total_Spending (sum of all spending categories)\n")
    
    f.write("\n### Final Dataset\n")
    f.write(f"- Rows: {df.shape[0]}\n")
    f.write(f"- Columns: {df.shape[1]}\n")
    f.write("- All data is now consistently formatted and ready for analysis\n")

print("Created summary file: cleaning_summary.md")
