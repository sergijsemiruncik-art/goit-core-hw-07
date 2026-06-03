from main import AddressBook, Record


# Parses user input by splitting it into command and arguments
def parse_input(user_input: str):
    cmd, *args = user_input.strip().split()
    cmd = cmd.lower()
    return cmd, args


# Adds a new contact or phone number to an existing contact
# Requires: name and phone number as arguments
def add_contact(args, book):
    if len(args) != 2:
        return "Please enter name and phone number."

    name, phone = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)

    record.add_phone(phone)
    return "Contact added."


# Changes an existing phone number for a contact
# Requires: name, old phone number, and new phone number
def change_contact(args, book):
    if len(args) != 3:
        return "Please enter name, old phone number and new phone number."

    name, old_phone, new_phone = args
    record = book.find(name)

    if record is None:
        return "Contact not found."

    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


# Displays all phone numbers for a specific contact
# Requires: contact name
def show_phone(args, book):
    if len(args) != 1:
        return "Please enter a username."

    name = args[0]
    record = book.find(name)

    if record is None:
        return "Contact not found."

    if not record.phones:
        return "Contact has no phone number."

    return "; ".join(phone.value for phone in record.phones)


# Adds a birthday to a contact
# Requires: name and birthday in DD.MM.YYYY format
def add_birthday(args, book):
    if len(args) != 2:
        return "Please enter name and birthday."

    name, birthday = args
    record = book.find(name)

    if record is None:
        return "Contact not found."

    record.add_birthday(birthday)
    return "Birthday added."


# Displays the birthday for a specific contact
# Requires: contact name
def show_birthday(args, book):
    if len(args) != 1:
        return "Please enter a username."

    name = args[0]
    record = book.find(name)

    if record is None:
        return "Contact not found."

    if record.birthday is None:
        return "Birthday not found."

    return record.birthday.value.strftime("%d.%m.%Y")


# Shows all upcoming birthdays for the next 7 days
def show_birthdays(args, book):
    if args:
        return "The birthdays command does not accept arguments."

    birthdays = book.get_upcoming_birthdays()

    if not birthdays:
        return "No upcoming birthdays."

    return "\n".join(
        f"{item['name']}: {item['birthday']}" for item in birthdays
    )


# Displays all contacts in the address book
def show_all(book):
    if not book.data:
        return "No contacts saved."

    return str(book)


# Main function that runs the interactive bot loop
def main():
    # Initialize the address book
    book = AddressBook()

    # Display welcome message and available commands
    print("Welcome to the assistant bot!")
    print(
        "Commands:\n"
        "hello\n"
        "add [name] [phone]\n"
        "change [name] [old_phone] [new_phone]\n"
        "phone [name]\n"
        "add-birthday [name] [DD.MM.YYYY]\n"
        "show-birthday [name]\n"
        "birthdays\n"
        "all\n"
        "close / exit"
    )

    # Main event loop for processing user commands
    while True:
        user_input = input("Enter a command: ")

        try:
            command, args = parse_input(user_input)
        except ValueError:
            print("Please enter a command.")
            continue

        # Handle exit commands
        if command in ("close", "exit"):
            print("Good bye!")
            break

        # Greet the user
        elif command == "hello":
            print("How can I help you?")

        # Add a new contact with phone number
        elif command == "add":
            try:
                print(add_contact(args, book))
            except ValueError as error:
                print(error)

        # Change existing phone number for a contact
        elif command == "change":
            try:
                print(change_contact(args, book))
            except ValueError as error:
                print(error)

        # Display phone numbers for a contact
        elif command == "phone":
            print(show_phone(args, book))

        # Add birthday to a contact
        elif command == "add-birthday":
            try:
                print(add_birthday(args, book))
            except (TypeError, ValueError) as error:
                print(error)

        # Show birthday for a specific contact
        elif command == "show-birthday":
            print(show_birthday(args, book))

        # Show upcoming birthdays for the next 7 days
        elif command == "birthdays":
            print(show_birthdays(args, book))

        # Display all contacts
        elif command == "all":
            print(show_all(book))

        # Handle invalid commands
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
