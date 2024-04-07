# import functions
from functions import read_sql_query, llm_response, apply_model

# import libraries
from langchain_core.prompts import PromptTemplate
from langsmith import Client
from langchain.smith import RunEvalConfig, run_on_dataset
import streamlit as st
import os

# --------------- LangSmith Setup
os.environ['LANGCHAIN_TRACING_V2']="true"
os.environ['LANGCHAIN_ENDPOINT']="https://api.smith.langchain.com"
os.environ['LANGCHAIN_API_KEY']="ls__8ba8cebf388a4bbca87ffdd714f18150"
os.environ['LANGCHAIN_PROJECT']="OpenFoodTox AI Analyzer"

client = Client()
# ---------------

### Defining the Prompt ###
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
The SQL command will be something like this: SELECT COUNT(DISTINCT Substance) FROM;

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

Example 11 - Give me the average reference value by assessment for the following substance: '(Z)-Nerol'?
The SQL command will be something like this: SELECT DISTINCT Assessment, AVG(value) as avg, unit FROM Reference_Values WHERE Substance='(Z)-Nerol' GROUP BY Assessment ORDER BY avg DESC;

Example 12 - What are the reported effects for the following susbstance: '(2E)-Methylcrotonic acid' ? 
The SQL command will be something like this:SELECT DISTINCT Effect FROM REFERENCE_POINTS WHERE SUBSTANCE='(2E)-Methylcrotonic acid';

Example 13 - Tell me the average endpoint values for the following substance: '(RS)-2,4-dinitro-6-(octan-2-yl)phenyl (2 E/Z)-but-2-enoate'?
The SQL command will be something like this: SELECT Substance, Endpoint, AVG(value) AS avg, unit FROM REFERENCE_POINTS WHERE SUBSTANCE=''(RS)-2,4-dinitro-6-(octan-2-yl)phenyl (2 E/Z)-but-2-enoate' GROUP BY Endpoint ORDER BY avg DESC;

Example 14 - What is the average endpoint value by each study?
The SQL command will be something like this: SELECT Study, Endpoint, AVG(value) AS avg, unit FROM REFERENCE_POINTS GROUP BY Endpoint ORDER BY avg DESC;

Example 15 - What is the average NOEL value for the following substance: '1,1-bis(Ethylthio)-ethane'?
The SQL command will be something like this: SELECT AVG(value), unit FROM REFERENCE_POINTS WHERE Study='NOEL';

Example 16 - What is the average NOAEL value for rats?
The SQL command will be something like this: SELECT AVG(value), unit FROM REFERENCE_POINTS WHERE Study='NOAEL' AND Species='Rat';

Example 18 - What is the average LD50 value for the following study: 'Human health'?
The SQL command will be something like this: SELECT AVG(value), unit FROM REFERENCE_POINTS WHERE Study='LD50' AND Study='Human health';

Example 19 - How many studies are available for 'Human health'?
The SQL command will be something like this:SELECT COUNT (DISTINCT OutputID) FROM REFERENCE_POINTS WHERE Study = 'Human health';

Example 20 - How many EFSA outputs are available for the following study: 'Human health'?
The SQL command will be something like this:SELECT COUNT (DISTINCT OutputID) FROM REFERENCE_POINTS WHERE Study = 'Human health';

Example 21 - Within OpenFoodTox how many outputs are available for 'Animal (target species) health'?
The SQL command will be something like this:SELECT COUNT (DISTINCT OutputID) FROM REFERENCE_POINTS WHERE Study = 'Animal (target species) health';

Example 21 - Within OpenFoodTox how many outputs are available for each study?
The SQL command will be something like this:SELECT Study ,COUNT (DISTINCT OutputID) AS count FROM REFERENCE_POINTS GROUP BY Study ORDER BY count DESC;

Also, the SQL command should not have ' and the () at the beginning or at the end of the SQL word in the output.Your output should be just the SQL command. 
For example:
If I ask you 'What is the CAS number of the Substance trans-3-Hexenyl hexanoate?' Your output must be just the SQL command, like this:  SELECT CASNumber FROM Substance_Characterization WHERE Substance = 'trans-3-Hexenyl hexanoate'.
Don't Say anything else!!!!!


Question: {query}

SQL QUERY: """

prompt = PromptTemplate(input_variables=['query'],
                                       template = template)


# --------------- Streamlit APP

page_title="I can help you to analyse the OpenFoodTox database"
layout = 'wide'
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
    data = apply_model(model_name=model_name,question=question, prompt=prompt)
    st.subheader('Answer:')
    for row in data:
        print(row)
        st.header(row)
# ---------------


# --------------- Model Evaluation

# 1. Create a Dataset (Only Inputs, No outputs)
example_inputs = ["How many substances are available within the OpenFoodTox database?",
             "Within OpenFoodTox how many substances have a CASnumber?",
             "What is the CASnumber for the following substance '(+)-13alpha-Tigloyloxylupanine'?",
             "What is the  CASnumber for the following substance '(-)-alpha-Santalene'?",
             "What is the CASnumber for the following substance '(2E)-3-(2-Anilino-6-methyl-4-pyrimidinyl)-2-propen-1-ol'?",
             "What is the substance name from the following CASnumber: 110-44-1' ? ",
             "What is the substance name from the following CASnumber: 19342-01-9' ?",
             "What is the molecular formula from the following CASnumber: 6119-92-2 ? ",
             "What are the smiles from the following CASnumber: 1113-21-9?",
             "What are the smiles from the following CASnumber: 110235-47-7?",
             "What are the smiles from the following Substance: (+)-Alpha-cedrene?",
             #"What are the ECRefNo for the following Substance: (2E,7R,11R)-Phytol ?",
             "What is the Substance name of the following smiles: C[C@@H](CCC[C@@H](C)CCC/C(=C/COC(=O)C)/C)CCCC(C)C ?",
             "Regarding the 2,3,4,6-Tetrachloro-5-cyanobenzamide substance what is it's component and smiles? ",
             "Tell me the cas number of the following substance: 1,2,3-Trimethoxybenzene",
             "How many substances are genotoxic?",
             "Is the following substance'(+)-Lupanine' genotoxic?",
             "Is the following substance genotoxic '(-)-Bornyl acetate'?",
             "How many substances are not genotoxic?",
             "How many substances are genotoxic?",
             "Give me a list with all the genotoxic substances",
             "How many Efsa opinions are available in OpenFoodTox?",
             "How many Efsa opinions are available in OpenFoodTox for the following substance: '3,5,6-Trichloro-2-pyridinol'?",
             "How many Efsa statements are available in OpenFoodTox for the following substance: '3,5,6-Trichloro-2-pyridinol'?",
             "What is the average reference value by each population?",
             "What is the average reference value for the following susbtance: '1-Ethoxy-1-(3-hexenyloxy)ethane'?",
             "What is the average reference value by assessment for the following substance: '(R)-(-)-Lavandulol'?",
             "Tell me the average reference value for consumers population",
             "What are the reported effects for the following susbstance: '1,3-Dichloropropene' ?",
             "Which one is the substance with the highest reference value?",
             "Tell me the average endpoint values for the following substance: '(S)-1-(3-(((4-amino-2,2-dioxido-1H-benzo[c][1,2,6]thiadiazin-5-yl)oxy)methyl)piperidin-1- yl)-3-methylbutan-1-one'?",
             "Within OpenFoodTox how many outputs are available for each study?",
             "How many EFSA outputs are available for the following study: 'Human health'?",
             "How many studies are available for 'Ecotox (soil compartment)'?"]

dataset_name = 'OpenFoodTox Questions'

# Storing inputs in as dataset lets us
# run chains and LLMs over s shared set of examples
dataset = client.create_dataset(
    dataset_name=dataset_name,
    description="Prompts Examples"
)

for input_prompt in example_inputs:
    # Each example must be unique and have inputs defines.
    # Outputs are optional
    client.create_example(
        inputs={'question': input_prompt},
        outputs = None,
        dataset_id=dataset.id
    )



