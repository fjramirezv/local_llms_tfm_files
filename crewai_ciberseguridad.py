from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
#import Ollama

os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
os.environ["OPENAI_MODEL_NAME"] ='ALPHA_generic'
os.environ["OPENAI_API_KEY"] ='sk-111111111111111111111111111111111111111111111111'

AG = Ollama(model="ALPHA_generic")
GC = Ollama(model="GAMMA_code")

# Agentes para detección y corrección de sesgos
bias_detection_agent = Agent(
    role='Bias Detector',
    goal='Identify potential biases in Python code',
    backstory='Specialist in analyzing Python code for biases',
    verbose=True,
    allow_delegation=False,
    llm=AG
)

code_correction_agent = Agent(
    role='Code Corrector',
    goal='Modify Python code to address identified biases',
    backstory='Expert in correcting biases in Python code to ensure fairness and accuracy',
    verbose=True,
    allow_delegation=False,
    llm=GC
)

# Tareas para detección y corrección de sesgos
def detect_bias_task(code_text):
    return Task(
        description=f"Read the following Python code and identify any possible biases:\n{code_text}\nPlease list all potential biases found.",
        agent=bias_detection_agent,
        expected_output="List of potential biases"
    )

def correct_bias_task(bias_report, code_text):
    return Task(
        description=f"Given the following bias report:\n{bias_report}\nAnd the original Python code:\n{code_text}\nPlease modify the Python code to address these biases and create a bias-free version.",
        agent=code_correction_agent,
        expected_output="Modified Python code without biases"
    )

# Solicitar el archivo de código fuente
code_file_path = "RandomForest_Bias.py"

# Leer el código fuente
with open(code_file_path, 'r') as file:
    python_code = file.read()

# Crear la instancia de Crew con las tareas
crew = Crew(
    agents=[bias_detection_agent, code_correction_agent],
    tasks=[detect_bias_task(python_code), correct_bias_task("", python_code)],  # Inicializar con el texto de código y un reporte vacío inicialmente
    verbose=2,
)

# Ejecutar las tareas con Crew
results = crew.kickoff()  # Se lanzan las tareas

print("--------------------------")
print("Final Code After Bias Correction:")
print(results)
