# Importing necessary libraries

from fastapi import APIRouter, HTTPException
from database import Database
from models import Static

router = APIRouter()

@router.get("/clear/", summary="Clear data from a table", response_description="Table data cleared successfully")
async def clear(table_name: str):
    """
    Clears all data from the specified table.

    Args:
        table_name (str): The name of the table to be cleared.

    Returns:
        dict: A success message if the data is cleared successfully.

    Raises:
        HTTPException: If there is an error during the database operation.
    """
    try:
        Database.delete_all_data_from_table(table_name)
        return {'cbot_msg': 'data has been cleared!'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/set_report_fields/", summary="Set report fields", response_description="Fields set successfully")
async def set_report_fields(fields: str):
    """
    Sets the report fields for the cBot.

    Args:
        fields (str): A comma-separated string of field names.

    Returns:
        dict: A success message if the fields are set successfully.

    Raises:
        HTTPException: If there is an error during the database operation.
    """
    try:
        Static.requirments = fields.split(',')
        return {"message": "Done"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

