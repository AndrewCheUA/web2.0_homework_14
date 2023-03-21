import unittest
from unittest.mock import MagicMock
from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
    search_field,
    birthday_list,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.contact = ContactModel(
            first_name='Contact',
            last_name='Test',
            email='contact@gmail.com',
            phone='0952589654',
            birthday=date(1987, 5, 29),
            additional_info='test info',
        )

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter_by().return_value.first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = self.contact
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact_id = 1
        contact = Contact(id=contact_id)
        self.session.query(Contact).filter_by().first.return_value = contact
        result = await remove_contact(contact_id, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query(Contact).filter().first.return_value = None
        self.session.commit.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        print(result)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = self.contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_note_not_found(self):
        body = self.contact
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_search_field_found(self):
        contact1 = Contact(
            first_name='User1',
            last_name='Test1',
            email='testmail1@gmail.com',
            phone='0953214569'
        )
        contact2 = Contact(
            first_name='User2',
            last_name='Test2',
            email='testmail2@gmail.com',
            phone='0953214568'
        )
        contact3 = Contact(
            first_name='User3',
            last_name='Test3',
            email='testmail3@gmail.com',
            phone='0953214567'
        )
        self.session.query().filter().all.return_value = [contact1, contact2, contact3]

        results = await search_field('Test2', user=self.user, db=self.session)

        assert contact1 not in results
        assert contact2 in results
        assert contact3 not in results

    async def test_birthday_list_found(self):
        contacts = [Contact(birthday=datetime.now() + timedelta(days=1)),
                    Contact(birthday=datetime.now() + timedelta(days=2)),
                    Contact(birthday=datetime.now() + timedelta(days=3)),
                    Contact(birthday=datetime.now() + timedelta(days=4)),
                    Contact(birthday=datetime.now() + timedelta(days=5)),
                    Contact(birthday=datetime.now() + timedelta(days=6)),
                    Contact(birthday=datetime.now() + timedelta(days=7)),
                    Contact(birthday=datetime.now() + timedelta(days=8)),
                    Contact(birthday=datetime.now() + timedelta(days=9)),
                    Contact(birthday=datetime.now() + timedelta(days=10)),
                    ]
        self.session.query().filter().all.return_value = contacts
        result = await birthday_list(user=self.user, db=self.session)
        self.assertEqual(result, contacts[0:7])

if __name__ == '__main__':
    unittest.main()
