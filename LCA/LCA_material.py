import pandas as pd
import numpy as np
'''
Inputs of the function:
    - op_time: unit hours per year
    - units: number of units to produce a year
    - technology

Outputs of the model:
    - dataframe of df equipment 
    - due to the lack of consumable's and assembly's information, the output of their impacts will be 0
'''
def LCA_material(units, technology, location, lca_indicators):

    file_path = './Data/' + str(technology) + '/equipment.xlsx'
    df = pd.read_excel(file_path)

    file_path = './Data/' + str(technology) + '/material.xlsx'
    df_material = pd.read_excel(file_path)

    # import metrics of all LCA indicators
    '''
    columns: LCA indicators
    rows: materials
    '''
    file_path = './Data/LCA_metrics.csv'
    df_LCA_metrics = pd.read_csv(file_path)

    # specify the location
    df_LCA_metrics = df_LCA_metrics[df_LCA_metrics['location'] == location]

    # Calculate the yields in material consumption 
    mapping_yileds = dict(zip(df['Section'], df['Yields section'])) # Create a dictionary mapping sections to their corresponding values from df2
    df_material['Yields'] = df_material['Section'].map(mapping_yileds)

    df_material['Consumption real'] = df_material['Consumption']/df_material['Yields']

    # LCA
    for indicators in lca_indicators:
        mapping_LCA = dict(zip(df_LCA_metrics['Materials'], df_LCA_metrics[indicators]))

        df_material[str(indicators)] = df_material['Material'].map(mapping_LCA)
        df_material[str(indicators) + ' material'] = df_material[str(indicators)] * df_material['Consumption real']

    return df_material

