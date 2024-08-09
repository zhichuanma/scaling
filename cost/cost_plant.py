import pandas as pd
import numpy as np
manufacturing_to_machine = 3.5
height_building = 5
price_envelope = 1671 #$/m2
lifetime_plant = 40 # years

'''
Inputs to the function
    - op_time: hours/year
    - units: number of units produced a year
    - technology
    - location: either China, EU or US.
'''


def cost_plant(op_time,units, technology,location,interest_rate):
    file_path = './Data/' + str(technology) + '/equipment.xlsx'
    df = pd.read_excel(file_path)

    # calculate the number of equipment based on the annual capacity and operating time.
    df['equipment number'] = np.ceil(units/op_time/df['Real throughput(unit/hour)'])

    # load the parameters to calculate the area of the plant
    df_parameters_building = pd.read_csv('./Data/cost_parameters_building.csv')

    # calculate the plant area
    df['area manufacturing'] = manufacturing_to_machine * df['equipment number'] * df['Gross area(m2)']
    df['area storage'] = df['area manufacturing'] * df_parameters_building['storage'][0]/ df_parameters_building['manufacturing'][0]
    df['area auxiliary'] = df['area manufacturing'] * df_parameters_building['auxiliary'][0]/ df_parameters_building['manufacturing'][0]
    df['area yard'] = df['area manufacturing'] * df_parameters_building['yard'][0]/ df_parameters_building['manufacturing'][0] 
    df['area total'] = df['area manufacturing']/ df_parameters_building['manufacturing'][0]

    # load plant price data
    df_land_price = pd.read_csv('./Data/land_price.csv')
    land_price = df_land_price[df_land_price['location'] == location]['land price($/m2)'].values[0]

    # Calculate the plant cost
    df['cost land'] = df['area total'] * land_price

    df['cost building'] = (np.sqrt(df['area total']) * height_building * 6 + 2* df['area total']) * price_envelope

    df['cost electrical'] = (df['area manufacturing'] * land_price * df_parameters_building[df_parameters_building['item'] == 'electrical_installations']['manufacturing'].values[0] +
                             df['area storage'] * land_price * df_parameters_building[df_parameters_building['item'] == 'electrical_installations']['storage'].values[0] +
                             df['area auxiliary'] * land_price * df_parameters_building[df_parameters_building['item'] == 'electrical_installations']['auxiliary'].values[0] +
                             df['area yard'] * land_price * df_parameters_building[df_parameters_building['item'] == 'electrical_installations']['yard'].values[0])
    
    df['cost yard'] = (df['area manufacturing'] * land_price * df_parameters_building[df_parameters_building['item'] == 'yard']['manufacturing'].values[0] +
                       df['area storage'] * land_price * df_parameters_building[df_parameters_building['item'] == 'yard']['storage'].values[0] +
                       df['area auxiliary'] * land_price * df_parameters_building[df_parameters_building['item'] == 'yard']['auxiliary'].values[0] +
                       df['area yard'] * land_price * df_parameters_building[df_parameters_building['item'] == 'yard']['yard'].values[0])

    df['cost service'] = (df['area manufacturing'] * land_price * df_parameters_building[df_parameters_building['item'] == 'service']['manufacturing'].values[0] +
                          df['area storage'] * land_price * df_parameters_building[df_parameters_building['item'] == 'service']['storage'].values[0] +
                          df['area auxiliary'] * land_price * df_parameters_building[df_parameters_building['item'] == 'service']['auxiliary'].values[0] +
                          df['area yard'] * land_price * df_parameters_building[df_parameters_building['item'] == 'service']['yard'].values[0])

    df['cost plant'] = df['cost land'] + df['cost electrical'] + df['cost yard'] + df['cost service'] + df['cost building']

    annualization_factor = interest_rate * (1 + interest_rate)**lifetime_plant/((1 + interest_rate)**lifetime_plant - 1)
    
    df['cost plant'] = annualization_factor * df['cost plant']
    # print(df)
    # print(df['area yard'])
    return df

