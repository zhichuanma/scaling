import pandas as pd
import numpy as np
import math

'''
Inputs of the function:
    - op_time: unit hours per year
    - units: number of units to produce a year
    - technology

Outputs of the model:
    - dataframe of df equipment 
'''
def cost_equipment(op_time,units, technology,interest_rate):
    file_path = './Data/' + str(technology) + '/equipment.xlsx'
    df = pd.read_excel(file_path)

    # calculate the number of equipment based on the annual capacity and operating time.
    df['equipment number'] = np.ceil(units/op_time/df['Real throughput(unit/hour)'])

    # calculate the annualization factor
    df['annualization_factor'] = interest_rate * (1 + interest_rate)**df['lifetime(year)']/((1 + interest_rate)**df['lifetime(year)'] - 1)


    # calculate the purchase cost of the equipment
    df['CAPEX adjusted'] = np.maximum( df['CAPEX($)'] * df['equipment number'] ** df['b'],  df['CAPEX($)'] * 0.7) # when we purchase more, the unit price will be cheaper
    df['CAPEX purchase'] = df['CAPEX adjusted'] * df['equipment number']

    # calculate the other cost components of equipment
    df_cost_parameter = pd.read_csv('./Data/cost_parameters_equip.csv')

    df.loc[df['Type'] == 'Solid', 'CAPEX delivery'] = df_cost_parameter['Solid'][1] * df['CAPEX purchase']
    df.loc[df['Type'] == 'Solid.Fluid', 'CAPEX delivery'] = df_cost_parameter['Solid.Fluid'][1] * df['CAPEX purchase']
    df.loc[df['Type'] == 'Fluid', 'CAPEX delivery'] = df_cost_parameter['Fluid'][1] * df['CAPEX purchase']

    df.loc[df['Type'] == 'Solid', 'CAPEX installation'] = df_cost_parameter['Solid'][2] * df['CAPEX purchase']
    df.loc[df['Type'] == 'Solid.Fluid', 'CAPEX installation'] = df_cost_parameter['Solid.Fluid'][2] * df['CAPEX purchase']
    df.loc[df['Type'] == 'Fluid', 'CAPEX installation'] = df_cost_parameter['Fluid'][2] * df['CAPEX purchase'] 

    df.loc[df['Type'] == 'Solid', 'CAPEX instrument'] = df_cost_parameter['Solid'][3] * df['CAPEX purchase']
    df.loc[df['Type'] == 'Solid.Fluid', 'CAPEX instrument'] = df_cost_parameter['Solid.Fluid'][3] * df['CAPEX purchase']
    df.loc[df['Type'] == 'Fluid', 'CAPEX instrument'] = df_cost_parameter['Fluid'][3] * df['CAPEX purchase'] 

    df.loc[df['Type'] == 'Solid', 'CAPEX piping'] = df_cost_parameter['Solid'][4] * df['CAPEX purchase']
    df.loc[df['Type'] == 'Solid.Fluid', 'CAPEX piping'] = df_cost_parameter['Solid.Fluid'][4] * df['CAPEX purchase']
    df.loc[df['Type'] == 'Fluid', 'CAPEX piping'] = df_cost_parameter['Fluid'][4] * df['CAPEX purchase']   

    df.loc[df['Type'] == 'Solid', 'CAPEX engineer'] = df_cost_parameter['Solid'][5] * df['CAPEX purchase']
    df.loc[df['Type'] == 'Solid.Fluid', 'CAPEX engineer'] = df_cost_parameter['Solid.Fluid'][5] * df['CAPEX purchase']
    df.loc[df['Type'] == 'Fluid', 'CAPEX engineer'] = df_cost_parameter['Fluid'][5] * df['CAPEX purchase'] 

    df.loc[df['Type'] == 'Solid', 'CAPEX construction'] = df_cost_parameter['Solid'][6] * df['CAPEX purchase']
    df.loc[df['Type'] == 'Solid.Fluid', 'CAPEX construction'] = df_cost_parameter['Solid.Fluid'][6] * df['CAPEX purchase']
    df.loc[df['Type'] == 'Fluid', 'CAPEX construction'] = df_cost_parameter['Fluid'][6] * df['CAPEX purchase']

    df.loc[df['Type'] == 'Solid', 'CAPEX contract'] = df_cost_parameter['Solid'][7] * df['CAPEX purchase']
    df.loc[df['Type'] == 'Solid.Fluid', 'CAPEX contract'] = df_cost_parameter['Solid.Fluid'][7] * df['CAPEX purchase']
    df.loc[df['Type'] == 'Fluid', 'CAPEX contract'] = df_cost_parameter['Fluid'][7] * df['CAPEX purchase']

    df.loc[df['Type'] == 'Solid', 'CAPEX contigency'] = df_cost_parameter['Solid'][8] * df['CAPEX purchase']
    df.loc[df['Type'] == 'Solid.Fluid', 'CAPEX contigency'] = df_cost_parameter['Solid.Fluid'][8] * df['CAPEX purchase']
    df.loc[df['Type'] == 'Fluid', 'CAPEX contigency'] = df_cost_parameter['Fluid'][8] * df['CAPEX purchase'] 

    # print(df)
    df['cost equipment'] = df['CAPEX purchase'] +  df['CAPEX delivery'] +  df['CAPEX installation'] +  df['CAPEX instrument'] 
    + df['CAPEX piping'] +  df['CAPEX engineer'] +  df['CAPEX construction'] +  df['CAPEX contract'] +  df['CAPEX contigency']
    
    df['cost_equipment'] = df['cost equipment'] * df['annualization_factor']
    return df