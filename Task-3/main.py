import tkinter
from tkinter import messagebox
import random
import json

def generate_pw():
    characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '#', '$', '%', '&', '(', ')', '*', '+', '=', '_', '-', '/', '?', '\\', '.', ',', '<', '>', '"', '\'']
    pw_list = [random.choice(characters) for _ in range(25)]
    random.shuffle(pw_list)
    pw_str = ''.join(pw_list)
    password_output.delete(0, tkinter.END)
    password_output.insert(0, pw_str)

def save_info():
    if not website_input.get() or not username_input.get() or not password_output.get():
        messagebox.showerror(message = 'Please complete all fields.')
    else:
        if messagebox.askokcancel(message = f"You are about to save: \nWebsite: {website_input.get()}\nUsername: {username_input.get()}\nPassword: {password_output.get()}\n") == True:
            new_dict = {website_input.get(): {'username' : username_input.get(), 'password' : password_output.get()}}
            try:
                read_handler = open('usernames_and_passwords.json', 'r')
                all_dicts = json.load(read_handler)
                read_handler.close()
            except:
                all_dicts = {}
            write_handler = open('usernames_and_passwords.json', 'w')
            all_dicts.update(new_dict)
            json.dump(all_dicts, write_handler, indent = 4)
            website_input.delete(0, tkinter.END)
            username_input.delete(0, tkinter.END)
            password_output.delete(0, tkinter.END)
            write_handler.close()
            messagebox.showinfo(message = 'Info saved')

def find_pw():
    try:
        read_handler = open('usernames_and_passwords.json', 'r')
    except:
        messagebox.showinfo(message = "Can't search. No info stored yet.")
    else:
        json_dict = json.load(read_handler)
        for website_name, info_dict in json_dict.items():
            if website_input.get().lower().strip() == website_name.lower().strip():
                messagebox.showinfo(message = f"Account on {website_name.title()}:\nUsername: {info_dict['username']}\nPassword: {info_dict['password']}\n(Copy and paste these before you close the window)")
                return
        messagebox.showinfo(message = "No info saved for that website.\nDid you spell it correctly?")

window = tkinter.Tk()
window.title('Password Manager')
window.config(padx = 35, pady = 35)

website_label = tkinter.Label(text = 'Website:')
website_label.grid(row = 1, column = 1)
website_input = tkinter.Entry(width = 27)
website_input.grid(row = 1, column = 2, columnspan = 1)
website_input.focus()

search_button = tkinter.Button(text = 'Search', width = 6, command = find_pw)
search_button.grid(row = 1, column = 3)

username_label = tkinter.Label(text = 'Username:')
username_label.grid(row = 2, column = 1)
username_input = tkinter.Entry(width = 38)
username_input.grid(row = 2, column = 2, columnspan = 2)

password_label = tkinter.Label(text = 'Password:')
password_label.grid(row = 3, column = 1)
password_output = tkinter.Entry(width = 27)
password_output.grid(row = 3, column = 2)
password_generator_button = tkinter.Button(text = 'Generate', command = generate_pw)
password_generator_button.grid(row = 3, column = 3)

save_button = tkinter.Button(text = 'Save', command = save_info, width = 36)
save_button.grid(row = 4, column = 2, columnspan= 2)

window.mainloop()