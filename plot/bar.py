import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

# colors configure
blue = (40/255, 120/255, 181/255)
pink = (255/255, 136/255, 132/255)
red = (200/255, 37/255, 35/255)
orange = (248/255, 172/255, 140/255)
lightblue = (154/255, 201/255, 219/255)
grey = (153/255, 153/255, 153/255)
lightgreen = (87/255, 171/255, 38/255)
yellow = (255/255, 237/255, 0/255)
darkblue = (0/255, 84/255, 58/255)
darkgreen = (0/255, 97/255, 102/255)
purple = (97/255, 33/255, 89/255)
darkred = (161/255, 15/255, 54/255)
brown = (245/255,168/255,0/255)
bluegreen = (0/255, 150/255, 158/255)
redpink = (227/255, 0/255, 102/255)
red_2 = (204/255, 8/255, 31/255)
darkyellow = (105/255, 84/255, 11/255)
superdarkgreen = (14/255,55/255, 22/255)
superdarkteal = (0/255,54/255,72/255)


def cost_breakdown_location(units, cost_equipment, cost_plant, cost_utility, cost_workforce, cost_material, technology, interest_rate, locations_list):
    """
    Plots a stacked bar chart of cost breakdown for the specified units based on different locations .
    
    Parameters:
    - df: Pandas DataFrame containing the cost data.
    - units_list: list of unit values to plot.
    
    Returns:
    - A matplotlib stacked bar chart.
    """
    colors = [blue, pink, red, orange, lightblue, grey]
    df_cost = {}
    for location in locations_list:
        if location not in df_cost:
            df_cost[location] = {}
        # df_equipment_cost = cost_equipment(technology = technology, units = units, op_time= 8760, interest_rate = interest_rate)
        df_plant_cost = cost_plant(technology = technology, units = units, op_time= 8760, location = location, interest_rate = interest_rate)
        df_utility_cost = cost_utility(technology = technology, units = units, op_time= 8760, location = location)
        df_workforce_cost = cost_workforce(technology = technology, units = units, op_time= 8760, location = location)
        # df_material_cost = cost_material(technology = technology, units = units, location = location)

        # equipment_cost = sum(df_equipment_cost['cost equipment'])/units
        plant_cost = sum(df_plant_cost['cost plant'])/units
        utility_cost = sum(df_utility_cost['cost utility'])/units
        labor_cost = sum(df_workforce_cost['cost workforce'])/units
        # material_cost = sum(df_material_cost['cost material'])

        # df_cost[location]['equipment'] = equipment_cost
        df_cost[location]['plant'] = plant_cost
        df_cost[location]['utility'] = utility_cost
        df_cost[location]['labor'] = labor_cost
        # df_cost[location]['material'] = material_cost
        
    matplotlib.rcParams['font.size'] = 10
    matplotlib.rcParams['font.sans-serif'] = "Arial"
    matplotlib.rcParams['font.family'] = 'sans-serif'

    colors = [blue, pink, red, orange, lightblue, grey]

    Cost_df = pd.DataFrame.from_dict(df_cost, orient='index')

    Cost_df.plot(kind='bar', stacked=True, figsize=(15, 9), color = colors, edgecolor='black', linewidth=1)

    plt.ylabel('Cost', fontsize=12, weight='bold')
    plt.xlabel(f'cost for producing {units} {technology} per year', fontsize=12, weight='bold')

    plt.xticks(fontsize=10, rotation=45)
    plt.tick_params(axis='x', which='both', length=0)  # Remove x-axis tick marks
    plt.yticks(fontsize=10)

    plt.legend()
    plt.tight_layout()
    plt.show()

def LCA_breakdown_location(units, LCA_equipment, LCA_plant, LCA_utility, LCA_material, technology, locations_list, lca_indicators):
    """
    Plots a stacked bar chart of cost breakdown for the specified units based on different locations .
    
    Parameters:
    - df: Pandas DataFrame containing the cost data.
    - units_list: list of unit values to plot.
    
    Returns:
    - A matplotlib stacked bar chart.
    """
    colors = [blue, pink, red, orange, lightblue, grey]
    df_LCA = {}
    for location in locations_list:
        if location not in df_LCA:
            df_LCA[location] = {}

        # df_equipment_LCA = LCA_equipment(technology = technology, units = units, op_time= 8760, location = location, lca_indicators = lca_indicators)
        df_plant_LCA = LCA_plant(technology = technology, units = units, op_time= 8760, location = location, lca_indicators = lca_indicators)
        df_utility_LCA = LCA_utility(technology = technology, units = units, op_time= 8760, location = location, lca_indicators = lca_indicators)
        # df_material_LCA = LCA_material(technology = technology, units = units, location = location, lca_indicators = lca_indicators)    
        # df_equipment_cost = cost_equipment(technology = technology, units = units, op_time= 8760, interest_rate = interest_rate)
        for indicator in lca_indicators:
            plant_LCA = sum(df_plant_LCA[str(indicator) + " plant"])/units
            utility_LCA = sum(df_utility_LCA[str(indicator) + " utility"])/units
        # df_material_cost = cost_material(technology = technology, units = units, location = location)

        # df_cost[location]['equipment'] = equipment_cost
        df_LCA[location]['plant'] = plant_LCA
        df_LCA[location]['utility'] = utility_LCA
        # df_cost[location]['material'] = material_cost
        
    matplotlib.rcParams['font.size'] = 10
    matplotlib.rcParams['font.sans-serif'] = "Arial"
    matplotlib.rcParams['font.family'] = 'sans-serif'

    colors = [blue, pink, red, orange, lightblue, grey]

    Cost_df = pd.DataFrame.from_dict(df_LCA, orient='index')

    Cost_df.plot(kind='bar', stacked=True, figsize=(15, 9), color = colors, edgecolor='black', linewidth=1)

    plt.ylabel(f'{lca_indicators}', fontsize=12, weight='bold')
    plt.xlabel(f'environmental impacts for producing {units} {technology} per year', fontsize=12, weight='bold')

    plt.xticks(fontsize=10, rotation=45)
    plt.tick_params(axis='x', which='both', length=0)  # Remove x-axis tick marks
    plt.yticks(fontsize=10)

    plt.legend()
    plt.tight_layout()
    plt.show()


def cost_breakdown_sections(technology, units, df_equipment_cost, df_plant_cost, df_utility_cost, df_workforce_cost, df_material_cost):
    """
    Plots a stacked bar chart of cost breakdown for the specified units based on different sections.
    
    Parameters:
    - df: Pandas DataFrame containing the cost data.
    
    Returns:
    - A matplotlib stacked bar chart.
   """
    
    matplotlib.rcParams['font.size'] = 10
    matplotlib.rcParams['font.sans-serif'] = "Arial"
    matplotlib.rcParams['font.family'] = 'sans-serif'

    colors = [blue, pink, red, orange, lightblue, grey]


    df_combined = pd.concat([df_equipment_cost, df_plant_cost, df_utility_cost, df_workforce_cost, df_material_cost])
    print(df_combined)
    df_summed = df_combined.groupby('Section')[['cost equipment', 'cost plant', 'cost utility', 'cost workforce', 'cost material']].sum().reset_index()

    df_summed['cost equipment'] = df_summed['cost equipment']/units
    df_summed['cost plant'] = df_summed['cost plant']/units
    df_summed['cost utility'] = df_summed['cost utility']/units
    df_summed['cost workforce'] = df_summed['cost workforce']/units
    # get rid of "cost"
    df_summed.set_index('Section', inplace=True)
    df_summed.columns = [col.replace('cost ', '') for col in df_summed.columns]

    # let the index order be based on the process of manufacturing
    if technology == "PEM":
        new_index_order = ['CCM', 'PTL', 'BP', 'MEA', "assembly"]
    elif technology == "SOEC":
        new_index_order = ['EEA', "Interconnect", "Glass Seal", "Assembly"]
        

    df_summed = df_summed.reindex(new_index_order)
    print(df_summed)
    df_summed.plot(kind='bar', stacked=True, figsize=(9, 12), color = colors, edgecolor='black', linewidth=1)
    
    plt.title('Cost Breakdown by Section', fontsize=14, weight='bold')
    plt.ylabel('Cost($/MW)', fontsize=12, weight='bold')
    plt.xlabel(f'Volume = {units} MW/y', fontsize=12, weight='bold')

    plt.xticks(fontsize=10, rotation=45)
    plt.tick_params(axis='x', which='both', length=0)  # Remove x-axis tick marks

    plt.yticks(fontsize=10)

    plt.legend()
    plt.tight_layout()
    plt.show()

def LCA_breakdown(technology, units, lca_indicators, df_equipment_LCA, df_plant_LCA, df_utility_LCA, df_material_LCA):
    """
    Plots a stacked bar chart of LCA breakdown for the specified units based on different lifecycle environmental impacts.
    
    Parameters:
    - df: Pandas DataFrame containing the cost data.
    
    Returns:
    - A matplotlib stacked bar chart.
   """
    
    normalized_factors = pd.read_excel('./Data/Global normalized factors.xlsx', index_col=0)

    LCA_results = {}

    # Initialize the dictionary by adding Equipment, Plant and Utility

    for indicator in lca_indicators:
        
        if indicator not in LCA_results:
            LCA_results[indicator] = {}

        equipment_LCA = sum(df_equipment_LCA[indicator + " equipment"]) / units / normalized_factors.loc[indicator, 'global NF for EF']
        plant_LCA = sum(df_plant_LCA[indicator + " plant"]) / units / normalized_factors.loc[indicator, 'global NF for EF']
        utility_LCA = sum(df_utility_LCA[indicator + " utility"]) / units / normalized_factors.loc[indicator, 'global NF for EF']
        
        # Initial component calculations
        LCA_results[indicator].update({
            'Equipment': equipment_LCA,
            'Plant': plant_LCA,
            'Utility': utility_LCA,
        })

    for indicator in lca_indicators:
        for index, row in df_material_LCA.iterrows():
            value_column = str(indicator) + " material"
            lca_value = row[value_column]
            normalized_value = lca_value / normalized_factors.loc[indicator, 'global NF for EF']
            
            # Check if the 'Material' key is already in the dictionary for the indicator
            if row["Material"] in LCA_results[indicator]:
                LCA_results[indicator][row["Material"]] += normalized_value
            else:
                LCA_results[indicator][row["Material"]] = normalized_value

    
    matplotlib.rcParams['font.size'] = 10
    matplotlib.rcParams['font.sans-serif'] = "Arial"
    matplotlib.rcParams['font.family'] = 'sans-serif'

    colors = [blue, pink, red, orange, lightblue, grey,superdarkgreen , yellow, darkblue, darkgreen, purple, darkred, brown, bluegreen, redpink, red_2, superdarkgreen,lightgreen, superdarkteal]

    LCA_df = pd.DataFrame.from_dict(LCA_results, orient='index')

    LCA_df.plot(kind='bar', stacked=True, figsize=(15, 9), color = colors, edgecolor='black', linewidth=1)

    plt.ylabel('Percentage of global environmental impacts', fontsize=12, weight='bold')
    plt.xlabel(f'Normalized environmental impacts for producing {units} {technology} per year', fontsize=12, weight='bold')

    plt.xticks(fontsize=10, rotation=45)
    plt.tick_params(axis='x', which='both', length=0)  # Remove x-axis tick marks
    plt.yticks(fontsize=10)

    plt.legend()
    plt.tight_layout()
    plt.show()

    return LCA_df