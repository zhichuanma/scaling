import pandas as pd
import numpy as np
manufacturing_to_machine = 3.5
height_building = 5
lifetime_plant = 40 # years
average_elec_consumption = 50 #kWh/m2

# Detailed information of the equipments
density_steel = 7850 #kg/m^3
transportation_distance = 50 #km, from origin to plant
waste_distance = 50 #km, from plant to landfill
gamma = 0.67
waste_rate_aluminium = 0.1
waste_factor_aluminium = 0.025
waste_rate_steel = 0.1
waste_factor_steel = 0.05
waste_rate_copper = 0.05
waste_factor_copper = 0.025
waste_rate_aluminium_silicate = 0.05
waste_factor_aluminium_silicate = 0.025
waste_rate_rubber = 0.1
waste_factor_rubber = 0.025
waste_rate_plastic = 0.1
waste_factor_plastic = 0.05
waste_rate_plastic = 0.1
waste_factor_plastic = 0.05
waste_rate_silicon_carbide = 0.2
waste_factor_silicon_carbide = 0.025
waste_rate_ceramic = 0.05
waste_factor_ceramic = 0.025
waste_rate_glass = 0.05
waste_factor_glass = 0.025
waste_rate_titanium = 0.05
waste_factor_titanium = 0.025

'''
Inputs of the function:
    - op_time: unit hours per year
    - units: number of units to produce a year
    - technology

Outputs of the model:
    - dataframe of df equipment 
'''

def LCA_equipment(op_time,units, technology, location, lca_indicators):
    
    file_path = './Data/' + str(technology) + '/equipment.xlsx'
    df = pd.read_excel(file_path)

    # calculate the number of equipment based on the annual capacity and operating time.
    df['equipment number'] = np.ceil(units/op_time/df['Real throughput(unit/hour)'])

    # load lca metrics
    file_path = './Data/LCA_metrics.csv'
    df_LCA_metrics = pd.read_csv(file_path)
    df_transportation_LCA = pd.read_csv('./Data/transportation_lca.csv')
    df_elec_LCA = pd.read_csv('./Data/energy_lca.csv')

    # specify the location
    df_LCA_metrics = df_LCA_metrics[df_LCA_metrics['location'] == location]
    
    # LCA of the equipments (GWP)
    for indicators in lca_indicators:

        # map the lca indicators with materials
        mapping_lca = dict(zip(df_LCA_metrics['Materials'], df_LCA_metrics[indicators]))
        transportation_lca = df_transportation_LCA[df_transportation_LCA['location'] == location][indicators].values[0] #Function unit: ton*km
        elec_lca = df_elec_LCA[df_elec_LCA['location'] == location][indicators].values[0] #Function unit: kWh

        # LCA for production process
        df['LCA production ' + str(indicators)] = ((1 + waste_factor_steel) * df['steel'] * mapping_lca['steel'] + \
                                                   (1 + waste_factor_aluminium) * df['aluminium'] * mapping_lca['aluminium'] + \
                                                   (1 + waste_factor_copper) * df['copper'] * mapping_lca['copper'] + \
                                                   (1 + waste_factor_aluminium_silicate) * df['aluminium silicate'] * mapping_lca['aluminium silicate'] + \
                                                   (1 + waste_factor_rubber) * df['rubber'] * mapping_lca['rubber'] + \
                                                   (1 + waste_factor_plastic) * df['plastic'] * mapping_lca['plastic'] + \
                                                   (1 + waste_factor_silicon_carbide) * df['silicon carbide'] * mapping_lca['silicon carbide'] + \
                                                   (1 + waste_factor_ceramic) * df['ceramic'] * mapping_lca['ceramic'] + \
                                                   (1 + waste_factor_glass) * df['glass'] * mapping_lca['glass'] + \
                                                   (1 + waste_factor_titanium) * df['titanium'] * mapping_lca['titanium']) * df['equipment number']

        # LCA for transportation process
        df['LCA transportation ' + str(indicators)] = ((1 + gamma) * transportation_distance * (df['steel'] + df['aluminium'] + df['copper'] + \
                                                                                                df['aluminium silicate'] + df['rubber'] + \
                                                                                                df['plastic'] + df['silicon carbide'] + df['ceramic'] + \
                                                                                                df['glass'] + df['titanium']) / 1000 * transportation_lca) * df['equipment number']

        # LCA for construction process
        df['LCA construction ' + str(indicators)] = df['Gross area(m2)'] * average_elec_consumption * elec_lca * df['equipment number']

        # LCA for demolishing process
        df['LCA demolishing ' + str(indicators)] = 0.15 * df['LCA construction ' + str(indicators)]

        # LCA for waste process
        df['LCA waste ' + str(indicators)] = ((1 + gamma) * waste_rate_steel * df['steel'] * transportation_lca / 1000 * waste_distance + \
                                              (1 + gamma) * waste_rate_aluminium * df['aluminium'] * transportation_lca / 1000 * waste_distance + \
                                              (1 + gamma) * waste_rate_copper * df['copper'] * transportation_lca / 1000 * waste_distance + \
                                              (1 + gamma) * waste_rate_aluminium_silicate * df['aluminium silicate'] * transportation_lca / 1000 * waste_distance + \
                                              (1 + gamma) * waste_rate_rubber * df['rubber'] * transportation_lca / 1000 * waste_distance + \
                                              (1 + gamma) * waste_rate_plastic * df['plastic'] * transportation_lca / 1000 * waste_distance + \
                                              (1 + gamma) * waste_rate_silicon_carbide * df['silicon carbide'] * transportation_lca / 1000 * waste_distance + \
                                              (1 + gamma) * waste_rate_ceramic * df['ceramic'] * transportation_lca / 1000 * waste_distance + \
                                              (1 + gamma) * waste_rate_glass * df['glass'] * transportation_lca / 1000 * waste_distance + \
                                              (1 + gamma) * waste_rate_titanium * df['titanium'] * transportation_lca / 1000 * waste_distance) * df['equipment number']

        # LCA in total
        df[str(indicators) + " equipment"] = df['LCA production ' + str(indicators)] + \
                                             df['LCA transportation ' + str(indicators)] + \
                                             df['LCA construction ' + str(indicators)] + \
                                             df['LCA demolishing ' + str(indicators)] + \
                                             df['LCA waste ' + str(indicators)]
    
    return df

