# azure-cloudapi v1.0.0

## A fully functional API to access Azure Storage Account in Python with ease!

This API is built to perform operations in an Azure Storage Account using python. You do not need to use the azure portal or need the connection string of storage account to access it.

Operations Provided:
- Upload Blobs to Container inside Storage.
- Delete Blobs from Container inside Storage.
- Download Blobs from Container inside Storage.
- List all Blobs present inside the Container in Storage.

# Features:
- Access Storage Account using code with ease, without repeating unnecessary steps.
- Generate Logs of all operations performed on the Storage with proper Date and Time of operation.
- Config File to change settings separately from main file.
- Enable/Disable operations inside config file.
- API built using FastAPI.

# How to use API
To use the CloudAPI, follow these steps:

1. Clone this project
2. Install necessary libraries - 
    - FastAPI - `pip install fastapi`
    - Uvicorn - `pip install "uvicorn[standard]"`
    - Azure Exceptions - `pip install azure-core`
    - Azure Storage - `pip install azure-storage-blob`
3. Add your Storage Account Connection String in config.ini in variable `conn_str` (Line 2)
4. Add your Container Name in config.ini in variable `container` (Line 3)
5. In terminal change directory to where main.py is present, execute command `uvicorn main:app --reload`

    Note: If error is thrown, try command `python -m uvicorn main:app --reload`
6. API is running, use URL `http://127.0.0.1:8000` to interact with API

# Changing Downloads Folder
Files downloaded are by default stored in `Downloads/`. 
Downloads directory can be changed by changing the `downloads_path` in main.py

Note: If you change the path, make sure following directory already exists to prevent errors 

# Changing Logs File
Operation Logs by default are stored in `CloudAPILogs.txt`. 
Log file name can be changed by chaning the variable `log_file_name`. 
You can also add log file into a directory by changeing name to `[directory_name]/[log_file_name].txt`.

Note: Make sure directory already exists in system to prevent error

# Command Examples

1. Uploading Blob -
    `http://127.0.0.1:8000/upload/C:/Users/Username/Downloads/data.csv`

2. Delete Blob - 
    `http://127.0.0.1:8000/delete/data.csv`

3. Download Blob - 
    `http://127.0.0.1:8000/download/data.csv`

4. Generate List of Blobs -
    `http://127.0.0.1:8000/list`

# Future Additions

- [x] Config File
- [ ] User Authentication
- [ ] Blob Name increment for blobs with same names
- [ ] FastAPI Documentation
- [ ] Storing Logs in Cloud
