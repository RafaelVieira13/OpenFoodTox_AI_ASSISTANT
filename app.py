# import libraries
import os
from langchain_community.llms import HuggingFaceHub
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import sqlite3
import re
import streamlit as st

### LLM Model -- Functions and Setting Up the Model ###

# setting api key
os.environ['HuggingFaceHub_API_TOKEN'] = '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'

# Function to Load the LLM model and provide sql query as response
def llm_response(question, prompt):
    llm=HuggingFaceHub(repo_id="google/gemma-2b-it")
    llm_chain = LLMChain(llm=llm ,prompt=prompt)
    response = llm_chain.run(question)
    return response


# Defining the Prompt

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


# Function to retrieve query from the SQL database
def read_sql_query(sql, db):
    print(sql)  # Print the SQL query before executing
    
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    
    print("Query result:")
    for row in rows:
        print(row)
    
    return rows


# Function to apply the model
def testing_model(question, prompt):
    llm_result = llm_response(question, prompt)

    # Using Regex to get just the Answer, which contains the sql command
    match = re.search(r'SQL QUERY:\s*(.*)', llm_result, re.MULTILINE)
    if match:
        sql_command = match.group(1).strip()
    else:
        print("No answer found.")

    # Using the sql_command on the read_sql_query
    data = read_sql_query(sql_command, "OpenFoodTox.db")[0][0]
    return data


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
    answer = testing_model(question, prompt)
    st.header(answer)

