import pandas as pd
import numpy as np
manufacturing_to_machine = 3.5
height_building = 5
lifetime_plant = 40 # years

# Detailed information of the plant
thick = 0.25 #m, the thickness of the wall
density_steel = 7850 #kg/m^3
density_concrete = 2400 #kg/m^3
transportation_distance = 50 #km, from origin to plant
waste_distance = 50 #km, from plant to landfill
gamma = 0.67
average_elec_consumption = 50 #kWh/m2
reinforced_ratio = 0.01 #reinforced ratio
waste_rate_concrete = 0.8
waste_factor_concrete = 0.025
waste_rate_steel = 0.1
waste_factor_steel = 0.05

'''
Inputs to the function
    - op_time: hours/year
    - units: number of units produced a year
    - technology
    - location: either China, EU or US.
'''

def LCA_plant(op_time,units, technology, location, lca_indicators):

    file_path = './Data/' + str(technology) + '/equipment.xlsx'
    df = pd.read_excel(file_path)

    # calculate the number of equipment based on the annual capacity and operating time.
    df['equipment number'] = np.ceil(units/op_time/df['Real throughput(unit/hour)'])

    # load the parameters to calculate the area of the plant
    df_parameters_building = pd.read_csv('./Data/lca_parameters_building.csv')

    # calculate the plant area
    df['area manufacturing'] = manufacturing_to_machine * df['equipment number'] * df['Gross area(m2)']
    df['area storage'] = df['area manufacturing'] * df_parameters_building['storage'][0]/ df_parameters_building['manufacturing'][0]
    df['area auxiliary'] = df['area manufacturing'] * df_parameters_building['auxiliary'][0]/ df_parameters_building['manufacturing'][0]
    df['area yard'] = df['area manufacturing'] * df_parameters_building['yard'][0]/ df_parameters_building['manufacturing'][0] 
    df['area total'] = df['area manufacturing']/ df_parameters_building['manufacturing'][0]
    
    # load LCA_metrics
    df_steel_LCA = pd.read_csv('./Data/steel_lca.csv')
    df_concrete_LCA = pd.read_csv('./Data/concrete_lca.csv')
    df_transportation_LCA = pd.read_csv('./Data/transportation_lca.csv')
    df_elec_LCA = pd.read_csv('./Data/energy_lca.csv')

    # Calculation of the quantity of concrete and steel
    df['concrete'] = np.sqrt(df['area total'] - df['area yard']) * thick * height_building * 8 * density_concrete
    df['steel'] = df['concrete'] / density_concrete * reinforced_ratio * density_steel

    # Specify the location
    steel_lca = df_steel_LCA[df_steel_LCA['location'] == location]
    concrete_lca = df_concrete_LCA[df_concrete_LCA['location'] == location]
    transportation_lca = df_transportation_LCA[df_transportation_LCA['location'] == location]
    elec_lca = df_elec_LCA[df_elec_LCA['location'] == location]

    # LCA of the plant
    for indicators in lca_indicators:
        steel_lca = df_steel_LCA[indicators].values[0] #Function unit: kg
        concrete_lca = df_concrete_LCA[indicators].values[0] #Function unit: m^3
        transportation_lca = df_transportation_LCA[df_transportation_LCA['location'] == location][indicators].values[0] #Function unit: ton*km
        elec_lca = df_elec_LCA[indicators].values[0] #Function unit: kWh

        df['LCA production ' + str(indicators)] = (1 + waste_factor_concrete) * df['concrete'] / density_concrete * concrete_lca + (1 + waste_factor_steel) * df['steel'] * steel_lca
        df['LCA transportation ' + str(indicators)] = (1 + gamma) * transportation_distance * (df['concrete'] + df['steel']) / 1000 * transportation_lca
        df['LCA construction ' + str(indicators)] = (df['area total'] - df['area yard']) * average_elec_consumption * elec_lca
        df['LCA demolishing ' + str(indicators)] = 0.15 * df['LCA construction ' + str(indicators)]
        df['LCA waste ' + str(indicators)] = (1 + gamma) * waste_rate_concrete * df['concrete'] * transportation_lca / 1000 * waste_distance + (1 + gamma) * waste_rate_steel * df['steel'] * transportation_lca / 1000 * waste_distance
        df[str(indicators) + " plant"] =df['LCA production ' + str(indicators)] + \
                                        df['LCA transportation ' + str(indicators)] + \
                                        df['LCA construction ' + str(indicators)] + \
                                        df['LCA demolishing ' + str(indicators)] + \
                                        df['LCA waste ' + str(indicators)]

    return df


