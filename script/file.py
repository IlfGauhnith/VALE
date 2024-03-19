import shutil
import tempfile
import os
from flask import Flask
from decorator import log_function_name

@log_function_name
def copy_to_temp(app:Flask, original_file_path, new_file_name=None):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        file_name = new_file_name or os.path.basename(original_file_path)
        
        # Construct the destination path in the temporary directory
        temp_file_path = os.path.join(temp_dir, file_name)
        
        # Copy the file to the temporary location
        shutil.copy2(original_file_path, temp_file_path)
        
        app.logger.info(f"Arquivo criado em {temp_file_path}")
        
        # Return the path of the copied file in the temporary location
        return temp_file_path
    
    except Exception as e:
        app.logger.error("Error:", e)
        # Clean up: remove the temporary directory and its contents
        shutil.rmtree(temp_dir)
        raise