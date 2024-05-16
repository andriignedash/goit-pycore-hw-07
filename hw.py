
from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_date = record.birthday.value
                try:
                    birthday_this_year = datetime(birthday_date.year, birthday_date.month, birthday_date.day).date()
                    birthday_this_year = birthday_this_year.replace(year=today.year)
                except ValueError:
                    if birthday_date.month == 2 and birthday_date.day == 29:
                        birthday_this_year = datetime(today.year, 2, 28).date() 
                    else:
                        continue
                print("Checking birthday:", birthday_this_year, "Today:", today, "Next week:", next_week)
                if today <= birthday_this_year <= next_week:
                    upcoming_birthdays.append(record.name.value)

        return upcoming_birthdays
    
def input_error(func):
    def wrapper(args, book):
        try:
            return func(args, book)
        except Exception as e:
            return str(e)
    return wrapper

@input_error
def add_contact(args, book):
    if len(args) < 2:
        return "Not enough arguments. Usage: add [name] [phone]"
    name, phone = args
    record = book.data.get(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return "Contact added."

@input_error
def change_phone(args, book):
    if len(args) < 3:
        return "Not enough arguments. Usage: change [name] [old phone] [new phone]"
    name, old_phone, new_phone = args
    record = book.data.get(name)
    if not record:
        return "Contact not found"
    if not any(phone.value == old_phone for phone in record.phones):
        return "Old phone number not found"
    for phone in record.phones:
        if phone.value == old_phone:
            phone.value = new_phone
            return "Updated successfully."
        
@input_error
def add_birthday(args, book):
    if len(args) < 2:
        return "Not enough arguments. Usage: add-birthday [name] [date]"
    name, date = args
    record = book.data.get(name)
    if not record:
        return "Contact not found"
    record.add_birthday(date)
    return "Birthday added." 

def show_birthday(args, book):
    if len(args) < 1:
        return "Not enough arguments. Usage: show-birthday [name]"
    name = args[0]
    record = book.data.get(name)
    if not record:
        return "Contact not found"
    if record.birthday:
        return f"Birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
    else:
        return "Birthday not set"

def show_all_contacts(book):
    if not book:
        return "No contacts found"
    result = ""
    for name, record in book.items():
        phones = ', '.join(phone.value for phone in record.phones)
        birthday = record.birthday.value.strftime('%d.%m.%Y') if record.birthday else "No birthday set"
        result += f"Contact name: {name}, phones: {phones}, Birthday: {birthday}\n"
    return result.strip()

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.strip().split()
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_phone(args, book))
        elif command == "phone":
            contact = book.data.get(args[0])
            if contact:
                phones = ', '.join(phone.value for phone in contact.phones)
                print(f"Phone numbers: {phones}")
            else:
                print("Contact not found")
        elif command == "all":
            print(show_all_contacts(book))
        elif command == "add-birthday":
            response = add_birthday(args, book)
            print(response)
        elif command == "show-birthday":
            response = show_birthday(args, book)
            print(response)
        elif command == 'birthdays':
            birthdays = book.get_upcoming_birthdays()
            if birthdays:
                print("Upcoming birthdays next week:")
                for name in birthdays:
                    print(name)
            else:
                print("No upcoming birthdays.")
        else:
            print("Invalid command.")


if __name__ == '__main__':
    main()
