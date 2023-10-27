import pickle
from collections import UserDict
from datetime import datetime


class CustomPhoneException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class CustomBirthdayException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if self.validate(value):
            self.value = value
        else:
            raise CustomPhoneException("Invalid phone number.")

    @staticmethod
    def validate(value):
        return len(value) == 10 and value.isdigit()


class Birthday(Field):
    def __init__(self, value):
        if self.validate(value):
            self.value = value
        else:
            raise CustomBirthdayException("Invalid birthday date.")

    @staticmethod
    def validate(value):
        today = datetime.today().date()
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y").date()
            if birthday > today:
                return False
        except Exception:
            return False
        return True


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone_number):
        for i, phone in enumerate(self.phones):
            if phone.value == phone_number:
                del self.phones[i]
                return "Phone removed."
        raise ValueError("Phone not found.")

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return "Phone changed."
        raise ValueError("Phone not found.")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return "Birthday added"

    def __str__(self):
        return f"Contact name: {self.name.value},\
        phones: {'; '.join(p.value for p in self.phones)}, \
        birthday: {self.birthday.value if self.birthday else 'Uknown date'}"


class AddressBook(UserDict):
    file_name = "data.bin"

    def save(self):
        with open(AddressBook.file_name, "wb") as fh:
            pickle.dump(self.data, fh)

    def load(self):
        try:
            with open(AddressBook.file_name, "rb") as fh:
                self.data = pickle.load(fh)
        except FileNotFoundError:
            return None

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        del self.data[name]

    def get_birthdays_per_week(self):
        week_days = {"Monday": [], "Tuersday": [], "Wednesday": [],
                     "Thursday": [], "Friday": []}
        today = datetime.today().date()
        birthday_info = []
        for name, record in self.data.items():
            if not record.birthday:
                continue
            birthday_obj = datetime.strptime(
                record.birthday.value, "%d.%m.%Y").date()
            birthday_this_year = birthday_obj.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_obj.replace(
                    year=today.year + 1)
            delta_days = (birthday_this_year - today).days

            if delta_days < 7:
                weekday = birthday_this_year.weekday()
                if weekday in [0, 5, 6]:
                    week_days["Monday"].append(name)
                elif weekday == 1:
                    week_days["Tuersday"].append(name)
                elif weekday == 2:
                    week_days["Wednesday"].append(name)
                elif weekday == 3:
                    week_days["Thursday"].append(name)
                elif weekday == 4:
                    week_days["Friday"].append(name)

        for key, value in week_days.items():
            if value != []:
                birthday_info.append(f"{key}: {', '.join(value)}\n")
        if birthday_info:
            return birthday_info
        else:
            return "Next week birthays not found"


if __name__ == "__main__":
    # реалізація класу

    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("25.10.1989")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("29.10.1988")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    jane = book.find("Jane")

    print(john)
    # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    # Виведення: 5555555555
    print(f"{john.name}: {found_phone} : {john.birthday}")

    print(f"{jane.name}: {found_phone} : {jane.birthday}")

    print(book.get_birthdays_per_week())
    # Видалення запису Jane
    book.delete("Jane")