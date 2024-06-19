import customtkinter
from tkinter import Canvas
import os


class OSD:
    def __init__(self):

        self.started = False
        customtkinter.set_appearance_mode("light")  
        customtkinter.set_default_color_theme("dark-blue")  

        self.app = customtkinter.CTk()

        self.window_width = 960
        self.window_height = 360

        self.screen_width = self.app.winfo_screenwidth()
        self.screen_height = self.app.winfo_screenheight()


        x_cordinate = int((self.screen_width) - (self.window_width))
        y_cordinate = int((self.screen_height) - (self.window_height))

        self.app.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, x_cordinate, y_cordinate))
        self.app.overrideredirect(True)

        self.tabview = customtkinter.CTkTabview(master=self.app, width=self.window_width, height=self.window_height, bg_color="transparent", fg_color="transparent")
        self.tabview.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

        self.tabs = ["SmartMirror", "Network", "System"]

        for tab in self.tabs:
            self.tabview.add(tab)
            label = customtkinter.CTkLabel(master=self.tabview.tab(tab), text=tab, fg_color="transparent", bg_color="transparent", font=("Aptos", 48,'bold'))
            label.place(anchor=customtkinter.NW, relx=0.02, rely=0.01)
            line = Canvas(self.tabview.tab(tab), width=self.window_width , height=1, bg="white")
            line.place(anchor=customtkinter.NW, relx=0.0, rely=0.2)

        self.selected_button = 0

    def chainge_mode_simple(self):
        print("button pressed")
        os.system("DISPLAY=:0 xte 'keydown Alt_L' 'key 1' 'keyup Alt_L'")

    def chainge_mode_complex(self):
        print("button pressed")
        os.system("DISPLAY=:0 xte 'keydown Alt_L' 'key 2' 'keyup Alt_L'")

    def chainge_mode_jokes(self):
        print("button pressed")
        os.system("DISPLAY=:0 xte 'keydown Alt_L' 'key 3' 'keyup Alt_L'")

    def reboot(self):
        os.system("sudo systemctl reboot")

    def shutdown(self):
        os.system("sudo systemctl shutdown")

    def restart_firefox(self):
        os.system("sudo systemctl restart kiosk.service")

    def restart_OSD(self):
        os.system("sudo systemctl restart pythonserver.service")

    def press_F11(self):
        os.system("DISPLAY=:0 xte 'key F11'")

    def cycle_tabs(self):
        self.tabview.set(self.tabs[self.tabview.index(self.tabview.get()) + 1] if self.tabview.index(self.tabview.get()) < len(self.tabs) - 1 else self.tabs[0])

    def cycle_buttons_forward(self):
        tab = self.tabview.get()
        buttons = [widget for widget in self.tabview.tab(tab).winfo_children() if isinstance(widget, customtkinter.windows.widgets.ctk_button.CTkButton)]
        if not buttons:
            return
        buttons[self.selected_button].configure(border_width = 0)
        self.selected_button = (self.selected_button + 1) % len(buttons)
        buttons[self.selected_button].configure(border_width = 4)
        self.app.update()

    def cycle_buttons_backward(self):
        tab = self.tabview.get()
        buttons = [widget for widget in self.tabview.tab(tab).winfo_children() if isinstance(widget, customtkinter.windows.widgets.ctk_button.CTkButton)]
        if not buttons:
            return
        buttons[self.selected_button].configure(border_width = 0)
        self.selected_button = (self.selected_button - 1) % len(buttons)
        buttons[self.selected_button].configure(border_width = 4)
        self.app.update()

    def call_button(self):
        tab = self.tabview.get()
        buttons = [widget for widget in self.tabview.tab(tab).winfo_children() if isinstance(widget, customtkinter.windows.widgets.ctk_button.CTkButton)]
        if not buttons:
            return
        buttons[self.selected_button].invoke()

    def create_smartmirror_tab(self):
        label = customtkinter.CTkLabel(master=self.tabview.tab("SmartMirror"), text="Modus", fg_color="transparent", bg_color="transparent", font=("Aptos", 32))
        label.place(anchor=customtkinter.W, relx=0.03, rely=0.3)

        modes = ["Simple", "Complex", "Jokes"]
        functions = [self.chainge_mode_simple, self.chainge_mode_complex, self.chainge_mode_jokes]

        for i in range(len(modes)):
            button = customtkinter.CTkButton(master=self.tabview.tab("SmartMirror"), text=f"{modes[i]}", command=functions[i], width=40,font=("Aptos", 32))
            button.grid(row=0, column=i, padx=10, pady=120)

    def create_network_tab(self):
        ip = os.popen('hostname -I | awk \'{print $1}\'').read().strip()
        hostname = os.popen('hostname').read().strip()
        network = os.popen('nmcli -t -f name connection show --active | awk \'NR >0 && NR<=1 {print $0}\'').read().strip()

        label = customtkinter.CTkLabel(master=self.tabview.tab("Network"), text=f"IP Address: {ip}", fg_color="transparent", bg_color="transparent", font=("Aptos", 32))
        label.place(anchor=customtkinter.W, relx=0.03, rely=0.25)

        label = customtkinter.CTkLabel(master=self.tabview.tab("Network"), text=f"Hostname: {hostname}", fg_color="transparent", bg_color="transparent", font=("Aptos", 32))
        label.place(anchor=customtkinter.W, relx=0.03, rely=0.45)

        label = customtkinter.CTkLabel(master=self.tabview.tab("Network"), text=f"Network: {network} ", fg_color="transparent", bg_color="transparent", font=("Aptos", 32))
        label.place(anchor=customtkinter.W, relx=0.03, rely=0.65)

    def create_system_tab(self):
        label = customtkinter.CTkLabel(master=self.tabview.tab("System"), text="System", fg_color="transparent", bg_color="transparent", font=("Aptos", 32))
        label.place(anchor=customtkinter.W, relx=0.03, rely=0.3)

        label = customtkinter.CTkButton(master=self.tabview.tab("System"), text="Reboot", command=self.reboot, font=("Aptos", 32))
        label.place(anchor=customtkinter.W, relx=0.03, rely=0.45)

        label = customtkinter.CTkButton(master=self.tabview.tab("System"), text="Shutdown", command=self.shutdown, font=("Aptos", 32))
        label.place(anchor=customtkinter.W, relx=0.23, rely=0.45)

        label = customtkinter.CTkLabel(master=self.tabview.tab("System"), text="SmartMirror", fg_color="transparent", bg_color="transparent", font=("Aptos", 32))
        label.place(anchor=customtkinter.W, relx=0.03, rely=0.60)

        label = customtkinter.CTkButton(master=self.tabview.tab("System"), text="Restart Firefox", command=self.restart_firefox, font=("Aptos", 32))
        label.place(anchor=customtkinter.W, relx=0.03, rely=0.75)

        label = customtkinter.CTkButton(master=self.tabview.tab("System"), text="Restart OSD", command=self.restart_OSD, font=("Aptos", 32))
        label.place(anchor=customtkinter.W, relx=0.33, rely=0.75)

        label = customtkinter.CTkButton(master=self.tabview.tab("System"), text="Press F11", command=self.press_F11, font=("Aptos", 32))
        label.place(anchor=customtkinter.W, relx=0.58, rely=0.75)

    def stop(self):
        if self.app and self.started:
            self.app.withdraw()  # Hide the window
            self.started = False

            self.app.quit()
            # self.app = None

    def please_stop(self):
        self.stop()

    def run(self):
        if self.app:
            self.app.deiconify()  # Show the window
        self.started = True
        self.create_smartmirror_tab()
        self.create_network_tab()
        self.create_system_tab()
        self.app.mainloop()