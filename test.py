LCA_results = {}
indicator = 'CO2'

# Existing nested dictionary structure
LCA_results[indicator] = {
    'Equipment': 50,
    'Plant': 75,
    'Utility': 25,
}

# Adding a new key-value pair
LCA_results[indicator]['Material'] = 100

print(LCA_results)