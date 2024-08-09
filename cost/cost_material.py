import pandas as pd
import numpy as np

def cost_material(units, technology, location):

    file_path = './Data/' + str(technology) + '/equipment.xlsx'
    df = pd.read_excel(file_path)

    file_path = './Data/' + str(technology) + '/material.xlsx'
    df_material = pd.read_excel(file_path)

    # load material price database
    df_material_price = pd.read_csv('./Data/material_price.csv')
    df_material_price['b'] =  np.log2(df_material_price['m'])
    df_material_price['Purchase price'] =  np.maximum(df_material_price['Price'] * df_material_price['m'], df_material_price['Price'] * (units/df_material_price['AtVolume'])**df_material_price['b'])

    # Calculate the yields in material consumption 
    mapping_yileds = dict(zip(df['Section'], df['Yields section'])) # Create a dictionary mapping sections to their corresponding values from df2
    df_material['Yields'] = df_material['Section'].map(mapping_yileds)

    mapping_price = dict(zip(df_material_price['item'],df_material_price['Purchase price']))
    df_material['Purchase price'] = df_material['Material'].map(mapping_price)

    df_material['Consumption real'] = df_material['Consumption']/df_material['Yields']
    df_material['cost material'] = df_material['Consumption real'] * df_material['Purchase price']
 
    # print(df_material)

    return df_material

