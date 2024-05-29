import json

output_file_path = 'list_of_files.txt'

with open('2up_search_results.json', 'r') as json_file:
    data_array = json.load(json_file)

    for data in data_array:
        if "APIResponse" in data and "Items" in data["APIResponse"] and data["APIResponse"]["Items"]:
            # Check if the "Items" list is not empty
            filename = data["APIResponse"]["Items"][0].get("OriginalFileName", "DefaultFilename")
            with open(output_file_path, "a") as output_file:
                output_file.write(filename + '\n')  # Adding a newline for each filename