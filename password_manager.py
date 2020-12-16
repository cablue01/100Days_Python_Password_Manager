from tkinter import *
from tkinter import messagebox  # import * only gets you all the classes and constants hence this line needed
from password import *
import pyperclip
import pandas as pd


class PasswordManager:
    def __init__(self, data_csv, default_email):
        self.data = pd.read_csv(data_csv).sort_values(by="website")
        print(self.data.info())
        self.default_email = default_email
        self.mode = "Add"
        self.data_file_name = data_csv

        # create form
        self.window = Tk()
        self.window.title("Password Manager")
        self.window.config(padx=50, pady=50)
        self.icon_img = PhotoImage(file="key.png")
        self.window.iconphoto(False, self.icon_img)

        self.canvas = Canvas(width=200, height=200, highlightthickness=0)
        self.logo_img = PhotoImage(file="logo.png")
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.grid(column=1, row=0)

        self.search_label = Label(text="Search")
        self.search_label.grid(row=1, column=0)
        self.website_list = self.data["website"].to_list()
        self.selected_variable = StringVar()
        self.selected_variable.set("Select website")
        self.search_dropdown = OptionMenu(self.window, self.selected_variable, *self.website_list,
                                          command=self.load_website)
        self.search_dropdown.grid(row=1, column=1, columnspan=2)
        self.search_dropdown.config(width=36)

        self.website_label = Label(text="Website")
        self.website_label.grid(column=0, row=2)
        self.website_label.config(pady=3)
        self.website_input = Entry(width=42)
        self.website_input.grid(column=1, row=2, columnspan=2)
        self.website_input.focus()

        self.email_label = Label(text="Email/Username")
        self.email_label.grid(column=0, row=3)
        self.email_label.config(pady=3)
        self.email_input = Entry(width=42)
        self.email_input.grid(column=1, row=3, columnspan=2)
        self.email_input.insert(0, default_email)

        self.password_label = Label(text="Password")
        self.password_label.grid(column=0, row=4)
        self.password_input = Entry(width=33)
        self.password_input.grid(column=1, row=4)
        self.generate_button = Button(text="generate", command=self.refresh_password)
        self.generate_button.grid(column=2, row=4)

        self.auth_token_label = Label(text="Auth Token")
        self.auth_token_label.grid(column=0, row=5)
        self.auth_token_input = Entry(width=33)
        self.auth_token_input.grid(column=1, row=5)
        self.auth_token_button = Button(text="copy", command=self.copy_auth_token)
        self.auth_token_button.grid(column=2, row=5)
        self.auth_token_button.config(width=7)

        self.app_id_label = Label(text="APP ID")
        self.app_id_label.grid(column=0, row=6)
        self.app_id_input = Entry(width=33)
        self.app_id_input.grid(column=1, row=6)
        self.app_id_button = Button(text="copy", command=self.copy_app_id)
        self.app_id_button.grid(column=2, row=6)
        self.app_id_button.config(width=7)

        self.api_key_label = Label(text="API KEY")
        self.api_key_label.grid(column=0, row=7)
        self.api_key_input = Entry(width=33)
        self.api_key_input.grid(column=1, row=7)
        self.api_key_button = Button(text="copy", command=self.copy_api_key)
        self.api_key_button.grid(column=2, row=7)
        self.api_key_button.config(width=7)

        self.two_factor_label = Label(text="Two Factor").grid(column=0, row=8)
        self.two_factor_var = IntVar()
        self.two_factor_cb = Checkbutton(text=" " * 60, variable=self.two_factor_var)
        self.two_factor_cb.grid(column=1, row=8)

        self.notes_label = Label(text="Notes").grid(column=0, row=9)
        self.notes_text = Text(width=33, height=5)
        self.notes_text.grid(column=1, row=9, pady=5, columnspan=2)

        self.add_button = Button(text=self.mode, width=35, command=self.update_data)
        self.add_button.grid(column=1, row=10, columnspan=1)
        self.add_button.config(width=28)

        self.cancel_button = Button(text="cancel", width=35, command=self.cancel)
        self.cancel_button.grid(column=2, row=10, columnspan=1)
        self.cancel_button.config(width=7)

        print("PasswordManager object created")

    def print_data(self):
        print(self.data)

    def load_website_list(self):
        self.search_dropdown["menu"].destroy()
        self.website_list = self.data["website"].to_list()
        self.search_dropdown = OptionMenu(self.window, self.selected_variable, *self.website_list,
                                          command=self.load_website)
        self.search_dropdown.grid(row=1, column=1, columnspan=2)
        self.search_dropdown.config(width=36)

    def open_form(self):
        self.window.mainloop()

    def load_input(self, input_control, data):
        input_control.delete(0, END)
        print(data, type(data))
        if not pd.isnull(data):
            input_control.insert(0, data)

    def load_website(self, website):
        print(f"load data for {website}")
        ws_data = self.data[self.data.website == website]

        self.load_input(self.website_input, ws_data["website"].item())
        self.load_input(self.email_input, ws_data["logon"].item())
        self.load_input(self.password_input, ws_data["password"].item())
        self.load_input(self.app_id_input, ws_data["app_id"].item())
        self.load_input(self.api_key_input, ws_data["api_key"].item())
        self.load_input(self.auth_token_input, ws_data["auth_token"].item())

        self.two_factor_var.set(ws_data["two_factor"].item())

        self.notes_text.delete(1.0, END)
        if not pd.isnull(ws_data["notes"].item()):
            self.notes_text.insert(1.0, ws_data["notes"].item())

        self.set_mode("Update")

    def refresh_password(self):
        new_password = generate_pwd()
        self.password_input.delete(0, END)
        self.password_input.insert(0, new_password)
        pyperclip.copy(new_password)

    def copy_auth_token(self):
        pyperclip.copy(self.auth_token_input.get())

    def copy_app_id(self):
        pyperclip.copy(self.app_id_input.get())
        
    def copy_api_key(self):
        pyperclip.copy(self.api_key_input.get())

    def reset_form(self):
        self.website_input.delete(0, END)
        self.email_input.delete(0, END)
        self.email_input.insert(0, self.default_email)
        self.password_input.delete(0, END)
        self.auth_token_input.delete(0, END)
        self.app_id_input.delete(0, END)
        self.api_key_input.delete(0, END)
        self.selected_variable.set("Select website")
        self.two_factor_var.set(0)
        self.set_mode("Add")
        self.notes_text.delete(1.0, END)

    def cancel(self):
        self.reset_form()

    def set_mode(self, mode):
        self.add_button.config(text=mode)
        self.mode = mode

    def form_data_invalid(self):
        website = self.website_input.get()
        user_name = self.email_input.get()
        pwd = self.password_input.get()
        return len(website) == 0 or len(user_name) == 0 or len(pwd) == 0

    def update_data(self):
        website = self.website_input.get()
        user_name = self.email_input.get()
        pwd = self.password_input.get()
        auth_token = self.auth_token_input.get()
        app_id = self.app_id_input.get()
        api_key = self.api_key_input.get()
        two_factor = self.two_factor_var.get()
        notes = self.notes_text.get(1.0, END).strip()

        if self.form_data_invalid():
            msg = "website, email, and password required"
            messagebox.showinfo(title="Oops", message=msg)
        elif self.mode == "Update":
            print("Update data")
            data_row = self.data[self.data.website == website]
            self.data.loc[data_row.index, "password"] = pwd
            self.data.loc[data_row.index, "logon"] = user_name
            self.data.loc[data_row.index, "auth_token"] = auth_token
            self.data.loc[data_row.index, "app_id"] = app_id
            self.data.loc[data_row.index, "api_key"] = api_key
            self.data.loc[data_row.index, "two_factor"] = two_factor
            self.data.loc[data_row.index, "notes"] = notes

            new_data = self.data.copy()
            new_data.to_csv(self.data_file_name, index=False)
            self.reset_form()
        elif self.mode == "Add":
            print("Add new website")
            new_fields = {
                "website": website,
                "logon": user_name,
                "password": pwd,
                "auth_token": auth_token,
                "app_id": app_id,
                "api_key": api_key,
                "two_factor": two_factor,
                "notes": notes,
            }
            new_data = self.data.append(new_fields, ignore_index=True).copy()
            new_data.sort_values(by="website").to_csv(self.data_file_name, index=False)
            self.data = pd.read_csv(self.data_file_name).sort_values(by="website")
            self.load_website_list()
            self.reset_form()
