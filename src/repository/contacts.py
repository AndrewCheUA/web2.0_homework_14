from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contact, User
from src.schemas import ContactModel


async def create_contact(body: ContactModel, user: User, db: Session):
    """
    The create_contact function creates a new contact in the database.
        Args:
            body (ContactModel): The contact to create.
            user (User): The current user, who is creating the contact.

    :param body: ContactModel: Get the data from the request body
    :param user: User: Get the user_id from the token
    :param db: Session: Access the database
    :return: The contact object
    :doc-author: Trelent
    """
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contacts(user: User, db: Session):
    """
    The get_contacts function returns a list of contacts for the user with the given id.


    :param user: User: Get the user's id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts for a given user
    :doc-author: Trelent
    """
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    return contacts


async def get_contact(contact_id: int, user: User, db: Session):
    """
    The get_contact function takes in a contact_id and user object, and returns the contact with that id.
        Args:
            contact_id (int): The id of the desired Contact.
            user (User): The User who owns the desired Contact.

    :param contact_id: int: Get a specific contact from the database
    :param user: User: Get the user from the database
    :param db: Session: Pass the database session to the function
    :return: A contact object from the database
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    return contact


async def update_contact(body: ContactModel, contact_id: int, user: User, db: Session):
    """
    The update_contact function updates a contact in the database.
        Args:
            body (ContactModel): The updated contact information.
            contact_id (int): The id of the contact to update.
            user (User): The current user, used for authorization purposes.

    :param body: ContactModel: Pass the contact information to be updated
    :param contact_id: int: Find the contact in the database
    :param user: User: Get the user_id of the logged in user
    :param db: Session: Access the database
    :return: The contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.additional_info = body.additional_info
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session):
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who is removing the contact. This is used to ensure that only contacts belonging to this
            user are deleted, and not contacts belonging to other users with similar IDs.

    :param contact_id: int: Identify the contact to be deleted
    :param user: User: Get the user id of the user who is logged in
    :param db: Session: Access the database
    :return: The contact object that was deleted
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_field(field_to_search: str, user: User, db: Session):
    """
    The search_field function searches for a field in the database and returns all contacts that contain it.
        Args:
            field_to_search (str): The string to search for.
            user (User): The user whose contacts are being searched through.

    :param field_to_search: str: Specify the field to search for
    :param user: User: Get the user's id from the database
    :param db: Session: Create a database session, which is used to query the database
    :return: A list of contacts that have the field_to_search in their name, surname or email
    :doc-author: Trelent
    """
    contacts_list = []
    contacts_all = db.query(Contact).filter(Contact.user_id == user.id).all()
    for contact in contacts_all:
        if field_to_search.capitalize() in contact.first_name.capitalize() and contact not in contacts_list:
            contacts_list.append(contact)
        if field_to_search.capitalize() in contact.last_name.capitalize() and contact not in contacts_list:
            contacts_list.append(contact)
        if field_to_search.capitalize() in contact.email.capitalize() and contact not in contacts_list:
            contacts_list.append(contact)

    return contacts_list


async def birthday_list(user: User, db: Session):
    """
    The birthday_list function takes a user and database session as arguments.
    It returns a list of contacts whose birthdays are within the next 7 days.

    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: A list of contacts with birthdays in the next week
    :doc-author: Trelent
    """
    contacts_list = []
    dt_now = datetime.now()
    now_year = datetime.now().strftime('%Y')
    contacts_all = db.query(Contact).filter(Contact.user_id == user.id).all()
    for contact in contacts_all:
        delta = contact.birthday.replace(year=int(now_year)) - dt_now
        if timedelta(days=-1) < delta < timedelta(days=7):
            contacts_list.append(contact)
    return contacts_list
