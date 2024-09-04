import customtkinter as ctk
import functions
import asyncio
import threading

# Set the appearance mode and theme
ctk.set_appearance_mode("dark")  # Options: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"


class DiscordAltManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Alt Manager")
        self.root.geometry("500x300")  # Set a fixed size for the window

        # Frame for holding the options
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Initialize label for status messages
        self.label = ctk.CTkLabel(self.frame, text="", text_color="green")
        self.label.pack(pady=10)

        # Initialize OptionMenu (dropdown) for account selection
        self.listbox_label = ctk.CTkLabel(self.frame, text="Select Account:")
        self.listbox_label.pack(pady=5)

        self.listbox = ctk.CTkOptionMenu(self.frame, values=[])
        self.refresh_optionmenu()
        self.listbox.pack(pady=5)

        # Initialize buttons in a horizontal frame
        self.button_frame = ctk.CTkFrame(self.frame)
        self.button_frame.pack(pady=10, fill="x")

        self.login_button = ctk.CTkButton(self.button_frame, text="Login", command=self.login_callback)
        self.login_button.pack(side="left", expand=True, padx=5)

        self.add_button = ctk.CTkButton(self.button_frame, text="Add Account", command=self.add_account_callback)
        self.add_button.pack(side="left", expand=True, padx=5)

        self.remove_button = ctk.CTkButton(self.button_frame, text="Remove", command=self.delete_account)
        self.remove_button.pack(side="left", expand=True, padx=5)

        # Setup asyncio event loop
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.start_loop, daemon=True).start()

    def start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def refresh_optionmenu(self):
        accounts = functions.get_accounts()
        self.listbox.configure(values=accounts)

    def login_callback(self):
        selected_account_name = self.listbox.get()
        selected_account_token = functions.get_token_with_name(selected_account_name)
        asyncio.run_coroutine_threadsafe(self.discord_token_login(selected_account_token), self.loop)

    async def discord_token_login(self, token):
        await functions.discord_token_login(token)

    def add_account(self, name, token):
        functions.add_account(name, token)
        self.label.configure(text="Added Account!", text_color="green")
        self.refresh_optionmenu()

    def add_account_callback(self):
        name_dialog = ctk.CTkInputDialog(text="Account Name", title="Add New Account")
        name = name_dialog.get_input()
        token_dialog = ctk.CTkInputDialog(text="Discord Token", title="Add New Account")
        token = token_dialog.get_input()
        if name and token:  # Check if user provided both name and token
            self.add_account(name, token)
        else:
            self.label.configure(text="Failed to add account. Both fields are required.", text_color="red")

    def delete_account(self):
        selected_account = self.listbox.get()
        if selected_account:  # Ensure an account is selected
            functions.delete_account(selected_account)
            self.label.configure(text="Deleted Account!", text_color="green")
            self.refresh_optionmenu()
        else:
            self.label.configure(text="No account selected to delete.", text_color="red")


# Main event loop
if __name__ == "__main__":
    root = ctk.CTk()
    app = DiscordAltManagerApp(root)
    root.mainloop()
