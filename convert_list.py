import csv

# Open the CSV file
with open('folder_ids.csv', 'r') as csvfile:
    # Create a CSV reader object
    csvreader = csv.reader(csvfile)
    
    # Skip the header row if it exists
    next(csvreader, None)
    
    # Initialize an empty list to store the items
    new_list = []
    
    # Iterate through each row in the CSV
    for row in csvreader:
        # Append the item to the list
        new_list.append(row[0])  # Assuming there's only one column
    
# Print the new list in a single line with items separated by space
print(' '.join(new_list))