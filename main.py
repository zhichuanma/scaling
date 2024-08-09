import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from cost.cost_equipment import cost_equipment
from cost.cost_plant import cost_plant
from cost.cost_utility import cost_utility
from cost.cost_workforce import cost_workforce
from cost.cost_material import cost_material

from LCA.LCA_equipment import LCA_equipment
from LCA.LCA_material import LCA_material
from LCA.LCA_plant import LCA_plant
from LCA.LCA_utility import LCA_utility

from plot.bar import cost_breakdown_sections
from plot.bar import LCA_breakdown
from plot.bar import cost_breakdown_location
from plot.bar import LCA_breakdown_location
'''
The central control station for the cost and LCA analysis.
In this file, we defined:
    - the global inputs which will be used in all the functions which are called.
    - the intermediate results
    - the final results from the analysis
'''
#--------------------------------------------------------------------------------------------------------#
# Global inputs
#--------------------------------------------------------------------------------------------------------#
technology = 'SOEC'
location = 'EU' # China, EU or US. based on  different location, the land cost and labor cost is differnet
interest_rate = 0.06

df_cost_component = pd.DataFrame(columns=['units', 'Equipment Cost', 'Plant Cost', 'Utility Cost', 'Labor Cost', 'Material Cost', 'Total Cost'])

'''
Here please input the LCA indicators you want to explore

Indicators can be chosen from this set: 
["GWP", "Ozone Depletion", "Acidification", "Eutrophication Freshwater", "Eutrophication Marine", "Eutrophication Terrestrial",
"Particulate Matter", "Ionizing Radiation", "Photochemical Ozone Formation", "Human Toxicity Cancer", "Human Toxicity Non-cancer", 
"Ecotoxicity Fresh Water", "Land Use", "Water Scarcity", "Resource Depletion Energy", "Resource Depletion Mineral and Metals"]
'''
lca_indicators = ["GWP", "Ozone Depletion", "Eutrophication Marine", "Human Toxicity Non-cancer", "Resource Depletion Mineral and Metals"]

# Create dataframes for lca indicators
LCA = {}

for indicator in lca_indicators:
    LCA[indicator] = pd.DataFrame(columns=['units', \
                                           'Equipment ' + str(indicator), \
                                           'Plant ' + str(indicator), \
                                           'Utility ' + str(indicator), \
                                           'Material ' + str(indicator), \
                                           'Total ' + str(indicator)])


for units in [1,10,100,1000,10000, 100000]: #unit MW for PEM

    #--------------------------------------------------------------------------------------------------------#
    # Intermediate results about cost
    #--------------------------------------------------------------------------------------------------------#
    df_equipment_cost = cost_equipment(technology = technology, units = units, op_time= 8760, interest_rate = interest_rate)
    df_plant_cost = cost_plant(technology = technology, units = units, op_time= 8760, location = location, interest_rate = interest_rate)
    df_utility_cost = cost_utility(technology = technology, units = units, op_time= 8760, location = location)
    df_workforce_cost = cost_workforce(technology = technology, units = units, op_time= 8760, location = location)
    df_material_cost = cost_material(technology = technology, units = units, location = location)

    # SAVE RESULTS INTO A DATAFRAME
    equipment_cost = sum(df_equipment_cost['cost equipment'])/units
    plant_cost = sum(df_plant_cost['cost plant'])/units
    utility_cost = sum(df_utility_cost['cost utility'])/units
    labor_cost = sum(df_workforce_cost['cost workforce'])/units
    material_cost = sum(df_material_cost['cost material'])
    Total_cost = equipment_cost + plant_cost + utility_cost + labor_cost + material_cost
    
    # Append the Cost results to the DataFrame
    df_cost_component = df_cost_component._append({'units': units,
                                    'Equipment Cost': equipment_cost,
                                    'Plant Cost': plant_cost,
                                    'Utility Cost': utility_cost,
                                    'Labor Cost': labor_cost,
                                    'Material Cost': material_cost,
                                    'Total Cost': Total_cost}, ignore_index=True)
    

    #--------------------------------------------------------------------------------------------------------#
    # Intermediate results about GWP
    #--------------------------------------------------------------------------------------------------------#
    
    df_equipment_LCA = LCA_equipment(technology = technology, units = units, op_time= 8760, location = location, lca_indicators = lca_indicators)
    df_plant_LCA = LCA_plant(technology = technology, units = units, op_time= 8760, location = location, lca_indicators = lca_indicators)
    df_utility_LCA = LCA_utility(technology = technology, units = units, op_time= 8760, location = location, lca_indicators = lca_indicators)
    df_material_LCA = LCA_material(technology = technology, units = units, location = location, lca_indicators = lca_indicators)

    # print(df_equipment_LCA)

    for indicator in lca_indicators:

        # SAVE RESULTS INTO DATAFRAMES
        equipment_LCA = sum(df_equipment_LCA[str(indicator) + " equipment"])/units
        plant_LCA = sum(df_plant_LCA[str(indicator) + " plant"])/units
        utility_LCA = sum(df_utility_LCA[str(indicator) + " utility"])/units
        material_LCA = sum(df_material_LCA[str(indicator) + ' material'])
        Total_LCA = equipment_LCA + plant_LCA + utility_LCA + material_LCA
        
        # Append the LCA results to the DataFrame
        LCA[indicator] = LCA[indicator]._append({'units': units,
                                        'Equipment ' + str(indicator): equipment_LCA,
                                        'Plant ' + str(indicator): plant_LCA,
                                        'Utility ' + str(indicator): utility_LCA,
                                        'Material ' + str(indicator): material_LCA,
                                        'Total ' + str(indicator): Total_LCA}, ignore_index=True)
    
   
print(df_cost_component)

for indicator in LCA: print(LCA[indicator])

#--------------------------------------------------------------------------------------------------------#
# Change production volume here                                                                          
#--------------------------------------------------------------------------------------------------------#
units = 10000
location = "EU"

df_equipment_cost = cost_equipment(technology = technology, units = units, op_time= 8760, interest_rate = interest_rate)
df_plant_cost = cost_plant(technology = technology, units = units, op_time= 8760, location = location, interest_rate = interest_rate)
df_utility_cost = cost_utility(technology = technology, units = units, op_time= 8760, location = location)
df_workforce_cost = cost_workforce(technology = technology, units = units, op_time= 8760, location = location)
df_material_cost = cost_material(technology = technology, units = units, location = location)

cost_breakdown_sections(units=units, technology=technology, df_equipment_cost=df_equipment_cost, df_plant_cost=df_plant_cost, df_utility_cost=df_utility_cost,df_workforce_cost=df_workforce_cost,df_material_cost=df_material_cost)

#--------------------------------------------------------------------------------------------------------#
# Change units and lca indicators here                                                                   
#--------------------------------------------------------------------------------------------------------#
lca_indicators = ["GWP", "Ozone Depletion", "Acidification", "Eutrophication Freshwater", "Eutrophication Marine", "Eutrophication Terrestrial",
"Particulate Matter", "Ionizing Radiation", "Photochemical Ozone Formation", "Human Toxicity Cancer", "Human Toxicity Non-cancer", 
"Ecotoxicity Fresh Water", "Land Use", "Water Scarcity", "Resource Depletion Energy", "Resource Depletion Mineral and Metals"]

units = 1000
location = "EU"

df_equipment_LCA = LCA_equipment(technology = technology, units = units, op_time= 8760, location = location, lca_indicators = lca_indicators)
df_plant_LCA = LCA_plant(technology = technology, units = units, op_time= 8760, location = location, lca_indicators = lca_indicators)
df_utility_LCA = LCA_utility(technology = technology, units = units, op_time= 8760, location = location, lca_indicators = lca_indicators)
df_material_LCA = LCA_material(technology = technology, units = units, location = location, lca_indicators = lca_indicators)

LCA_breakdown(technology, units, lca_indicators, df_equipment_LCA, df_plant_LCA, df_utility_LCA, df_material_LCA)

#--------------------------------------------------------------------------------------------------------#
# Change units here                                                                   
#--------------------------------------------------------------------------------------------------------#
units = 1000
locations_list = ["China", "US", "EU"]
lca_indicators = ["GWP"]

cost_breakdown_location(units, cost_equipment, cost_plant, cost_utility, cost_workforce, cost_material, technology, interest_rate, locations_list)
LCA_breakdown_location(units, LCA_equipment, LCA_plant, LCA_utility, LCA_material, technology, locations_list, lca_indicators)