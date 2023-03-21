from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter

from src.database.connect import get_db
from src.repository import contacts as repository_contacts
from src.schemas import ContactResponse, ContactModel
from src.services.auth import auth_service
from src.database.models import User

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/birthday_search", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def birthday_list(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The birthday_list function returns a list of contacts with birthdays in the current month.
        The function takes two parameters: db and current_user.
        The db parameter is used to access the database, while the current_user parameter is used to identify which user's contact list should be returned.

    :param db: Session: Access the database
    :param current_user: User: Get the current user from the database
    :return: A list of contacts with a birthday in the next 30 days
    :doc-author: Trelent
    """
    contacts = await repository_contacts.birthday_list(current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts


@router.get("/search_field{field_to_search}", response_model=List[ContactResponse],
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def search_field(part_to_search: str, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The search_field function searches for a contact in the database.
        It takes a string as an argument and returns all contacts that contain this string in any of their fields.
        If no such contacts are found, it raises an HTTPException with status code 404.

    :param part_to_search: str: Specify the part of the field to search for
    :param db: Session: Get the database session
    :param current_user: User: Get the user_id of the logged in user
    :return: A list of contacts that contain the string in any field
    :doc-author: Trelent
    """
    contacts = await repository_contacts.search_field(part_to_search, current_user, db)
    if len(contacts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts


@router.get("/all", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts for the current user.

    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the auth_service
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts


@router.post("/create", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
        The function takes a ContactModel object as input, which is validated by pydantic.
        The function also takes an optional db Session object and current_user User object as inputs,
        both of which are provided by dependency injection via FastAPI's Depends decorator.

    :param body: ContactModel: Pass the contact data in a json format
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the current user from the database
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contacts.create_contact(body, current_user, db)
    return contact


@router.get("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact(contact_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function is used to retrieve a single contact from the database.
    It takes in an integer representing the ID of the contact, and returns a Contact object.

    :param contact_id: int: Specify the contact_id that is passed in the url
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: A contact based on the given id
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.put("/update/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes three arguments:
            body: A ContactModel object containing the new values for the contact.
            contact_id: An integer representing the id of an existing contact to be updated.
            db (optional): A Session object used to connect to and query a database, defaults to None if not provided.

    :param body: ContactModel: Get the contact data from the request body
    :param contact_id: int: Specify the id of the contact to delete
    :param db: Session: Get a database session
    :param current_user: User: Get the current user
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(body, contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/delete/{contact_id}", status_code=status.HTTP_204_NO_CONTENT,
               description='No more than 10 requests per minute',
               dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.
        The function takes in an integer representing the id of the contact to be removed,
        and returns a dictionary containing information about that contact.

    :param contact_id: int: Specify the id of the contact to be removed
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
