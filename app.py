# import functions
from functions import read_sql_query, llm_response, apply_model

# import libraries
#import os
#from langchain_community.llms import HuggingFaceHub
from langchain_core.prompts import PromptTemplate
#from langchain.chains import LLMChain
#import sqlite3
#import re
import streamlit as st



### Defining the Prompt ###
template = """
Context: You are an expert in converting English questions to SQL lite queries!
The SQL database has the name OpenFoodTox.db and has the following table Substance_Characterization with the following columns: Substance, has, Component, CASNumber,
ECRefNo, MolecularFormula, and smiles.
For example:
Example 1 - How many substances are available within OpenFoodTox?
The SQL command will be something like this: SELECT COUNT(DISTINCT Substance) FROM Substance_Characterization;
Example 2 - What is the CAS number of the Substance trans-3-Hexenyl hexanoate?
The SQL command will be something like this: SELECT CASNumber FROM Substance_Characterization WHERE Substance = 'trans-3-Hexenyl hexanoate';
Also, the SQL command should not have ' and the () at the beginning or at the end of the SQL word in the output.Your output should be just the SQL command. 
For example:
If I ask you 'What is the CAS number of the Substance trans-3-Hexenyl hexanoate?' Your output must be just the SQL command, like this:  SELECT CASNumber FROM Substance_Characterization WHERE Substance = 'trans-3-Hexenyl hexanoate'.
Don't Say anything else!!!!!
Question: {query}

SQL QUERY: """

prompt = PromptTemplate(input_variables=['query'],
                                       template = template)


### Creating streamlit app ###
page_title="I can help you to analyse the OpenFoodTox database"
layout = 'centered'

st.set_page_config(page_title=page_title,layout=layout)

st.header("OpenFoodTox AI Analyzer")
st.write("Hello I'm your AI assistant and I'm here to help you to gain insights about the OpenFoodTox database")
st.image(image='openfoodtox_update.png', width=600)


with st.sidebar:
    st.image(image='EFSA_horizon_RGB_EN 1@4x.png')
    st.header('*What Is the OpenFoodTox AI Analyzer?*')
    st.write('''OpenFoodTox is your go-to resource for understanding chemical hazards in food. It's an open-source database filled with toxicological information, accessible to everyone.

And now, with the OpenFoodTox AI Analyzer, you have an easy-to-use tool at your fingertips. It's perfect for risk assessors, managers, and anyone else involved in food safety.

Here's what it offers:

* Instant access to toxicological data through prompt responses.
* Quick identification of chemical hazards in food products.''')
    st.divider()
    st.caption("Author: Rafael Vieira;  rafael11934@hotmail.com")


question = st.text_input("Question", key='input')
submit = st.button('Ask the question')

# if submit is clicked
if submit:
    model_name = "google/gemma-7b"
    answer = apply_model(model_name=model_name,question=question, prompt=prompt)
    st.header(answer)

