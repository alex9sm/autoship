import customtkinter as ctk
import os
from PIL import Image
from labels_tab import LabelsTab
from tracking_tab import TrackingTab

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("AutoShip")
        self.geometry("1000x600")
        
        # Set the appearance mode to dark
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # App Logo/Title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="AutoShip", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Sidebar buttons
        self.label_button = ctk.CTkButton(self.sidebar_frame, text="Labels", command=self.show_label_frame)
        self.label_button.grid(row=1, column=0, padx=20, pady=10)
        
        self.tracking_button = ctk.CTkButton(self.sidebar_frame, text="Tracking", command=self.show_tracking_frame)
        self.tracking_button.grid(row=2, column=0, padx=20, pady=10)
        
        # Appearance mode settings
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                      command=self.change_appearance_mode)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_menu.set("Dark")
        
        # Initialize tab modules
        self.labels_tab = LabelsTab(self)
        self.tracking_tab = TrackingTab(self)
        
        # Set default tab
        self.show_label_frame()
        
    def show_label_frame(self):
        # Hide tracking frame and show label frame
        self.tracking_tab.frame.grid_forget()
        self.labels_tab.frame.grid(row=0, column=1, sticky="nsew")
        # Update button colors to highlight active tab
        self.label_button.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        self.tracking_button.configure(fg_color=["#3E454A", "#2A2D2E"])
        
    def show_tracking_frame(self):
        # Hide label frame and show tracking frame
        self.labels_tab.frame.grid_forget()
        self.tracking_tab.frame.grid(row=0, column=1, sticky="nsew")
        # Update button colors to highlight active tab
        self.label_button.configure(fg_color=["#3E454A", "#2A2D2E"])
        self.tracking_button.configure(fg_color=["#3B8ED0", "#1F6AA5"])
    
    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode.lower())


if __name__ == "__main__":
    app = App()
    app.mainloop() 