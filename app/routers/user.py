# Importing necessary libraries
from fastapi import APIRouter, HTTPException
from database import Database
from bot import template1, template2
import time
import sqlite3

router = APIRouter()

@router.post("/add_user/", summary="Add a new user", response_description="User added successfully")
async def create_user(data: dict):
    """
    Adds a new user record to the 'Users' table.

    Args:
        data (dict): A dictionary containing user information.

    Returns:
        dict: A dictionary containing the ID of the new user and the client email.

    Raises:
        HTTPException: If there is an error during the database operation.
    """
    email = data['user']
    client_email = data['client']

    try:
        # Check if the user already exists
        existing_user = Database.retrieve_records_as_dicts('Users', email=email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists.")
        
        # Insert the new user if they don't already exist
        id_ = None
        retry_attempts = 3
        while retry_attempts > 0:
            try:
                id_ = Database.insert_record('Users', {
                    'email': email,
                    'client_email': client_email,
                    'conversation': '',
                    'cost': 0.0
                })
                break
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e):
                    retry_attempts -= 1
                    time.sleep(0.1)  # Wait briefly before retrying
                else:
                    raise e  # Re-raise if it's not a locking issue

        if id_ is None:
            raise HTTPException(status_code=500, detail="Failed to add user after multiple attempts due to database lock.")

        return {"id": id_, 'client_email': client_email}

    except HTTPException as e:
        raise e  # Re-raise the HTTPException if it's already handled
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Conversation setup endpoint remains unchanged
@router.post("/Conversation_setup/", summary="Set up a conversation", response_description="Conversation setup completed")
async def Conversation_setup(data: dict):
    """
    Sets up a conversation for a user based on client data.

    Args:
        data (dict): A dictionary containing user ID and client email.

    Returns:
        dict: A success message if the conversation is set up successfully.

    Raises:
        HTTPException: If there is an error during the database operation.
    """
    user_id = data['user_id']
    client_email = data['client']
    current_time = str(time.localtime().tm_mday) + '-' + str(time.localtime().tm_mon) + '-' + str(time.localtime().tm_year)
    try:
        client_data = Database.retrieve_records_as_dicts('Clients', client_email=client_email)[0]
        client_keywords = client_data['client_keywords']  # Retrieve client_keywords from client data

        if len(client_data['client_questions']) < 5:
            chat_template = template2.format(
                client_name=client_data['client_name'],
                client_role=client_data['client_role'],
                client_email=client_data['client_email'],
                client_phone=client_data['client_phone'],
                client_address=client_data['client_address'],
                client_information=client_data['client_information'],
                tone_of_speech=client_data['tone_of_speech'],
                current_time=current_time
            )
        else:
            chat_template = template1.format(
                client_questions=client_data['client_questions'],
                client_name=client_data['client_name'],
                client_role=client_data['client_role'],
                client_email=client_data['client_email'],
                client_phone=client_data['client_phone'],
                client_address=client_data['client_address'],
                client_information=client_data['client_information'],
                tone_of_speech=client_data['tone_of_speech'],
                current_time=current_time
            )

        # Update the Users table with the client_keywords
        Database.update_table_values('Users', {
            'client_email': client_email,
            'conversation': chat_template,
            'client_keywords': client_keywords  # Update the new field
        }, "id = {}".format(user_id))

        return {'cbot_status': 'cBot is Ready!'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
