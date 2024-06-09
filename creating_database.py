import sqlite3
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


'''
1. Reading OpenFoodTox Excel File
'''
# reading each excel file
subst_charact = pd.read_csv('data\SubstanceCharacterisation_KJ_2022.csv')
genotoxicity = pd.read_csv('data\Genotoxicity_KJ_2022.csv')
efsa_outputs = pd.read_csv('data\EFSAOutputs_KJ_2022.csv')
ref_values = pd.read_csv('data\ReferenceValues_KJ_2022.csv')
ref_points = pd.read_csv('data\ReferencePoints_KJ_2022.csv')

'''
2. OpenFoodTox database creation
'''
try:
    # Connecting to sqlite
    connection = sqlite3.connect('OpenFoodTox.db')


    # Create a cursor object to insert record, cretate a table, retrieve
    cursor = connection.cursor()

    # Loading each dataframe to sqlite
    subst_charact.to_sql('Substance_Characterization', connection, if_exists='replace')
    genotoxicity.to_sql('Genotoxicity', connection, if_exists='replace')
    efsa_outputs.to_sql('EFSAOUTPUTS', connection, if_exists='replace')
    ref_values.to_sql('Reference_Values', connection, if_exists='replace')
    ref_points.to_sql('Reference_Points', connection, if_exists='replace')

    # Closing Connection
    connection.commit()
    connection.close()

    print('Data Successfully Stored into Database')

except Exception as e:
    print(f'Error While Storing Data Into Database: {e}')
    