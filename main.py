from tkinter import *
import random
import special_sym
from tkinter import messagebox
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pass():
    pass_list = []
    no_letters = random.randint(8, 10)
    no_symbols = random.randint(2, 4)
    no_numbers = random.randint(2, 4)

    for i in range(no_letters):
        pass_list.append(random.choice(special_sym.letters))
    for i in range(no_symbols):
        pass_list.append(random.choice(special_sym.symbols))
    for i in range(no_numbers):
        pass_list.append(random.choice(special_sym.numbers))

    random.shuffle(pass_list)
    my_pass = "".join(pass_list)
    pwd_entry.insert(0, my_pass)
    pyperclip.copy(my_pass)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    web = web_entry.get()
    email = e_name.get()
    pswrd = pwd_entry.get()
    new_data = {
        web: {
            "email": email,
            "password": pswrd,
        }
    }

    if len(web) == 0 or len(email) == 0 or len(pswrd) == 0 or web.isspace() or email.isspace() or pswrd.isspace():
        messagebox.showinfo(title="Oops", message="Please! don't leave any fields empty")
    else:
        is_ok = messagebox.askokcancel(title=web, message=f"These are the details entered: \nEmail: {email}"
                                                          f"\nPassword: {pswrd} \n Is it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # reading the old data
                    e_data = json.load(data_file)

            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # updating old data
                e_data.update(new_data)
                with open("data.json", "w") as data_file:
                    # saving the data
                    json.dump(e_data, data_file, indent=4)
            finally:
                web_entry.delete(0, END)
                pwd_entry.delete(0, END)
        messagebox.showinfo(title="Thank you", message="Your credentials are saved successfully.")


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    web_find = web_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data Exists!")
    else:
        if web_find in data:
            e_mail = data[web_find]["email"]
            pass_word = data[web_find]["password"]
            messagebox.showinfo(title=web_find, message=f"Email: {e_mail}\n Password: {pass_word}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {web_find} exists.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

canvas = Canvas(width=200, height=200, highlightthickness=0)
image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

# labels
website = Label(text="Website:")
website.grid(column=0, row=1)

name = Label(text="Email/Username:")
name.grid(column=0, row=2)

password = Label(text="Password:")
password.grid(column=0, row=3)

# Buttons
add = Button(text="Add", width=36, command=save)
add.grid(column=1, row=4, columnspan=2, padx=5, pady=5)

genpass = Button(text="Generate Password", width=15, command=generate_pass)
genpass.grid(column=2, row=3, columnspan=2)

search = Button(text="Search", width=15, command=find_password)
search.grid(column=2, row=1)

# Entry
web_entry = Entry(width=25)
web_entry.grid(column=1, row=1, sticky="ew", padx=5, pady=5)
web_entry.focus()

e_name = Entry(width=35)
e_name.grid(column=1, row=2, columnspan=2, sticky="ew", padx=5, pady=5)
e_name.insert(END, "")
pwd_entry = Entry(width=23)
pwd_entry.grid(column=1, row=3, sticky="ew", padx=5, pady=5)

window.mainloop()
