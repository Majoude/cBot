# Importing necessary libraries
from fastapi import APIRouter, HTTPException
from database import Database

router = APIRouter()

@router.post("/add_client/", summary="Add a new client", response_description="Client added successfully")
async def create_client(data: dict):
    """
    Adds a new client record to the 'Clients' table.

    Args:
        data (dict): A dictionary containing client information.

    Returns:
        dict: A success message if the record is added successfully.

    Raises:
        HTTPException: If there is an error during the database operation.
    """
    client_email = data['clientEmail']
    client_name = data['clientName']
    client_role = data['clientRole']
    client_phone = data['phone']
    client_address = data['address']
    client_information = data['info']
    tone_of_speech = data['toneOfSpeech']
    client_questions = data['que']
    client_keywords = data.get('clientKeywords', '')  # New field

    
    try:
        # Check if the client email already exists
        existing_client = Database.retrieve_records_as_dicts('Clients', client_email=client_email)
        if existing_client:
            raise HTTPException(status_code=400, detail="Client email already exists.")
        
        # If the email doesn't exist, insert the new client
        Database.insert_record('Clients', {
            'client_email': client_email,
            'client_name': client_name,
            'client_role': client_role,
            'client_phone': client_phone,
            'client_address': client_address,
            'client_information': client_information,
            'tone_of_speech': tone_of_speech,
            'client_questions': client_questions,
            'client_keywords': client_keywords  # Include the new field

        })

        return {"message": "Record added successfully"}
    
    except HTTPException as e:
        raise e  # Re-raise the HTTPException if it's already handled
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
