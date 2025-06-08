from __future__ import annotations
from typing import Optional, Protocol


class ContactList(list["Contact"]):
    def search(self, name: str) -> list["Contact"]:
        # ---All Contacts with name that contains the name paramater's value---
        matching_contacts: list["Contact"] = []
        for contact in self:
            if name in contact.name:
                matching_contacts.append(contact)
        return matching_contacts


class Contact:
    all_contacts: ContactList = ContactList()

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email
        Contact.all_contacts.append(self)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{self.name!r}, {self.email!r}"
            f")"
        )


class Suplier(Contact):
    def order(self, order: "Order") -> None:
        print(
            "If this were a real system we would send"
            f"'{order} order to '{self.name}'"
        )


class AddressHolder:
    def __init__(self, street: str, city: str, state: str, code: str) -> None:
        self.street = street
        self.city = city
        self.state = state
        self.code = code


class Friend(Contact, AddressHolder):
    def __init__(
            self,
            name: str,
            email: str,
            phone: str,
            street: str,
            city: str,
            state: str,
            code: str,
    ) -> None:
        Contact.__init__(self, name, email)
        AddressHolder.__init__(self, street, state, city, code)
        self.phone = phone


class Emailable(Protocol):
    email: str


class MailSender(Emailable):
    def send_mail(self, message: str) -> None:
        print(f"Sending mail to {self.email=}")


class EmailableContact(Contact, MailSender):
    pass


class Nameable(Protocol):
    name: str


class NameSender(Emailable):
    def send_name(self, message: str) -> None:
        print(f"Sending name to {self.email=}")


class NameableContact(Contact, NameSender):
    pass

# c = Contact("Alice", "alice@gmail")
# c_2 = Contact("Sansha", "Sasha@gmail")
# c_3 = Contact("Danya", "dany@gmail")
# res = Contact.search("dadaya")
# print(res)
