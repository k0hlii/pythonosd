import customtkinter
from tkinter import Canvas
import os

class OSD:
    def __init__(self):
        self.started = False
        customtkinter.set_appearance_mode("dark")  
        customtkinter.set_default_color_theme("dark-blue")  

        self.app = customtkinter.CTk()  
        self.app.geometry("720x480")

        self.app.overrideredirect(True)

        self.tabview = customtkinter.CTkTabview(master=self.app, width=720, height=480, bg_color="transparent", fg_color="transparent")
        self.tabview.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

        self.tabs = ["SmartMirror", "Network", "System"]

        for tab in self.tabs:
            self.tabview.add(tab)
            label = customtkinter.CTkLabel(master=self.tabview.tab(tab), text=tab, fg_color="transparent", bg_color="transparent", font=("Aptos", 24))
            label.place(anchor=customtkinter.NW, relx=0.02, rely=0.01)
            line = Canvas(self.tabview.tab(tab), width=800, height=1, bg="white")
            line.place(anchor=customtkinter.NW, relx=0.0, rely=0.2)

        self.selected_button = 0

    def button_function(self):
        print("button pressed")

    def reboot(self):
        os.system("sudo systemctl reboot")

    def shutdown(self):
        os.system("sudo systemctl shutdown")

    def stop_service(self):
        os.system("sudo systemctl restart kiosk.service")

    def cycle_tabs(self):
        self.tabview.set(self.tabs[self.tabview.index(self.tabview.get()) + 1] if self.tabview.index(self.tabview.get()) < len(self.tabs) - 1 else self.tabs[0])

    def cycle_buttons_forward(self):
        tab = self.tabview.get()
        buttons = [widget for widget in self.tabview.tab(tab).winfo_children() if isinstance(widget, customtkinter.windows.widgets.ctk_button.CTkButton)]
        if not buttons:
            return
        buttons[self.selected_button].configure(border_width = 0)
        self.selected_button = (self.selected_button + 1) % len(buttons)
        buttons[self.selected_button].configure(border_width = 2)
        self.app.update()

    def cycle_buttons_backward(self):
        tab = self.tabview.get()
        buttons = [widget for widget in self.tabview.tab(tab).winfo_children() if isinstance(widget, customtkinter.windows.widgets.ctk_button.CTkButton)]
        if not buttons:
            return
        buttons[self.selected_button].configure(border_width = 0)
        self.selected_button = (self.selected_button - 1) % len(buttons)
        buttons[self.selected_button].configure(border_width = 2)
        self.app.update()

    def call_button(self):
        tab = self.tabview.get()
        buttons = [widget for widget in self.tabview.tab(tab).winfo_children() if isinstance(widget, customtkinter.windows.widgets.ctk_button.CTkButton)]
        if not buttons:
            return
        buttons[self.selected_button].invoke()

    def create_smartmirror_tab(self):
        label = customtkinter.CTkLabel(master=self.tabview.tab("SmartMirror"), text="Modus", fg_color="transparent", bg_color="transparent", font=("Aptos", 18))
        label.place(anchor=customtkinter.W, relx=0.03, rely=0.3)

        modes = ["Dashboard", "WordClock", "MillionTimes", "SolarSystem", "FlipDot"]

        for i in range(5):
            button = customtkinter.CTkButton(master=self.tabview.tab("SmartMirror"), text=f"{modes[i]}", command=self.button_function, width=40)
            button.grid(row=0, column=i, padx=10, pady=150)

    def create_network_tab(self):
        ip = os.popen('hostname -I | awk \'{print $1}\'').read().strip()
        hostname = os.popen('hostname').read().strip()
        network = os.popen('nmcli -t -f name connection show --active | awk \'NR >1 && NR<=2 {print $0}\'').read().strip()

        label = customtkinter.CTkLabel(master=self.tabview.tab("Network"), text=f"IP Address: {ip}", fg_color="transparent", bg_color="transparent", font=("Aptos", 18))
        label.place(anchor=customtkinter.W, relx=0.03, rely=0.25)

        label = customtkinter.CTkLabel(master=self.tabview.tab("Network"), text=f"Hostname: {hostname}", fg_color="transparent", bg_color="transparent", font=("Aptos", 18))
        label.place(anchor=customtkinter.W, relx=0.03, rely=0.45)

        label = customtkinter.CTkLabel(master=self.tabview.tab("Network"), text=f"Network: {network} ", fg_color="transparent", bg_color="transparent", font=("Aptos", 18))
        label.place(anchor=customtkinter.W, relx=0.03, rely=0.65)

    def create_system_tab(self):
        label = customtkinter.CTkButton(master=self.tabview.tab("System"), text="Reboot", command=self.reboot)
        label.place(anchor=customtkinter.W, relx=0.03, rely=0.25)

        label = customtkinter.CTkButton(master=self.tabview.tab("System"), text="Shutdown", command=self.shutdown)
        label.place(anchor=customtkinter.W, relx=0.03, rely=0.45)

        label = customtkinter.CTkButton(master=self.tabview.tab("System"), text="Restart Firefox", command=self.stop_service)
        label.place(anchor=customtkinter.W, relx=0.03, rely=0.65)

    def stop(self):
        if self.app and self.started:
            self.app.withdraw()  # Hide the window

            self.app.quit()
            # self.app = None
            self.started = False

    def run(self):
        if self.app:
            self.app.deiconify()  # Show the window
        self.started = True
        self.started = True
        self.create_smartmirror_tab()
        self.create_network_tab()
        self.create_system_tab()
        self.app.mainloop()
