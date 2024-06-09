# Import functions
from functions import read_sql_query, llm_response, apply_model

# Import libraries
from langchain_core.prompts import PromptTemplate
import streamlit as st
import os
import pandas as pd
import re

# --------------- 
# LangSmith Setup
# ---------------
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"
os.environ['LANGCHAIN_API_KEY'] = "ls__8ba8cebf388a4bbca87ffdd714f18150"
os.environ['LANGCHAIN_PROJECT'] = "OpenFoodTox AI Analyzer"

# ---------------
# Defining the Prompt
# ---------------
template = """
Context: You are an expert in converting English questions to SQL lite queries!
The SQL database has the name OpenFoodTox_TEST.db and has the following tables:
 - Substance_Characterization with the following columns: Substance, has, Component, CASNumber, ECRefNo, MolecularFormula, and smiles.
 - Genotoxicity with the following columns: Substance, Author, Year, OutputID, Genotoxicity.
 - EFSAOUTPUTS with the following columns: Substance, OutputID, LegalBasis, Panel, Published, Title, OutputType, DOI, URL.
 - Reference_Values with the following columns: Substance, Author, Year, OutputID, Assessment, qualfier, value, unit, Population.
 - Reference_Points with the following columns: Substance, Author, Year, OutputID, Study, TestType, Species, Route, DurationDays, Endpoint, qualifier, value, unit, Effect, Toxicity

For example:
Example 1 - How many substances are available within OpenFoodTox?
The SQL command will be something like this: SELECT COUNT(DISTINCT Substance) FROM Substance_Characterization;

Example 2 - What is the CAS number of the Substance trans-3-Hexenyl hexanoate?
The SQL command will be something like this: SELECT CASNumber FROM Substance_Characterization WHERE Substance = 'trans-3-Hexenyl hexanoate';

Example 3 - How many substances are not genotoxic?
The SQL command will be something like this: SELECT COUNT(DISTINCT Substance) FROM Genotoxicity WHERE Genotoxicity = 'Negative';

Example 4 - How many substances are genotoxic?
The SQL command will be something like this: SELECT COUNT(DISTINCT Substance) FROM Genotoxicity WHERE Genotoxicity = 'Positive';

Example 5 - Is the following substance'(+)-Lupanine' genotoxic?
The SQL command will be something like this: SELECT DISTINCT Genotoxicity FROM Genotoxicity WHERE Substance = '(+)-Lupanine';

Example 6 - How many Efsa opinions are available in OpenFoodTox?
The SQL command will be something like this: SELECT COUNT(DISTINCT OutputID) FROM EFSAOUTPUTS WHERE OutputType = 'EFSA opinion';

Example 7 - How many Efsa opinions are available in OpenFoodTox for the following substance: '(-)-Alpha-elemol'?
The SQL command will be something like this: SELECT COUNT(DISTINCT OutputID) FROM EFSAOUTPUTS WHERE OutputType = 'EFSA opinion' AND Substance = '(-)-Alpha-elemol';

Example 8 - Tell me how many EFSA statements are available in OpenFoodTox?
The SQL command will be something like this: SELECT COUNT(DISTINCT OutputID) FROM EFSAOUTPUTS WHERE OutputType = 'EFSA statement';

Example 9 - What is the average reference value by each population?
The SQL command will be something like this: SELECT DISTINCT Population, AVG(value) as avg, unit FROM Reference_Values GROUP BY Population ORDER BY avg DESC;

Example 10 - What is the average reference value for the following susbtance: '(R)-(-)-Lavandulol'?
The SQL command will be something like this: SELECT AVG(value) as avg, unit FROM Reference_Values WHERE Substance='(R)-(-)-Lavandulol';

Example 11 - What is the average reference value by assessment?
The SQL command will be something like this: SELECT DISTINCT Assessment, AVG(value) as avg, unit FROM Reference_Values GROUP BY Assessment ORDER BY avg DESC;

Example 12 - What are the reported effects for the following susbstance: '(2E)-Methylcrotonic acid'?
The SQL command will be something like this: SELECT DISTINCT Effect FROM Reference_Points WHERE Substance='(2E)-Methylcrotonic acid';

Example 13 - Tell me the average endpoint values for the following substance: '(RS)-2,4-dinitro-6-(octan-2-yl)phenyl (2 E/Z)-but-2-enoate'?
The SQL command will be something like this: SELECT Substance, Endpoint, AVG(value) AS avg, unit FROM Reference_Points WHERE Substance='(RS)-2,4-dinitro-6-(octan-2-yl)phenyl (2 E/Z)-but-2-enoate' GROUP BY Endpoint ORDER BY avg DESC;

Example 14 - What is the average endpoint value by each study?
The SQL command will be something like this: SELECT Study, Endpoint, AVG(value) AS avg, unit FROM Reference_Points GROUP BY Endpoint ORDER BY avg DESC;

Example 15 - What is the average NOEL value for the following substance: '1,1-bis(Ethylthio)-ethane'?
The SQL command will be something like this: SELECT AVG(value), unit FROM Reference_Points WHERE Study='NOEL' AND Substance='1,1-bis(Ethylthio)-ethane';

Example 16 - What is the average NOAEL value for rats?
The SQL command will be something like this: SELECT AVG(value), unit FROM Reference_Points WHERE Study='NOAEL' AND Species='Rat';

Example 17 - What is the average LD50 value for the following study: 'Human health'?
The SQL command will be something like this: SELECT AVG(value), unit FROM Reference_Points WHERE Study='LD50' AND Study='Human health';

Example 18 - How many studies are available for 'Human health'?
The SQL command will be something like this: SELECT COUNT(DISTINCT OutputID) FROM Reference_Points WHERE Study = 'Human health';

Example 19 - How many EFSA outputs are available for the following study: 'Human health'?
The SQL command will be something like this: SELECT COUNT(DISTINCT OutputID) FROM Reference_Points WHERE Study = 'Human health';

Example 20 - Within OpenFoodTox how many outputs are available for 'Animal (target species) health'?
The SQL command will be something like this: SELECT COUNT(DISTINCT OutputID) FROM Reference_Points WHERE Study = 'Animal (target species) health';

Example 21 - Within OpenFoodTox how many outputs are available for each study?
The SQL command will be something like this: SELECT Study, COUNT(DISTINCT OutputID) AS count FROM Reference_Points GROUP BY Study ORDER BY count DESC;

Also, the SQL command should not have ' and the () at the beginning or at the end of the SQL word in the output. Your output should be just the SQL command. 
For example:
If I ask you 'What is the CAS number of the Substance trans-3-Hexenyl hexanoate?' Your output must be just the SQL command, like this:  SELECT CASNumber FROM Substance_Characterization WHERE Substance = 'trans-3-Hexenyl hexanoate'.
Don't Say anything else!!!!!

Question: {query}

SQL QUERY: """

prompt = PromptTemplate(input_variables=['query'], template=template)

# ---------------
# Streamlit APP
# ---------------

page_title = "I can help you to analyse the OpenFoodTox database"
layout = 'wide'
st.set_page_config(page_title=page_title, layout=layout)

with st.sidebar:
    st.image(image='images/EFSA_horizon_RGB_EN 1@4x.png')
    st.header('*What Is the OpenFoodTox AI Analyzer?*')
    st.write('''
OpenFoodTox is your go-to resource for understanding chemical hazards in food. It's an open-source database filled with toxicological information, accessible to everyone.

And now, with the OpenFoodTox AI Analyzer, you have an easy-to-use tool at your fingertips. It's perfect for risk assessors, managers, and anyone else involved in food safety.

Here's what it offers:

* Instant access to toxicological data through prompt responses.
* Quick identification of chemical hazards in food products.''')
    st.divider()
    st.caption("Author: Rafael Vieira; rafael11934@hotmail.com")

question = st.text_input("Make your Question:", key='input')
submit = st.button('Send')

# If submit is clicked
if submit:
    model_name = "google/gemma-7b"
    data = apply_model(model_name=model_name, question=question, prompt=prompt)
    
    st.write('Answer:')
    if data:
        data_download = pd.DataFrame(data)
        st.write(data_download)
    else:
        st.subheader('Answer:')
        st.write("No data returned from the model.")





