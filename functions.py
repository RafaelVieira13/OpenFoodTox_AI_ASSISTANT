from langchain_community.llms import HuggingFaceHub
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import re
import sqlite3

# setting api key
os.environ['HuggingFaceHub_API_TOKEN'] = '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'


# Function to Load the LLM model and provide sql query as response
def llm_response(model_name, question, prompt):
    llm=HuggingFaceHub(repo_id=model_name)
    llm_chain = LLMChain(llm=llm ,prompt=prompt)
    response = llm_chain.run(question)
    return response

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
def apply_model(model_name, question, prompt):
    llm_result = llm_response(model_name, question, prompt)

    # Using Regex to get just the Answer, which contains the sql command
    match = re.search(r'SQL QUERY:\s*(.*)', llm_result, re.MULTILINE)
    if match:
        sql_command = match.group(1).strip()
    else:
        print("No answer found.")

    # Using the sql_command on the read_sql_query
    data = read_sql_query(sql_command, "OpenFoodTox_TEST.db")
    return data