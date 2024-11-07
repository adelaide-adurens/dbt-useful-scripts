import json
from pathlib import Path
import os

'''
    This script helps to quickly identify based on the project manifest.json if 
any model in the project is not being referenced by another one and is pottentially 
a candidate to me removed from the project.
'''

# Set paths according to your project structure
dbt_project_path = Path(__file__).resolve().parents[0]  # Assuming this script is in the root folder.
manifest_path = dbt_project_path / 'target/manifest.json'
output_file_path = dbt_project_path / 'unused_models_list.txt'



# Step 1: Run `dbt compile` to generate the manifest.json
os.system("dbt compile")

# Load the dbt manifest.json
with manifest_path.open() as f:
    manifest = json.load(f)

# Step 2: Identify all models and those that are referenced by others
all_models = {node_id: manifest['nodes'][node_id]['original_file_path'] 
              for node_id in manifest['nodes'] if manifest['nodes'][node_id]['resource_type'] == 'model'}
referenced_models = set()

for node in manifest['nodes'].values():
    if 'depends_on' in node:
        for dep in node['depends_on'].get('nodes', []):
            if dep in all_models:
                referenced_models.add(dep)

# Determine unused models
unused_models = set(all_models.keys()) - referenced_models


# Step 4: Save all unused model paths to a text file
with output_file_path.open("w") as f:
    for model in unused_models:
        f.write(model + "\n")


print(f"List of models tagged with 'not_used' saved to {output_file_path}.")

