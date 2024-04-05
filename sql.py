import sqlite3
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


'''
1. Reading OpenFoodTox Excel File
'''
# reading each excel file
subst_charact = pd.read_csv('SubstanceCharacterisation_KJ_2022.csv')
genotoxicity = pd.read_csv('Genotoxicity_KJ_2022.csv')
efsa_outputs = pd.read_csv('EFSAOutputs_KJ_2022.csv')

#genotoxicity = pd.read_excel('Genotoxicity_KJ_2022.xlsx')

'''
2. OpenFoodTox database creation
'''

# Connecting to sqlite
connection = sqlite3.connect('OpenFoodTox_TEST.db')


# Create a cursor object to insert record, cretate a table, retrieve
cursor = connection.cursor()

# Loading each dataframe to sqlite
subst_charact.to_sql('Substance_Characterization', connection, if_exists='replace')
genotoxicity.to_sql('Genotoxicity', connection, if_exists='replace')
efsa_outputs.to_sql('EFSAOUTPUTS', connection, if_exists='replace')

# Closing Connection
connection.commit()
connection.close()
    
