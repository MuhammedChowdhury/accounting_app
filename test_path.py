import os

def list_templates(folder_name):
    """
    Lists the contents of the specified folder, including subdirectories and files,
    with absolute paths. Handles errors gracefully.
    """
    try:
        # Get absolute path of the folder
        folder_path = os.path.abspath(folder_name)
        print(f"Absolute Path of '{folder_name}': {folder_path}")
        
        # Check if the folder exists
        if not os.path.exists(folder_path):
            print(f"The folder '{folder_name}' does not exist.")
            return
        
        # List all files and subdirectories
        print(f"Contents of '{folder_name}':")
        for root, dirs, files in os.walk(folder_path):
            print(f"\nRoot: {root}")
            for dir_name in dirs:
                print(f"  Directory: {dir_name}")
            for file_name in files:
                print(f"  File: {file_name}")
                
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the folder to inspect
folder_to_check = 'templates'

# Call the function
list_templates(folder_to_check)
