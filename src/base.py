
from langchain.llms import OpenAI
from langchain import PromptTemplate
import os
import subprocess
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain, SequentialChain
import sys

TOPIC = sys.argv[1]


pdflatex_path = "/Library/TeX/texbin"  # for macOS
# pdflatex_path = "C:\\texlive\\2023\\bin\\win32"  # for Windows

# Add the path to the system PATH
os.environ["PATH"] += os.pathsep + pdflatex_path



def load_key_from_file(file_path = "openai_key.secret"):
    with open(file_path, 'r') as file:
        key = file.read().strip()
    return key

openai_api_key = load_key_from_file()




llm = OpenAI(model_name="text-davinci-003", openai_api_key=openai_api_key, max_tokens = 3500)

def write_string_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
def compile_tex(latex_code, tex_file='presentation.tex', output_dir='.'):
    # Write the LaTeX code to a .tex file
    with open(tex_file, 'w') as f:
        f.write(latex_code)

    # Define the path to pdflatex (you might need to adjust this according to your system)
    #pdflatex_path = "/usr/local/texlive/2023/bin/x86_64-linux"  # for Unix/Linux
    

    # Compile the .tex file to a .pdf
    process = subprocess.Popen(
        [
            "pdflatex",
            "-interaction=nonstopmode",
            "-output-directory={}".format(output_dir),
            tex_file
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        print("Error Occurred: ", stderr.decode())
    else:
        print("PDF was successfully created.")



def process_prompt(prompt):

    summary_template = """You are a super-intelligent, passionate educator with domain expertise in the topic you'll be responding about today.
    Your goal is to create a 5 minute slide deck tutorial on the topic that the user suggest, that is appropriate at the university level.
    Can you give a breakdown of the high level contents of the slide deck in a structured csv format.
    Include the number and time to be spent on each slide and high level bullet point summary of each slide. 
    The csv columns should be -- 
    1. Slide number
    2. Slide title
    3. Number of minutes to spend
    4. High level bullet points for the slide (seperated by ';')
    Include the header row as well. Return only the csv
    Keep the response to under 2000 tokens.
    % TOPIC
    {topic}

    YOUR RESPONSE:
    """
    prompt_template = PromptTemplate(input_variables=["topic"], template=summary_template)

    # Holds my 'summary' chain
    summary_chain = LLMChain(llm=llm, prompt=prompt_template, output_key = "outline")



    latex_template = """You are a super-intelligent, passionate educator with domain expertise in the topic you'll be responding about today.
    Your goal is to create a 5 minute slide deck tutorial on the topic that the user suggest, that is appropriate at the university level.
    Given a outline of a talk with the number of minutes on each slide can you create latex slides for the slides.
    Include details in your slides that would be appropriate at the university level. 
    Make sure there's something in there for all levels of students. 
    Your slides should not read like notes for yourself but a finished product that is self-explanatory to students who read it.
    Remember to fill in details from the bullet points you're given, make sure there's no images in it and include details but keep it under 2500 tokens.
    % OUTLINE
    {outline}

    YOUR RESPONSE:
    """
    prompt_template = PromptTemplate(input_variables=["outline"], template=latex_template)

    # Holds my 'slide' chain
    slide_chain = LLMChain(llm=llm, prompt=prompt_template, output_key = "latex")


    narrative_template = """You are a super-intelligent, passionate educator in the topic you'll be responding about today.
    Your goal is to create a slide deck tutorial on the topic that the user suggest, that is appropriate at the university level. 
    Given a outline of the talk, create the narrative that an instructor would speak while displaying the slide that is appropriate for the number of minutes in the plan.

    The text should be such that it sounds natural to speak and not necessarily to read, do not include things like the time duration of the slide or the title. The script will be read verbatim by an instructor.
    The content should be fun, engaging, include things not necessarily that is included in the slide. 
    Split the output by slide number, only return it as a list of strings. Make sure that the text is appropriate for the number of minutes planned for the specific slide for an instructor that speaks faster than average.

    
    % OUTLINE
    {outline}

    YOUR RESPONSE:
    """
    prompt_template = PromptTemplate(input_variables=["outline"], template=narrative_template)

    # Holds my 'meal' chain
    narrative_chain = LLMChain(llm=llm, prompt=prompt_template, output_key = "narrative")



    overall_chain = SequentialChain(
        chains=[summary_chain, slide_chain, narrative_chain],
        input_variables=["topic"],
        # Here we return multiple variables
        output_variables=["outline", "latex", "narrative"],
        verbose=True)


    review = overall_chain({'topic':  prompt})

    return review




#TOPIC = "Sorting algorithms"
output = process_prompt(TOPIC)
compile_tex(output["latex"])

output["outline"]


write_string_to_file('../data/narrative_' + TOPIC + '.txt', output["narrative"])        
write_string_to_file('../data/outline_' + TOPIC + '.txt', output["outline"])        
