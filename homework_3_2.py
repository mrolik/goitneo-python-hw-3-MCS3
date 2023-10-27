from classes import AddressBook, Record, CustomPhoneException,\
    CustomBirthdayException


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Give me name please."
        except KeyError:
            return "Contact not found."
        except CustomPhoneException:
            return "Invalid phone number."
        except CustomBirthdayException:
            return "Invalid birthday date."

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    contact = book.find(name)
    if contact:
        contact.add_phone(phone)
        return "Phone added"
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    if not book.find(name):
        return "Contact not found."
    else:
        contact = book.find(name)
        contact.edit_phone(old_phone, new_phone)
        return "Contact changed."


@input_error
def get_contact(args, book: AddressBook):
    contact = book.find(args[0])
    if contact:
        return contact
    else:
        return "Contact not found."


@input_error
def get_all(book: AddressBook):
    contacts_list = []
    if not book.data:
        return "Contact list is empty"
    for name, record in book.data.items():
        contacts_list.append(f"{name} : {record}\n")
    return "".join(contacts_list)


@input_error
def add_birthday(args, book: AddressBook):
    name = args[0]
    birthday = args[1]
    contact = book.find(name)
    if contact:
        contact.add_birthday(birthday)
        return "Birthday added"
    else:
        return "Contact not found"


@input_error
def show_birthday(args, book: AddressBook):
    contact = book.find(args[0])
    if contact and contact.birthday:
        return contact.birthday.value
    else:
        return "Birthday not found."


@input_error
def birthdays(book: AddressBook):
    return book.get_birthdays_per_week()


def main():
    """main function of the project"""
    book: AddressBook = AddressBook()
    book.load()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            book.save()
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(get_contact(args, book))
        elif command == "all":
            print(get_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()