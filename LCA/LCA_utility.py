import pandas as pd
import numpy as np
'''
Function to calculate the energy consumption in the manufacturing process
Inputs:
    - capacity of the plant
    - operation time of the factory
Outputs:
    -

The results will be used to calculate the cost and impacts of the technologies.

'''


def LCA_utility(op_time, units, technology, location, lca_indicators):

    file_path = './Data/' + str(technology) + '/equipment.xlsx'
    df = pd.read_excel(file_path)

    # calculate the number of equipment based on the annual capacity and operating time.
    df['equipment number'] = np.ceil(units/op_time/df['Real throughput(unit/hour)'])

    # calculate the energy consumption of each equipment
    df['operating hour'] = units/df['Real throughput(unit/hour)']*df['Availability']/df['equipment number']

    # calculate the energy consumption of each equipment
    df['electricity consumption'] = df['operating hour'] * df['equipment number'] * df['Power(kW)'] #unit -- kWh

    # load the LCA data
    df_elec_LCA = pd.read_csv('./Data/energy_lca.csv')

    # specify the location
    df_elec_LCA = df_elec_LCA[df_elec_LCA['location'] == location]

    # GWP
    for indicators in lca_indicators:

        elec_LCA = df_elec_LCA[str(indicators)].values[0]
        df[str(indicators) + ' utility'] = elec_LCA * df['electricity consumption']

    return df

