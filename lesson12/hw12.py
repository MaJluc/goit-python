import re
import inspect
import pathlib
import signal
import sys
from collections import UserDict
from datetime import date
import pickle
import re


class AddressBook(UserDict):
    def add_record(self, name, record):
        self.data[name] = record

    def iterator(self, n=None):

        outer_count = 1
        inner_count = 1
        n_records = []
        records = (i for i in self.data.values())
        for one_record in records:
            n_records.append(one_record)
            if inner_count == n or outer_count == len(self.data):
                yield n_records
                n_records = []
                inner_count = 0
            inner_count += 1
            outer_count += 1

    def save_dumped_data(self):
        with open('contact_list.txt', 'wb') as file:
            pickle.dump(self.data, file)

    def read_dumped_data(self):
        with open('contact_list.txt', 'rb') as file:
            self.data = pickle.load(file)
            return self


class Record:
    def __init__(self, name, birthday=None):
        self.name = name
        self.phones = []
        self.birthday = birthday

    def __add__(self, phone):
        self.phones.append(phone)
        return self

    def __sub__(self, phone):
        self.phones.remove(phone)
        return self

    def change_phone(self, phone, new_phone):
        self.phones[self.phones.index(phone)] = new_phone

    def days_to_birthday(self):
        if self.birthday:
            if self.birthday.value.replace(date.today().year) > date.today():
                quantity_day = self.birthday.value.replace(date.today().year) - date.today()
            else:
                quantity_day = self.birthday.value.replace(
                    date.today().year + 1) - date.today()
            return quantity_day.days
        else:
            return ''


class Field:

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    def __init__(self, name):
        self.value = name


class Phone(Field):
    def __init__(self, phone):
        self.value = phone

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_phone):
        REG_PHONE = '(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{3}[-\.\s]??\d{2}[-\.\s]??\d{2}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{2}[-\.\s]??\d{2})'
        if not re.search(REG_PHONE, str(new_phone)):
            raise ValueError(f'This phone number "{new_phone}" is not correct. Please enter a 10 or 12 digit phone number.\n')
        else:
            self.__value = new_phone

class Birthday(Field):
    # imput format: 'YYYY-MM-DD'
    def __init__(self, date_birth):
        self.value = date_birth

    @property
    def value(self):
        return date.fromisoformat(self.__value)

    @value.setter
    def value(self, new_date_birth):
        REG_DATE = r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'
        if not re.search(REG_DATE, str(new_date_birth)):
            raise ValueError(f'Please enter your birthday in the format: "YYYY-MM-DD".\n')
        else:
            self.__value = new_date_birth



def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return f'Command {e} not found!!!'
        except ValueError as e:
            return e
        except IndexError as e:
            return f'Command not full!!'
    return inner

def processing_com_add(name, phone, birthday=None):
    if name.value in [key.value for key in list(contact_list.keys())]:
        raise ValueError(f'The new contact cannot be saved because the name "{name.value}" already exists. '
                         f'Please enter a different name.\n')
    record = Record(name, birthday) + phone
    contact_list.add_record(name, record)
    return f'New contact is saved: name "{name.value}", phone "{phone.value}", date of birth ' \
           f'"{birthday.value if birthday else "-"}".\n'


def processes_com_change(name, phone, new_phone):
    if not name in [key.value for key in list(contact_list.keys())]:
        raise ValueError(f'Сontact by name "{name}" does not exist. Enter the correct name.\n')
    for nam, rec in contact_list.items():
        if nam.value == name:
            for ph in rec.phones:
                if ph.value == phone:
                    rec.change_phone(ph, new_phone)
                    return f'Saved a new phone number "{new_phone.value}" for a contact with the name "{name}".\n'
                else:
                    raise ValueError(f'The contact "{name}" does not have a phone number {phone}.\n')


def processing_com_exit():
    return 'Good bye!\n'


def processing_com_hello():
    return 'How can I help you?\n'


def processing_com_join(name, phone):
    if not name in [key.value for key in list(contact_list.keys())]:
        raise ValueError(f'Сontact with name "{name}" does not exist. Enter the correct name.\n')
    for nam, rec in contact_list.items():
        if nam.value == name:
            record = rec + phone
            contact_list.add_record(nam, record)
    return f'A new phone number "{phone.value}" has been added for the contact with the name "{name}".\n'


def processes_com_phone(name):
    for nam, rec in contact_list.items():
        if nam.value == name:
            return ' '.join([phone.value for phone in rec.phones])
    raise ValueError(f'Contact with the name "{name}" does not exist.\n')


def processes_com_show_all():
    return contact_list.iterator()


def processes_com_search(pattern):
    result = ''
    for nam, rec in contact_list.items():
        phone_list = [phone.value for phone in rec.phones]
        for p in phone_list:
            if p.find(pattern) != (-1) or nam.value.find(pattern) != (-1):
                result += f'name: {nam.value}, phone: {" ".join([phone.value for phone in rec.phones])}, ' \
                          f'birtday: {rec.birthday.value if rec.birthday else "-"} ' \
                          f'{"("+str(rec.days_to_birthday())+" days)" if rec.days_to_birthday() else ""}\n'
    if not result:
        raise ValueError(f'No matches.\n')
    return result


@ input_error
def get_command_handler(user_input):
    if user_input[:2] == ['show', 'all']:
        return processes_com_show_all()
    elif user_input[:2] == ['good', 'bye'] or user_input[0] in ('close', 'exit'):
        return processing_com_exit()
    elif user_input[0] == 'search':
        return processes_com_search(user_input[1])
    elif user_input[0] == 'hello':
        return processing_com_hello()
    elif user_input[0] == 'phone':
        return processes_com_phone(user_input[1])
    elif user_input[0] == 'join':
        return processing_com_join(user_input[1], Phone(user_input[2]))
    elif user_input[0] == 'add':
        birthday = Birthday(user_input[3]) if len(user_input) > 3 else None
        return processing_com_add(Name(user_input[1]), Phone(user_input[2]), birthday)
    elif user_input[0] == 'change':
        return processes_com_change(user_input[1], user_input[2], Phone(user_input[3]))
    else:
        raise KeyError(user_input[0])


def signal_handler(signal, frame):
    contact_list.save_dumped_data()
    sys.exit(0)


contact_list = AddressBook()


if __name__ == '__main__':
    print('''Command:
<hello> - greeting;
<add_name_phone_birthday> - add a new contact (“birthday”(YYYY-MM-DD") - it is not necessary to indicate it);
<join_name_phone> - add a new phone to an existing contact;
<phone_name> - displays phone numbers by contact name;
<show_all> - displays all contents of the contact book, incl. number of days until the next birthday 
             (if there is data in the book about the date of birth)
<search> - displays a list of users whose name or phone number matches the entered string;
<good_bye>, <close>, <exit> - end of the program.''')
    path = pathlib.Path('contact_list.txt')

    if path.exists() and path.stat().st_size > 0:
        contact_list = contact_list.read_dumped_data()

    while True:
        user_input = input('Enter command: ').lower().split()
        result = get_command_handler(user_input)
        if result == 'Good bye!\n':
            print(result)
            break
        elif inspect.isgenerator(result):
            for n in result:
                for rec in n:
                    print(f'name: {rec.name.value}; phone: {", ".join([phone.value for phone in rec.phones])}; '
                          f'birthday {rec.birthday.value if rec.birthday else "-"} '
                          f'{"("+str(rec.days_to_birthday())+" days)" if rec.days_to_birthday() else ""}. ')
        else:
            print(result)
            signal.signal(signal.SIGINT, signal_handler)

    serialized_list = contact_list.save_dumped_data()
