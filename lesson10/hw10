from collections import UserDict


class AddressBook(UserDict):
    
    def add_record(self, record):
        self.data[record.name.value] = record

class Record:

    def __init__(self, name):
        self.name = name
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, phone_old, phone_new):
        self.remove_phone(phone_old)
        self.phones.append(phone_new)

class Field:
    pass

class Name(Field):

    def __init__(self, name):
        self.value = name

class Phone(Field):
    
    def __init__(self, phone):
        self.phone = phone
