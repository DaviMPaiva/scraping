import os
import json

# Function to read a JSON file and return its contents
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Folder containing JSON files
folder_path = "links_folder/"

# Set to store unique items
list_all = [] 
# Loop through each file in the folder
for filename in os.listdir(folder_path):
    print(filename)
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        data = read_json(file_path)
        if isinstance(data, list):
            list_all += data

# Convert set to list
merged_list = list(set(list_all))
print("the list has size: ", len(merged_list))
# Save merged list as JSON
output_file_path = "merged_list.json"
with open(output_file_path, 'w') as output_file:
    json.dump(merged_list, output_file, indent=4)

print("Merged list saved to", output_file_path)
