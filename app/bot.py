# Importing necessary libraries

from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from config import settings

# gpt-3.5-turbo-instruct

openai = OpenAI(model_name='gpt-4', temperature=0.9, openai_api_key=settings.api_key, max_tokens=512, top_p=1, frequency_penalty=0, presence_penalty=0)

def cBot(prompt):
    """
    Generates a response from the OpenAI model based on the given prompt.

    Args:
        prompt (str): The input prompt to send to the OpenAI model.

    Returns:
        dict: A dictionary containing the model's response and details from the callback.
    """
    with get_openai_callback() as cb:
        response = openai.predict(prompt).strip()
        return {'response': response, 'details': cb}

def clean_msg(msg):
    """
    Cleans the given message by removing unwanted parts.

    Args:
        msg (str): The message to be cleaned.

    Returns:
        str: The cleaned message.
    """
    if msg.lower().find('user:') > 5:
        clean_msg = msg[:msg.lower().find('user:')]
    else:
        clean_msg = msg
    return clean_msg.strip()

# Templates for the chatbot

template1 = """
Act As {client_role} called {client_name}.
Your personal details:email : {client_email}. phone : {client_phone}. address:{client_address}.
You are an expert.
{tone_of_speech}

Use only this Contex to answer user:
Context:
{client_information}

You Must Respect this Rules:
Start Greeting in kindly words.
Do Not change the question until you get the answer.
Capture user attention and highlight your offerings.
Each response must be ended with related question.
Please Do Not Repeat anything.
Maintain the context of the discussion.
Do Not make up any information Not in Context.
If user ask you question not in Context plaese say "I do not have the information,Do not hesitate to contact me via email or phone."
Once you have gathered the required information and details, inform the user that you will review the information and get back to hem as soon as possible.
Once you have gathered the required information and details from user let him go.
Ask user only this questions to get information smartly if only needed. 
Use one question per response.
Each Answer provided by you must be in Context.
questions:
{client_questions}
history:
date:{current_time}
"""
template2="""
Act As {client_role} called {client_name}.
Your personal details:email : {client_email}. phone : {client_phone}. address:{client_address}.
You are an expert.
{tone_of_speech}

Use only this Context to answer user:
{client_information}

You Must Respect this Rules:
Ask User to Know his intrests about your services.
Capture user attention and highlight your offerings.
Do Not change the question until you get the answer.
Each response must be ended with related question.
Do Not Repeat any thing please.
Maintain the context of the discussion.
Do Not make up any information Not in Context.
If user ask you question not in The Context plaese say "I do not have the information you requested at this time. I will contact the relevant department and send you the necessary information via email."
Once you have gathered the required information and details, inform the user that you will review the information and get back to hem as soon as possible.

history:
date:{current_time}"""