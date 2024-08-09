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
def cost_workforce(op_time, units, technology, location):
    file_path = './Data/' + str(technology) + '/equipment.xlsx'
    df = pd.read_excel(file_path)

    # calculate the number of equipment based on the annual capacity and operating time.
    df['equipment number'] = np.ceil(units/op_time/df['Real throughput(unit/hour)'])

    # calculate the energy consumption of each equipment
    df['operating hour'] = units/df['Real throughput(unit/hour)']*df['Availability']/df['equipment number'] # total working hours of each quipment

    # the required number of workers and managers is not linear to the number of equipment
    df['Workers required']  =  df['Workers'] * df['equipment number']**0.226
    df['Managers required'] =  df['Managers'] * df['equipment number']**0.226

    # calculate the energy consumption of each equipment
    df['worker hour'] = df['operating hour'] *  df['Workers required'] #unit -- hours
    df['manager hour'] = df['operating hour']  * df['Managers required'] #unit -- hours

    # load plant price data
    df_labor_price = pd.read_csv('./Data/labor_price.csv')
    worker_price = df_labor_price[df_labor_price['location'] == location]['worker price'].values[0]
    manager_price = df_labor_price[df_labor_price['location'] == location]['manager price'].values[0]

    # calculate the cost of workforce for automatic lines
    df['cost worker'] = worker_price * df['worker hour']
    df['cost manager'] = manager_price * df['manager hour']

    df['cost workforce'] = df['cost manager'] + df['cost worker']
    # print(df)
    return df

