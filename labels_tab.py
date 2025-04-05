import customtkinter as ctk
import os
import json
import uuid
import requests
from dotenv import load_dotenv
from shipaway import url, create_label

# Load environment variables from .env file
load_dotenv()

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
                                                 values=["USPS Priority", "USPS Express"])
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
        self.receiver_title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")
        
        # Template selection section
        self.template_selection_frame = ctk.CTkFrame(self.receiver_frame)
        self.template_selection_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        
        self.template_selection_label = ctk.CTkLabel(self.template_selection_frame, text="Select Template:")
        self.template_selection_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        # Get list of template files
        self.templates = self.get_template_files()
        
        # Template dropdown
        self.template_dropdown = ctk.CTkOptionMenu(self.template_selection_frame, 
                                                values=self.templates,
                                                command=self.load_selected_template)
        self.template_dropdown.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        
        # Refresh button
        self.refresh_button = ctk.CTkButton(self.template_selection_frame, text="Refresh", 
                                          command=self.refresh_templates,
                                          width=100)
        self.refresh_button.grid(row=0, column=2, padx=20, pady=10)
        
        self.receiver_content = ctk.CTkLabel(self.receiver_frame, text="Enter receiver details for your shipping labels.")
        self.receiver_content.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # Create scrollable frame for recipient fields
        self.receiver_scrollable_frame = ctk.CTkScrollableFrame(self.receiver_frame, width=700, height=400)
        self.receiver_scrollable_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.receiver_frame.grid_rowconfigure(3, weight=1)
        self.receiver_frame.grid_columnconfigure(0, weight=1)
        
        # Recipient fields
        current_row = 0
        
        # Recipient Name
        self.recipient_name_label = ctk.CTkLabel(self.receiver_scrollable_frame, text="Name:")
        self.recipient_name_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.recipient_name_entry = ctk.CTkEntry(self.receiver_scrollable_frame, width=200)
        self.recipient_name_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        current_row += 1
        
        # Recipient Address Line 1
        self.recipient_address1_label = ctk.CTkLabel(self.receiver_scrollable_frame, text="Address Line 1:")
        self.recipient_address1_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.recipient_address1_entry = ctk.CTkEntry(self.receiver_scrollable_frame, width=200)
        self.recipient_address1_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        current_row += 1
        
        # Recipient Address Line 2
        self.recipient_address2_label = ctk.CTkLabel(self.receiver_scrollable_frame, text="Address Line 2:")
        self.recipient_address2_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.recipient_address2_entry = ctk.CTkEntry(self.receiver_scrollable_frame, width=200)
        self.recipient_address2_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        current_row += 1
        
        # Recipient City
        self.recipient_city_label = ctk.CTkLabel(self.receiver_scrollable_frame, text="City:")
        self.recipient_city_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.recipient_city_entry = ctk.CTkEntry(self.receiver_scrollable_frame, width=200)
        self.recipient_city_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        current_row += 1
        
        # Recipient State
        self.recipient_state_label = ctk.CTkLabel(self.receiver_scrollable_frame, text="State:")
        self.recipient_state_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.recipient_state_entry = ctk.CTkEntry(self.receiver_scrollable_frame, width=200)
        self.recipient_state_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        current_row += 1
        
        # Recipient Postal Code
        self.recipient_postal_code_label = ctk.CTkLabel(self.receiver_scrollable_frame, text="Postal Code:")
        self.recipient_postal_code_label.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.recipient_postal_code_entry = ctk.CTkEntry(self.receiver_scrollable_frame, width=200)
        self.recipient_postal_code_entry.grid(row=current_row, column=1, padx=20, pady=(10, 0), sticky="w")
        current_row += 1
        
        # Order Label button
        self.order_label_button = ctk.CTkButton(self.receiver_frame, text="Order Label", command=self.order_label)
        self.order_label_button.grid(row=4, column=0, columnspan=2, padx=20, pady=(20, 10))
        
        # Status message
        self.receiver_status_label = ctk.CTkLabel(self.receiver_frame, text="")
        self.receiver_status_label.grid(row=5, column=0, columnspan=2, padx=20, pady=(0, 20))
    
    def get_template_files(self):
        """Get a list of JSON template files in the templates folder"""
        templates = ["Select a template"]
        
        # Check if templates folder exists
        if os.path.exists("templates"):
            # Get all JSON files in the templates folder
            for file in os.listdir("templates"):
                if file.endswith(".json"):
                    # Display friendly name (replace underscores with spaces, remove .json)
                    friendly_name = file.replace("_", " ").replace(".json", "")
                    templates.append(friendly_name)
        
        return templates
    
    def refresh_templates(self):
        """Refresh the list of templates in the dropdown"""
        # Get updated list of templates
        templates = self.get_template_files()
        
        # Update dropdown values
        self.template_dropdown.configure(values=templates)
        
        # Select first item
        if templates:
            self.template_dropdown.set(templates[0])
        
        self.receiver_status_label.configure(text="Template list refreshed", text_color="green")
    
    def load_selected_template(self, selected_template):
        """Load the selected template data"""
        if selected_template == "Select a template":
            return
            
        # Convert display name to filename
        filename = selected_template.replace(" ", "_") + ".json"
        file_path = os.path.join("templates", filename)
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    template_data = json.load(file)
                self.receiver_status_label.configure(text=f"Template '{selected_template}' loaded", text_color="green")
                # Future: Pre-fill sender info or other template data as needed
            except Exception as e:
                self.receiver_status_label.configure(text=f"Error loading template: {str(e)}", text_color="red")
        else:
            self.receiver_status_label.configure(text=f"Template file not found", text_color="red")
    
    def order_label(self):
        """Order a shipping label using the shipaway API"""
        # Check if a template is selected
        selected_template = self.template_dropdown.get()
        if selected_template == "Select a template":
            self.receiver_status_label.configure(text="Please select a template first", text_color="red")
            return
        
        # Get recipient information
        recipient_name = self.recipient_name_entry.get().strip()
        recipient_address1 = self.recipient_address1_entry.get().strip()
        recipient_city = self.recipient_city_entry.get().strip()
        recipient_state = self.recipient_state_entry.get().strip()
        recipient_postal_code = self.recipient_postal_code_entry.get().strip()
        
        # Basic validation
        if not recipient_name or not recipient_address1 or not recipient_city or not recipient_state or not recipient_postal_code:
            self.receiver_status_label.configure(text="Please fill in all required recipient fields", text_color="red")
            return
        
        try:
            # Load template data
            template_filename = selected_template.replace(" ", "_") + ".json"
            template_path = os.path.join("templates", template_filename)
            
            with open(template_path, 'r') as file:
                template_data = json.load(file)
            
            # Update recipient information
            template_data["recipient"]["name"] = recipient_name
            template_data["recipient"]["address1"] = recipient_address1
            template_data["recipient"]["address2"] = self.recipient_address2_entry.get().strip()
            template_data["recipient"]["city"] = recipient_city
            template_data["recipient"]["state"] = recipient_state
            template_data["recipient"]["postal_code"] = recipient_postal_code
            
            # Send request to API
            self.receiver_status_label.configure(text="Sending request to API...", text_color="blue")
            
            success, response = create_label(template_data)
            
            # Handle response
            if success:
                # Create generated folder if it doesn't exist
                if not os.path.exists("generated"):
                    os.makedirs("generated")
                
                # Save response to file
                timestamp = uuid.uuid4()
                response_filename = f"label_{timestamp}.json"
                response_path = os.path.join("generated", response_filename)
                
                with open(response_path, 'w') as file:
                    json.dump(response, file, indent=2)
                
                self.receiver_status_label.configure(
                    text=f"Label ordered successfully! Response saved to {response_filename}", 
                    text_color="green"
                )
            else:
                self.receiver_status_label.configure(
                    text=response, 
                    text_color="red"
                )
        
        except Exception as e:
            self.receiver_status_label.configure(text=f"Error: {str(e)}", text_color="red")
    
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
            "uuid": os.getenv("UUID"),
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