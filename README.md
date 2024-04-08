# OpenFoodTox AI Analyzer

 ## What is the OpenFoodTox Analyzer?
OpenFoodTox is your go-to resource for understanding chemical hazards in food. It's an open-source database filled with toxicological information, accessible to everyone.
And now, with the OpenFoodTox AI Analyzer, you have an easy-to-use tool at your fingertips. It's perfect for risk assessors, managers, and anyone else involved in food safety.

Here's what it offers:
* Instant access to toxicological data through prompt responses.
* Quick identification of chemical hazards in food products.

## How the App Works?
![image](https://github.com/RafaelVieira13/OpenFoodTox_AI_ASSISTANT/assets/129581165/c7597402-84cc-4e5a-89c4-f228ec1a4dcd)

The OpenFoodTox AI Analyzer operates by providing prompts within the application.These prompts are then transformed into SQL queries using Google Gemma 7b LLM. Subsequently, a Python function is invoked to extract the SQL query from the model's output, which in turn is utilized to retrieve the final answer from the SQL database

## Tools Used
* Model Name: Google Gemma 7b
* Programming Languages: Python and SQL
* AI Framework: LangChain
* Front-end : Streamlit
* Model Fine-Tuning Library: Transformers
* Model Evaluation/Monitorization: LangSmith
*  Databse: SQL Lite

## Project Architecture

![image](https://github.com/RafaelVieira13/OpenFoodTox_AI_ASSISTANT/assets/129581165/c4ae1821-06b9-45d2-8fa1-4c90b0c3f3e9)

* Python/SQL Script: https://github.com/RafaelVieira13/OpenFoodTox_AI_ASSISTANT/blob/one_openfoodtox_table/sql.py
* Functions to Call the Model and Convert Prompt to SQL Query and to a Real Answer: https://github.com/RafaelVieira13/OpenFoodTox_AI_ASSISTANT/blob/one_openfoodtox_table/functions.py
* App Creation: https://github.com/RafaelVieira13/OpenFoodTox_AI_ASSISTANT/blob/one_openfoodtox_table/app.py

## Advantages
* Faster way to perform qucik analysis about OpenFoodTox;
* More user-firendly way to analyse OpenFoodTox;
* More intuitive;
* Enhance user interactions

## Limitations
* Not suitable for advance analysis;
* Model doesn't recognize the difference between some words (e.g with and without);
* May generate wrong answers;

 ## Final APP
 * Streamlit WebAPP: https://oftaiassistant.streamlit.app/
 * Langsmith: https://www.langchain.com/langsmith

  ## Further Work
  * OpenFoodTox SQL Database update and maintenance.
  * Model Evaluation
  * Collection of prompts and respective answers
  * If necessary fine-tunne the model to improve accuracy
  * Switch OpenSource tools to cloud
