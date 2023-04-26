from fastapi import FastAPI
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
import os
from datetime import datetime

# Enter your azure storage account connection string
storage_conn_str = "[Your Storage Account Connection String]"
# Enter your container name
container = "[Storage Container Name]"

blob_service_client = BlobServiceClient.from_connection_string(storage_conn_str)

# Function for adding logs of commands into file CloudAPILogs.txt (can change name)
def addLog(cmmd, blob_name):
    log_file_name = "CloudAPILogs.txt" # Log File Name
    # You can also add log file into a directory by changeing name to "[directory_name]/[log_file_name].txt"
    # but make sure directory already exists in system to prevent error
    currTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    logfile = open(log_file_name, "a")
    match cmmd:
        case "upload": 
            logfile.write("{} => Uploaded Blob {}\n".format(currTime, blob_name))
        case "delete": 
            logfile.write("{} => Deleted Blob {}\n".format(currTime, blob_name))
        case "download": 
            logfile.write("{} => Downloaded Blob {}\n".format(currTime, blob_name))
        case "list": 
            logfile.write("{} => Generated list of Blobs\n".format(currTime))
    logfile.close()

# Creating a FastAPI Application
app = FastAPI(
    title="CloudAPI",
    version="0.1.1"
    )

# Default Message
@app.get("/", tags= ["Welcome"])
async def welcome():
    msg = {"message": "Welcome to AzureCloudAPI!"}
    return msg

#  ------ Upload Blob to Storage -----
@app.get("/upload/{loc:path}")
async def uploadBlob(loc: str):
    blob_name = loc.split("/")[-1]
    blob_client = blob_service_client.get_blob_client(container, blob=blob_name)
    with open(loc, "rb") as data:
        try:
                blob_client.upload_blob(data)
                status = "Uploaded {} successfully".format(blob_name)
                addLog("upload", blob_name)
        except ResourceExistsError:
             status = "Blob already exists"
    return {"status": status}

#  ----- Delete Blob from Storage -----
@app.get("/delete/{blob}")
async def deleteBlob(blob: str):
     container_client = blob_service_client.get_container_client(container)
     blobs = container_client.list_blobs()
     try:
            container_client.delete_blob(blob)
            status = "Successfully Deleted Blob {}".format(blob)
            addLog("delete", blob)
     except ResourceNotFoundError:
            status = "Blob does not exist"
     return status

#  ----- Download a Blob -----
@app.get("/download/{blob}")
async def downloadBlob(blob: str):
    blob_client = blob_service_client.get_blob_client(container, blob=blob)
    downloads_path = "Downloads/" # Path where blobs will be downloaded
    # If you change the path, make sure following directory already exists to prevent errors
    try:
        blob_data = blob_client.download_blob()
        file = open("{}{}".format(downloads_path, blob), "wb")
        file.write(blob_data.readall())
        status = "Successfully Downloaded Blob {}".format(blob)
        addLog("download", blob)
    except ResourceNotFoundError:
        status = "Blob does not exist"
    return {"status": status}

#  ----- Get List of Blobs in Storage -----
@app.get("/list")
async def listBlobs():
    list_blobs = []
    container_client = blob_service_client.get_container_client(container)
    blobs = container_client.list_blobs()
    for blob in blobs:
        list_blobs.append({"Name": blob['name'], "Size": blob['size']})
    if len(list_blobs) == 0:
             list_blobs.append({"status": "No Blobs in Storage"})
    addLog("list", "")
    return list_blobs