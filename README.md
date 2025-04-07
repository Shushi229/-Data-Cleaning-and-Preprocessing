# -Data-Cleaning-and-Preprocessing
## Task 1:

## Objective
Clean and prepare a raw dataset with issues like nulls, duplicates, inconsistent formats, and outliers. The goal is to make the dataset suitable for analysis and modeling.

## Dataset Used
- **Customer Personality Analysis** from Kaggle

## Tools Used
- Python
- Pandas
- NumPy
- Matplotlib & Seaborn (for visualization and outlier treatment)

## Key Steps Performed

1. **Initial Data Exploration**
   - Checked shape, null values, data types, and duplicates.
   
2. **Missing Values Handling**
   - Filled numerical nulls with median.
   - Filled categorical nulls with mode.

3. **Duplicates Removal**
   - Removed duplicate rows using `.drop_duplicates()`.

4. **Text Standardization**
   - Standardized inconsistent entries in columns like `Education` and `Marital_Status`.

5. **Date Handling**
   - Converted `Dt_Customer` to datetime format.
   - Extracted year, month, and day for additional insights.

6. **Outlier Treatment**
   - Used IQR method to cap outliers in numerical columns.

7. **Feature Engineering**
   - Created new features like `Age` and `Total_Spending`.

## Files Included

- `marketing_campaign.csv` – Original dataset
- `cleaned_marketing_campaign1.csv` – Cleaned dataset
- `cleaning_script.py` – Python script used for data cleaning
- `cleaning_summary.md` – Auto-generated summary of all cleaning steps

## Concepts Applied

- `.isnull()`, `.fillna()`, `.drop_duplicates()`, `.str.lower()`, `pd.to_datetime()`, IQR for outliers
- Feature engineering using `df.sum()` and date component extraction
- Clean and consistent formatting of column names and values

## Outcome
A cleaned, standardized dataset ready for analysis and modeling.

## Author
Saurabh
