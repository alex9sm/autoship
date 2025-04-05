import customtkinter as ctk
import os
import json
import uuid

class LabelsTab:
    def __init__(self, parent):
        self.parent = parent
        
        # Create main frame
        self.frame = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
        
        # Label frame title
        self.label_title = ctk.CTkLabel(self.frame, text="Labels", font=ctk.CTkFont(size=24, weight="bold"))
        self.label_title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Create tabs frame for Template and Receiver
        self.label_tabs_frame = ctk.CTkFrame(self.frame)
        self.label_tabs_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Configure label_tabs_frame grid
        self.label_tabs_frame.grid_columnconfigure(0, weight=1)
        self.label_tabs_frame.grid_rowconfigure(1, weight=1)
        
        # Create tab buttons frame
        self.label_tab_buttons = ctk.CTkFrame(self.label_tabs_frame)
        self.label_tab_buttons.grid(row=0, column=0, sticky="ew")
        
        # Create tab buttons
        self.template_button = ctk.CTkButton(self.label_tab_buttons, text="Template", 
                                           command=self.show_template_tab,
                                           fg_color="transparent", border_width=1)
        self.template_button.grid(row=0, column=0, padx=(0, 5), pady=10, sticky="e")
        
        self.receiver_button = ctk.CTkButton(self.label_tab_buttons, text="Receiver", 
                                          command=self.show_receiver_tab,
                                          fg_color="transparent", border_width=1)
        self.receiver_button.grid(row=0, column=1, padx=(5, 0), pady=10, sticky="w")
        
        self.label_tab_buttons.grid_columnconfigure(0, weight=1)
        self.label_tab_buttons.grid_columnconfigure(1, weight=1)
        
        # Create content frames for template and receiver tabs
        self.template_frame = ctk.CTkFrame(self.label_tabs_frame, fg_color="transparent")
        self.receiver_frame = ctk.CTkFrame(self.label_tabs_frame, fg_color="transparent")
        
        # Setup Template tab content
        self.setup_template_tab()
        
        # Setup Receiver tab content
        self.setup_receiver_tab()
        
        # Show default template tab
        self.show_template_tab()
    
    def setup_template_tab(self):
        # Template tab content
        self.template_title = ctk.CTkLabel(self.template_frame, text="Template Settings", font=ctk.CTkFont(size=18, weight="bold"))
        self.template_title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")
        
        # Create scrollable frame for template fields
        self.template_scrollable_frame = ctk.CTkScrollableFrame(self.template_frame, width=700, height=400)
        self.template_scrollable_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.template_frame.grid_rowconfigure(1, weight=1)
        self.template_frame.grid_columnconfigure(0, weight=1)
        
        # Template settings
        current_row = 0
        
        # Template Name
        self.template_name_label = ctk.CTkLabel(self.template_scrollable_frame, text="Template Name:")
        self.template_name_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.template_name_entry = ctk.CTkEntry(self.template_scrollable_frame, width=200)
        self.template_name_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        current_row += 1
        
        # Service Speed
        self.service_speed_label = ctk.CTkLabel(self.template_scrollable_frame, text="Service Speed:")
        self.service_speed_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.service_speed_menu = ctk.CTkOptionMenu(self.template_scrollable_frame, 
                                                 values=["USPS First Class", "USPS Priority", "USPS Express", "UPS Ground", "UPS Next Day Air"])
        self.service_speed_menu.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        self.service_speed_menu.set("USPS Priority")
        current_row += 1
        
        # Sender section header
        self.sender_section_label = ctk.CTkLabel(self.template_scrollable_frame, text="Sender Information", 
                                               font=ctk.CTkFont(size=14, weight="bold"))
        self.sender_section_label.grid(row=current_row, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")
        current_row += 1
        
        # Sender Name
        self.sender_name_label = ctk.CTkLabel(self.template_scrollable_frame, text="Name:")
        self.sender_name_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.sender_name_entry = ctk.CTkEntry(self.template_scrollable_frame, width=200)
        self.sender_name_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        current_row += 1
        
        # Sender Company
        self.sender_company_label = ctk.CTkLabel(self.template_scrollable_frame, text="Company:")
        self.sender_company_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.sender_company_entry = ctk.CTkEntry(self.template_scrollable_frame, width=200)
        self.sender_company_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        current_row += 1
        
        # Sender Address
        self.sender_address1_label = ctk.CTkLabel(self.template_scrollable_frame, text="Address Line 1:")
        self.sender_address1_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.sender_address1_entry = ctk.CTkEntry(self.template_scrollable_frame, width=200)
        self.sender_address1_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        current_row += 1
        
        # Sender Address Line 2
        self.sender_address2_label = ctk.CTkLabel(self.template_scrollable_frame, text="Address Line 2:")
        self.sender_address2_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.sender_address2_entry = ctk.CTkEntry(self.template_scrollable_frame, width=200)
        self.sender_address2_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        current_row += 1
        
        # Sender City
        self.sender_city_label = ctk.CTkLabel(self.template_scrollable_frame, text="City:")
        self.sender_city_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.sender_city_entry = ctk.CTkEntry(self.template_scrollable_frame, width=200)
        self.sender_city_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        current_row += 1
        
        # Sender State
        self.sender_state_label = ctk.CTkLabel(self.template_scrollable_frame, text="State:")
        self.sender_state_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.sender_state_entry = ctk.CTkEntry(self.template_scrollable_frame, width=200)
        self.sender_state_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        current_row += 1
        
        # Sender Postal Code
        self.sender_postal_code_label = ctk.CTkLabel(self.template_scrollable_frame, text="Postal Code:")
        self.sender_postal_code_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.sender_postal_code_entry = ctk.CTkEntry(self.template_scrollable_frame, width=200)
        self.sender_postal_code_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        current_row += 1
        
        # Sender Phone
        self.sender_phone_label = ctk.CTkLabel(self.template_scrollable_frame, text="Phone:")
        self.sender_phone_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.sender_phone_entry = ctk.CTkEntry(self.template_scrollable_frame, width=200)
        self.sender_phone_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        current_row += 1
        
        # Package section header
        self.package_section_label = ctk.CTkLabel(self.template_scrollable_frame, text="Package Information", 
                                                font=ctk.CTkFont(size=14, weight="bold"))
        self.package_section_label.grid(row=current_row, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")
        current_row += 1
        
        # Package Length
        self.package_length_label = ctk.CTkLabel(self.template_scrollable_frame, text="Length (inches):")
        self.package_length_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.package_length_entry = ctk.CTkEntry(self.template_scrollable_frame, width=100)
        self.package_length_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        self.package_length_entry.insert(0, "12")
        current_row += 1
        
        # Package Width
        self.package_width_label = ctk.CTkLabel(self.template_scrollable_frame, text="Width (inches):")
        self.package_width_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.package_width_entry = ctk.CTkEntry(self.template_scrollable_frame, width=100)
        self.package_width_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        self.package_width_entry.insert(0, "10")
        current_row += 1
        
        # Package Height
        self.package_height_label = ctk.CTkLabel(self.template_scrollable_frame, text="Height (inches):")
        self.package_height_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.package_height_entry = ctk.CTkEntry(self.template_scrollable_frame, width=100)
        self.package_height_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        self.package_height_entry.insert(0, "6")
        current_row += 1
        
        # Package Weight
        self.package_weight_label = ctk.CTkLabel(self.template_scrollable_frame, text="Weight (lbs):")
        self.package_weight_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.package_weight_entry = ctk.CTkEntry(self.template_scrollable_frame, width=100)
        self.package_weight_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        self.package_weight_entry.insert(0, "1")
        current_row += 1
        
        # Package Description
        self.package_description_label = ctk.CTkLabel(self.template_scrollable_frame, text="Description:")
        self.package_description_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.package_description_entry = ctk.CTkEntry(self.template_scrollable_frame, width=200)
        self.package_description_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        current_row += 1
        
        # Save button
        self.save_button = ctk.CTkButton(self.template_frame, text="Save Template", command=self.save_template)
        self.save_button.grid(row=2, column=0, columnspan=2, padx=20, pady=(10, 20))
        
        # Status message
        self.status_label = ctk.CTkLabel(self.template_frame, text="")
        self.status_label.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 20))
    
    def setup_receiver_tab(self):
        """Set up the Receiver tab content"""
        self.receiver_title = ctk.CTkLabel(self.receiver_frame, text="Receiver Information", font=ctk.CTkFont(size=18, weight="bold"))
        self.receiver_title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        self.receiver_content = ctk.CTkLabel(self.receiver_frame, text="Enter receiver details for your shipping labels.")
        self.receiver_content.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        # Add some sample receiver fields
        self.receiver_name_label = ctk.CTkLabel(self.receiver_frame, text="Name:")
        self.receiver_name_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.receiver_name_entry = ctk.CTkEntry(self.receiver_frame, width=200)
        self.receiver_name_entry.grid(row=2, column=1, padx=20, pady=(10, 0), sticky="w")
        
        self.receiver_address_label = ctk.CTkLabel(self.receiver_frame, text="Address:")
        self.receiver_address_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.receiver_address_entry = ctk.CTkEntry(self.receiver_frame, width=200)
        self.receiver_address_entry.grid(row=3, column=1, padx=20, pady=(10, 0), sticky="w")
    
    def save_template(self):
        """Save the template to a JSON file in the templates folder"""
        # Validate template name
        template_name = self.template_name_entry.get().strip()
        if not template_name:
            self.status_label.configure(text="Error: Template name is required", text_color="red")
            return
        
        # Create filename (replace spaces with underscores and add json extension)
        filename = template_name.replace(" ", "_") + ".json"
        file_path = os.path.join("templates", filename)
        
        # Create the directory if it doesn't exist
        if not os.path.exists("templates"):
            os.makedirs("templates")
        
        # Create the template data dictionary
        template_data = {
            "uuid": str(uuid.uuid4()),
            "service_speed": self.service_speed_menu.get(),
            "sender": {
                "name": self.sender_name_entry.get(),
                "company": self.sender_company_entry.get(),
                "address1": self.sender_address1_entry.get(),
                "address2": self.sender_address2_entry.get(),
                "city": self.sender_city_entry.get(),
                "state": self.sender_state_entry.get(),
                "postal_code": self.sender_postal_code_entry.get(),
                "phone": self.sender_phone_entry.get()
            },
            "recipient": {
                "name": "",
                "company": "",
                "address1": "",
                "address2": "",
                "city": "",
                "state": "",
                "postal_code": "",
                "phone": ""
            },
            "package": {
                "length": self.get_float_value(self.package_length_entry.get(), 12),
                "width": self.get_float_value(self.package_width_entry.get(), 10),
                "height": self.get_float_value(self.package_height_entry.get(), 6),
                "weight": self.get_float_value(self.package_weight_entry.get(), 1),
                "description": self.package_description_entry.get(),
                "provider": "evs",
                "references": [],
                "saturday_delivery": True
            }
        }
        
        # Save to JSON file
        try:
            with open(file_path, 'w') as json_file:
                json.dump(template_data, json_file, indent=2)
            self.status_label.configure(text=f"Template saved as {filename}", text_color="green")
        except Exception as e:
            self.status_label.configure(text=f"Error saving template: {str(e)}", text_color="red")
    
    def get_float_value(self, value_str, default=0):
        """Convert string to float with error handling"""
        try:
            return float(value_str)
        except (ValueError, TypeError):
            return default
    
    def show_template_tab(self):
        """Show template tab and hide receiver tab"""
        self.receiver_frame.grid_forget()
        self.template_frame.grid(row=1, column=0, sticky="nsew")
        
        # Update button styling
        self.template_button.configure(fg_color=["#3B8ED0", "#1F6AA5"], text_color=["#ffffff", "#ffffff"])
        self.receiver_button.configure(fg_color="transparent", text_color="white")
    
    def show_receiver_tab(self):
        """Show receiver tab and hide template tab"""
        self.template_frame.grid_forget()
        self.receiver_frame.grid(row=1, column=0, sticky="nsew")
        
        # Update button styling
        self.receiver_button.configure(fg_color=["#3B8ED0", "#1F6AA5"], text_color=["#ffffff", "#ffffff"])
        self.template_button.configure(fg_color="transparent", text_color="white") 