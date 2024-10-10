# Importing necessary libraries

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from bot import cBot, clean_msg
from database import Database
from models import Static
import time

router = APIRouter()

@router.get("/chat/", summary="Start a chat", response_description="Chat response from cBot")
async def chat(user_id: str, user_msg: str):
    """
    Starts a chat with the user and returns the response from the cBot.

    Args:
        user_id (str): The ID of the user.
        user_msg (str): The message from the user.

    Returns:
        dict: A dictionary containing the response from the cBot.

    Raises:
        HTTPException: If there is an error during the database operation.
    """
    try:
        conversation = Database.retrieve_records_as_dicts('Users', id=user_id)[0]['conversation']
        conversation = conversation + '\nuser:' + user_msg + '\nbot:'
        response = cBot(conversation)['response']
        response = clean_msg(response).strip()
        conversation += response
        Database.update_table_values('Users', {'conversation': conversation}, "id = {}".format(user_id))
        return {'data': [response]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summarize/", summary="Summarize conversation", response_description="Conversation summary generated")
async def summarize(user_id: str):
    """
    Summarizes the conversation for the specified user and fills out a table with requirements.

    Args:
        user_id (str): The ID of the user.

    Returns:
        dict: A dictionary containing the summary of the conversation.

    Raises:
        HTTPException: If there is an error during the database operation.
    """
    current_time = str(time.localtime().tm_mday) + '-' + str(time.localtime().tm_mon) + '-' + str(time.localtime().tm_year)
    try:
        conversation = Database.retrieve_records_as_dicts('Users', id=user_id)[0]['conversation']
        start = conversation.lower().find("history:")
        prompt = """Use the following conversation:
date:{current_time}
Conversation:
{chat_history}

END OF Conversation

To Complete the following table with Requirements.
if No value set field to N/A.
Do Not make up any Value.
Find this Requirements:{fields}
output Must Be table:
Table:
| Requirement        | Value           |
|--------------------|-----------------|
|                    |                 |
|                    |                 | """.format(current_time=current_time, chat_history=conversation[start:], fields=Static.requirements)

        response = cBot(prompt)['response']
        Static.requirments = ''
        return {'cbot_summary': response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
