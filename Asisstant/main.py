import os
import re
import sys
from datetime import timedelta, datetime


def file_error(func):
    def inner(*args):
        if os.path.isfile('data//data-file.txt') and os.path.getsize('data//data-file.txt') > 0:
            return func(*args)
        else:
            print('Книга контактів порожня. Добавте інформацію')
        
    return inner


class Asisstant: 
    def __init__(self):
        self.user_name = ''
        self.user_phone = ''
        self.user_location = ''
        self.user_email = ''
        self.user_birthday = ''
        self.user_note = ''
        self.user_tag = ''
        self.data = []
        print('Привіт! Введи \'help\' для виводу меню екран.')


    def command(self):
        command = input('Зроби свій вибір: ').strip().casefold()
        if command == 'add':
            consumer.add()
        elif command == 'search':
            consumer.search()
        elif command == 'delete':
            consumer.delete()
        elif command == 'edit':
            consumer.edit()
        elif command == 'show':
            consumer.show()
        elif command == 'birthday':
            consumer.day_to_birthday()
        elif command == 'help':
            consumer.help()
        elif command == 'exit':
            consumer.exit()
        else:
            print(f'Команди "{command}" не існує. Будь ласка, спробуй ще раз')


    def help(self):
        print('Я твій помічник, ось, що я вмію:')
        print('<add>   - зберігати контакти з іменами, номерами телефонів, адресами електронної пошти, їх локацію та дні народження в книзі контактів;')
        print('<birthday> - відобразити список контактів, у яких день народження після вказаної кількості днів від поточної дати;')
        print('<search>   - пошук інформації по всій книзі контактів;')
        print('<edit>     - редагувати та видаляти інформацію з контактної книги;')
        print('<delete>   - видалити контакт з книги контактів;')
        print('<show>     - відобразити весь вміст контактної книги;') 
        print('<exit>     - вихід з програми')

        
    def edit_name(self, record):
        self.user_name = self.name_input().strip()
        record['name'] = self.user_name
        return record


    def edit_phone(self, record):
        while True:
            command_edit_phone = input('Змінити("change") чи додати("add") телефон?:  ').strip().casefold()
            if command_edit_phone not in ('change', 'add'):
                print(f'Команди "{com_edit_note}" не існує. Будь ласка, спробуй ще раз')
            else:
                break
        self.user_phone = self.phone_input().strip()
        if command_edit_phone == 'change':
            record['phone'] = self.user_phone
            return record
        elif command_edit_phone == 'add':
            record['phone'] = record['phone'] + ' ' + self.user_phone
            return record
        else:
            print(f'Команди "{com_edit_phone}" не існує. Будь ласка, спробуй ще раз')

            
    def edit_location(self, record):
        self.user_location = self.location_input().strip()
        record['location'] = self.user_location
        return record


    def edit_email(self, record):
        self.user_email = self.email_input().strip()
        record['email'] = self.user_email
        return record


    def edit_birthday(self, record):
        self.user_birthday = self.birthday_input().strip()
        record['birthday'] = self.user_birthday
        return record


    def edit_note(self, record):
        while True:
            command_edit_note = input('Змінити("change"), додати("add") чи видалити("delete") нотатки?:  ').strip().casefold()
            if command_edit_note not in ('change', 'add', 'delete'):
                print(f'Команди "{command_edit_note}" не існує. Будь ласка, спробуй ще раз')
            else:
                break
        if command_edit_note == 'delete':
            record['note'] = ''
            return record
        self.user_note = self.add_note().strip()
        if command_edit_note == 'change':
            record['note'] = self.user_note
            return record
        elif command_edit_note == 'add':
            record['note'] = record['note'] + ', ' + self.user_note
            return record
        else:
            print(f'Команди "{command_edit_note}" не існує. Будь ласка, спробуй ще раз')

    def edit_tag(self, record):
        while True:
            command_edit_tag = input('Змінити("change"), додати("add") чи видалити("delete") тег?:  ').strip().casefold()
            if command_edit_tag not in ('change', 'add', 'delete'):
                print(f'Команди "{command_edit_tag}" не існує. Будь ласка, спробуй ще раз')
            else:
                break
        if command_edit_tag == 'delete':
            record['tag'] = '\n'
            return record
        self.user_tag = self.add_tag().strip()
        if command_edit_tag == 'change':
            record['tag'] = self.user_tag + '\n'
            return record
        elif command_edit_tag == 'add':
            record['tag'] = record['tag'].replace('\n', ' ') + self.user_tag + '\n'
            return record
        else:
            print(f'Команди "{command_edit_tag}" не існує. Будь ласка, спробуй ще раз')
    

    EDITOR = {'name': edit_name,
              'phone': edit_phone,
              'location': edit_location,
              'email': edit_email,
              'birthday': edit_birthday,
              'note': edit_note,
              'tag': edit_tag}


    def get_editor_handler(self, com_edit):

        return self.EDITOR[com_edit]


    def deserialization_data(self):
        with open('data//data-file.txt', 'r') as file:
            self.data = []
            keys = ['name', 'phone', 'location', 'email', 'birthday', 'note', 'tag']
            for row in file:
                record = {}
                row = row.split('| ')
                for key, value in zip(keys, row):
                    record[key] = value
                self.data.append(record)


    def serialization_data(self):
        with open('data//data-file.txt', 'w') as file:
            for record in self.data:
                file.write('| '.join(record.values()))


    @file_error
    def edit(self):
        self.deserialization_data()
        while True:
            self.user_name = input('Введіть ім\'я для редагування даних:  ').strip()
            if any(record['name'].strip().casefold() == self.user_name.casefold() for record in self.data):
                break
            else:
                print(f'Ім\'я "{self.user_name}" відсутнє в книзі контактів.')
        for record in self.data:
            if record['name'].strip().casefold() == self.user_name.casefold():
                while True:
                    command_edit = input('Що будемо редагувати?\n ім\'я("name"), телефон("phone"), локацію("location"), пошту("email"), Д.Н.("birthday"), нотатки("note"),теги("tag")\nЗробіть вибір:  ').strip().casefold()
                    try:
                        updated_record = self.get_editor_handler(command_edit)(self, record)
                        self.data[self.data.index(record)] = updated_record
                        print(f'Контактні дані "{record["name"]}" оновлені.')
                        break
                    except KeyError:
                        print(f'Невірно, спробуй ще раз.')

        self.serialization_data()

    @file_error
    def delete(self):
        self.deserialization_data()
        self.user_name = input('Введіть ім\'я для видалення даних: ').strip()
        if not any(record['name'].strip().casefold() == self.user_name.casefold() for record in self.data):
            print(f'Ім\'я "{self.user_name}" відсутнє в книзі контактів.')
        for record in self.data:
            if record['name'].strip().casefold() == self.user_name.casefold():
                self.data.remove(record)
                print(f'Контакт з ім\'ям "{record["name"]}" було видалено.')
        self.serialization_data()


    def name_input(self):
        with open('data//data-file.txt', 'r') as file:
            users = file.readlines()
            while True:
                try:
                    self.user_name = input('Введіть ім\'я: ')
                    if not any(re.split('\| ', user)[0].strip().casefold() == self.user_name.casefold() for user in users):
                        return self.user_name
                    else:
                        print('Це ім\'я вже є в книзі контактів!')
                except AttributeError:
                    print('Будь ласка, спробуй ще раз.')


    def phone_input(self):
        while True:
            try:
                self.user_phone = input('Введіть номер телефону: ')
                if self.user_phone == (re.search(r'\+?\d?\d?\d?\d{2}\d{7}', self.user_phone)).group():
                    return self.user_phone
                else:
                    print('Невірно набраний номер, спробуй ще раз.')
            except AttributeError:
                print('Невірно, спробуй ще раз.')


    def location_input(self):
        self.user_location = input('Додайте локацію, або натисніть "Enter", щоб продовжити: ')
        return self.user_location

                
    def email_input(self):
        while True:
            try:
                self.user_email = input('Додайте електронну пошту, або натисніть "Enter", щоб продовжити: ')
                if len(self.user_email) == 0:
                    return self.user_email
                if self.user_email == (re.search(r'[a-zA-Z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}', self.user_email)).group():
                    return self.user_email
                else:
                    print('Невірно, спробуй ще раз.')
            except AttributeError:
                print('Невірно, спробуй ще раз.')


    def birthday_input(self):
        while True:
            try:
                self.user_birthday = input('Введіть день народження в форматі DD.MM.YYYY: ')
                if datetime.now().date() > datetime.strptime(self.user_birthday, '%d.%m.%Y').date():
                    break
                else:
                    print("Невірно, спробуй ще раз.")
            except ValueError:
                print("Невірно, спробуй ще раз.")
        return self.user_birthday


    def add_note(self):
        self.user_note = input('Додайте нотатки, або натисніть "Enter", щоб продовжити: ')
        return self.user_note


    def add_tag(self):
        self.user_tag = '#' + input('Додайте тег, або натисніть "Enter", щоб продовжити: ')
        return self.user_tag


    def combine_data(self):
        combine_data = consumer.name_input() + '| ' + consumer.phone_input() + '| ' + consumer.location_input() + '| ' +  consumer.email_input() + '| '\
                +  consumer.birthday_input() + '| ' + consumer.add_note() + '| ' + consumer.add_tag() + '\n'
        return combine_data
    

    def add(self):
        with open('data//data-file.txt', 'a') as file:
            file.write(str(consumer.combine_data()))

        
    def exit(self):
        print("На все добре!")
        sys.exit(0)  

    def print_users(self, users):
        print('-'*152)   
        header = "| {:^2} | {:^10} | {:^22} | {:^28} | {:^15} | {:^15} | {:^20} | {:^15} |".format('№', 'ім\'я', 'телефон', 'місце знаходження','пошта', 'день народження', 'нотатки', 'теги') 
        print(header)
        print('-'*152)    
        for user in enumerate(users):
            count = user[0]+1
            name = re.split(r'\|',user[1])[0].strip()
            phone = re.split(r'\|',user[1])[1].strip()
            location = re.split(r'\|',user[1])[2].strip()
            e_mail = re.split(r'\|',user[1])[3].strip()
            birthday = re.split(r'\|',user[1])[4].strip()
            note = re.split(r'\|',user[1])[5].strip()
            tag = re.split(r'\|',user[1])[6].strip()
            user_data = "| {:^2} | {:<10} | {:<22} | {:<28} | {:15} | {:<15} | {:<20} | {:<15} |".format(count, name, phone, location, e_mail, birthday, note, tag) 
            print(user_data)
        print('-'*152)


    @file_error
    def day_to_birthday(self):
        while True:
            try:
                n = input('Будь ласка, введіть кількість днів до дня народження: ')
                if n.isdigit:
                    break
            except ValueError:
                print('Введіть дійсний номер.')
        user_list = []
        user_date = datetime.now() + timedelta(days = int(n))
        search_pattern = datetime.strftime(user_date, '%d.%m')
        with open('data//data-file.txt', 'r') as file:
            users = file.readlines()
            for user in users:
                if re.search(search_pattern, re.split(r'\|',user)[4].strip()):
                    user_list.append(user) 
        if len(user_list)>0:
            print(f'В цей день свій день народження святкує:\n')
            self.print_users(user_list)
        else:
            print('В цей день ніхто не святкує дня народження!')


    @file_error
    def search(self):
        while True:
            key_word = input('Будь ласка, введіть ключове слово: ')
            if len(key_word) > 2:
                break
            else:
                print('Замало даних для пошуку. Введіть не менше 3 символів')
        user_list = []
        with open('data//data-file.txt', 'r') as file:
            users = file.readlines()
            for user in users:
                if key_word.lower() in user.lower():
                    user_list.append(user)
        if len(user_list)>0:
            print(f'Результати пошуку за ключовим словом "{key_word}":\n')
            self.print_users(user_list)
        else:
            print('Немає збігів!')


    @file_error
    def show(self):
        with open('data//data-file.txt', 'r') as file:
            users = file.readlines() 
            self.print_users(users)


consumer = Asisstant()


def main():
    
    while True:
        try:
            os.mkdir('data')
        except FileExistsError:
            pass
        consumer.command()

    
if __name__ == '__main__':
    main()
