import os
import json
import base64
import concurrent.futures
from pathlib import Path

def decode_base64_to_pdf(base64_data, output_path):
    """
    Decode base64 string to PDF file
    
    Args:
        base64_data (str): Base64 encoded PDF data
        output_path (str): Path where to save the PDF file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Decode base64 string to binary data
        pdf_data = base64.b64decode(base64_data)
        
        # Write binary data to file
        with open(output_path, 'wb') as pdf_file:
            pdf_file.write(pdf_data)
        
        return True
    except Exception as e:
        print(f"Error decoding base64 data: {str(e)}")
        return False

def process_json_file(json_file_path, pdf_folder):
    """
    Process a single JSON file to extract the base64 PDF and save it
    
    Args:
        json_file_path (str): Path to the JSON file
        pdf_folder (str): Folder to save the PDF file
    
    Returns:
        tuple: (filename, success, error_message)
    """
    try:
        filename = os.path.basename(json_file_path)
        pdf_filename = os.path.splitext(filename)[0] + ".pdf"
        pdf_path = os.path.join(pdf_folder, pdf_filename)
        
        # Read JSON file
        with open(json_file_path, 'r') as f:
            label_data = json.load(f)
        
        # Extract base64 PDF data
        base64_pdf = label_data.get("data", {}).get("label_pdf")
        
        if not base64_pdf:
            return (filename, False, "No label_pdf data found")
        
        # Decode and save PDF
        success = decode_base64_to_pdf(base64_pdf, pdf_path)
        
        if success:
            return (filename, True, pdf_path)
        else:
            return (filename, False, "Failed to decode or save PDF")
    
    except Exception as e:
        return (filename, False, str(e))

def convert_all_labels(generated_folder="generated", pdf_folder="pdfs"):
    """
    Convert all label JSON files in the generated folder to PDFs
    
    Args:
        generated_folder (str): Folder containing JSON label files
        pdf_folder (str): Folder to save the PDFs
    
    Returns:
        tuple: (success_count, total_count, errors)
    """
    # Create PDF folder if it doesn't exist
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
    
    # Get all JSON files in the generated folder
    json_files = [
        os.path.join(generated_folder, f) 
        for f in os.listdir(generated_folder) 
        if f.endswith(".json")
    ]
    
    if not json_files:
        return (0, 0, ["No JSON files found in the generated folder"])
    
    results = []
    errors = []
    
    # Use ThreadPoolExecutor for parallel processing
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(process_json_file, json_file, pdf_folder): json_file 
            for json_file in json_files
        }
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_file):
            filename, success, message = future.result()
            if success:
                results.append((filename, message))
            else:
                errors.append(f"{filename}: {message}")
    
    return (len(results), len(json_files), errors)
