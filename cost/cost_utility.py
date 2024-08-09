import pandas as pd
import numpy as np
'''
Function to calculate the energy consumption in the manufacturing process
Inputs:
    - capacity of the plant
    - operation time of the factory
Outputs:
    -
    -
    -
The results will be used to calculate the cost and impacts of the technologies.

'''
def cost_utility(op_time, units, technology, location):
    file_path = './Data/' + str(technology) + '/equipment.xlsx'
    df = pd.read_excel(file_path)

    # calculate the number of equipment based on the annual capacity and operating time.
    df['equipment number'] = np.ceil(units/op_time/df['Real throughput(unit/hour)'])

    # calculate the energy consumption of each equipment
    df['operating hour'] = units/df['Real throughput(unit/hour)']*df['Availability']/df['equipment number']

    # calculate the energy consumption of each equipment
    df['electricity consumption'] = df['operating hour'] * df['equipment number'] * df['Power(kW)'] #unit -- kWh

    # load plant price data
    df_elec_price = pd.read_csv('./Data/energy_price.csv')
    elec_price = df_elec_price[df_elec_price['location'] == location]['electricity price($/kWh)'].values[0]

    # calculate the cost of electricity
    df['cost electricity'] = elec_price * df['electricity consumption']
    df['cost utility'] = df['cost electricity']
    # print(df)

    return df
