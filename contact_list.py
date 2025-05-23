import json
import os
from typing import List, Dict

class Contact:
    def __init__(self, name: str, phone: str, email: str = ""):
        self.name = name.title()
        self.phone = phone
        self.email = email

    def to_dict(self) -> Dict:
        return {"name": self.name, "phone": self.phone, "email": self.email}

    @staticmethod
    def from_dict(data: Dict):
        return Contact(data['name'], data['phone'], data.get('email', ''))


class ContactManager:
    def __init__(self, file_path='contacts.json'):
        self.file_path = file_path
        self.contacts: List[Contact] = self.load_contacts()

    def load_contacts(self) -> List[Contact]:
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            return [Contact.from_dict(item) for item in data]

    def save_contacts(self):
        with open(self.file_path, 'w') as f:
            json.dump([c.to_dict() for c in self.contacts], f, indent=4)

    def add_contact(self, contact: Contact):
        if any(c.phone == contact.phone for c in self.contacts):
            print("Contact with this phone number already exists.")
            return
        self.contacts.append(contact)
        self.save_contacts()
        print(f"Contact {contact.name} added successfully.")

    def list_contacts(self):
        if not self.contacts:
            print("No contacts found.")
        for i, contact in enumerate(self.contacts, start=1):
            print(f"{i}. {contact.name} - {contact.phone} - {contact.email}")

    def find_contact(self, name: str) -> List[Contact]:
        return [c for c in self.contacts if name.lower() in c.name.lower()]

    def update_contact(self, phone: str, new_data: Dict):
        for contact in self.contacts:
            if contact.phone == phone:
                contact.name = new_data.get('name', contact.name).title()
                contact.phone = new_data.get('phone', contact.phone)
                contact.email = new_data.get('email', contact.email)
                self.save_contacts()
                print("Contact updated successfully.")
                return
        print("Contact not found.")

    def delete_contact(self, phone: str):
        for i, contact in enumerate(self.contacts):
            if contact.phone == phone:
                del self.contacts[i]
                self.save_contacts()
                print("Contact deleted successfully.")
                return
        print("Contact not found.")


def main():
    manager = ContactManager()

    while True:
        print("\n--- Contact List Menu ---")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            name = input("Name: ")
            phone = input("Phone: ")
            email = input("Email (optional): ")
            manager.add_contact(Contact(name, phone, email))
        elif choice == '2':
            manager.list_contacts()
        elif choice == '3':
            name = input("Enter name to search: ")
            results = manager.find_contact(name)
            if results:
                for c in results:
                    print(f"{c.name} - {c.phone} - {c.email}")
            else:
                print("No contacts found.")
        elif choice == '4':
            phone = input("Enter phone of the contact to update: ")
            new_name = input("New Name (leave blank to keep current): ")
            new_phone = input("New Phone (leave blank to keep current): ")
            new_email = input("New Email (leave blank to keep current): ")
            update_data = {k: v for k, v in {
                "name": new_name, "phone": new_phone, "email": new_email
            }.items() if v}
            manager.update_contact(phone, update_data)
        elif choice == '5':
            phone = input("Enter phone number of contact to delete: ")
            manager.delete_contact(phone)
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
