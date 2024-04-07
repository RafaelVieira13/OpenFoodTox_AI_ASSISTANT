# libraries
from langsmith import Client
from langchain.smith import RunEvalConfig, run_on_dataset

client = Client()

# ---------------
# Model Evaluation
# --------------- 

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

# ------------------------------
# 2. Evaluate Datasets with LLM
# ------------------------------