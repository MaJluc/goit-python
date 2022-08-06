import re

correct_phone = "(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
contacts = {'1':'q', 'qw':'36789'}
STOP = ['good bye', 'close', 'exit']


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return e
        except ValueError as e: 
            return e
        except NameError:
            return 'Name empty in contacts'
            
    return inner


def validate(correct, value):
    return re.search(correct, str(value))


def unknown_func():
    raise KeyError('Enter a valid request')


def hello_func():    
   return "How can I help you?"


def add_funk(name, phone):
    if name in contacts:
        raise ValueError('This contact already exists')
    else:
        contacts[name] = phone
        
        return f'{name} {phone}'


def change_func(name, phone):
    if name in contacts:
        contacts[name] = phone
        
        return f'{name} {phone}'
        
    else:
        raise NameError


def phone_func(name):
    if name in contacts:
    
       return contacts[name]
       
    else:
        raise NameError


def show_all_func():
    list = []
    for key, value in contacts.items():
        list.append(f'{key} {value}')
        
    return '\n'.join(list)


OPERATIONS = {
    'hello': hello_func,
    'add': add_funk,
    'change': change_func,
    'phone': phone_func,
    'show all': show_all_func,
    'unknown': unknown_func
}


def parser(user_input):
    if user_input.startswith('hello'):
        command = 'hello'
    elif user_input.startswith('show all'):
        command = 'show all'
    elif (user_input.startswith('add') or user_input.startswith('change')) and len(user_input.split(' ')) == 3:
        command = user_input.split(' ')[0]
    elif user_input.startswith('phone') and len(user_input.split(' ')) == 2:
        command = 'phone'
    else:
        command = 'unknown'

    return command


@input_error
def get_handler(command, user_input):
    if command in ['hello', 'show all', 'unknown']:
    
        return OPERATIONS[command]()
        
    elif command in ['add', 'change']:
        name = user_input.split(' ')[1]
        phone = user_input.split(' ')[2]
        if not validate(correct_phone, phone):
            raise ValueError('Phone namber is not correct')
            
        return OPERATIONS[command](name, phone)
        
    elif command == 'phone':
        name = user_input.split(' ')[1]
        
        return OPERATIONS[command](name)
        

def main():
    while True:
        user_input = input('').lower()
        if user_input in STOP:
            print('Good bye!')
            break
        else:
            result = get_handler(parser(user_input), user_input)
            print(result)
        
if __name__ == "__main__":
    main()

