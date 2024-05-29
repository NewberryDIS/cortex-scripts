import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('cu_searched_check.csv')

# Strip whitespaces from all string columns
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

# Check for duplicates between two columns (assuming columns are named 'Column1' and 'Column2')
df['IsDuplicate'] = df.duplicated(subset=['Searched', 'Found'], keep=False)

# Create a new column 'NotDuplicate' with values from 'Column1' for non-duplicate rows
df['NotDuplicate'] = df['Searched'][~df['IsDuplicate']]

# Save the updated DataFrame back to a CSV file
df.to_csv('cu_duplicate_check.csv', index=False)