import sqlite3
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Connecting to sqlite
connection = sqlite3.connect('OpenFoodTox.db')

# Create a cursor object to insert record, cretate a table, retrieve
cursor = connection.cursor()

# Reading the data from the CSV file
df = pd.read_csv('SubstanceCharacterisation_KJ_2022.csv')

# Load df to sqlite
df.to_sql('Substance_Characterization', connection, if_exists='replace')

# Performing some queries to test the database
data = cursor.execute('''SELECT CASNumber 
                      FROM Substance_Characterization 
                      WHERE Substance = 'trans-3-Hexenyl hexanoate'
''')
for row in data:
    print(row)

# Closing Connection
connection.commit()
connection.close()
    
