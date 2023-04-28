from fastapi import FastAPI
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
import os
from datetime import datetime
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

# Importing Connection String and Conatiner Name
conn_str = config['storageacc']['conn_str'][1:-1]
container = config['storageacc']['container'][1:-1]
blob_service_client = BlobServiceClient.from_connection_string(conn_str)

# Function for adding logs of commands into Log File
def addLog(cmmd, blob_name):
    if config.getboolean('settings', 'logOperations'):
        log_file_name = config['settings']['logFileName'][1:-1]
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
    if config.getboolean('permissions', 'allowUpload'):
        blob_name = loc.split("/")[-1]
        blob_client = blob_service_client.get_blob_client(container, blob=blob_name)
        with open(loc, "rb") as data:
            try:
                blob_client.upload_blob(data)
                status = "Uploaded {} successfully".format(blob_name)
                addLog("upload", blob_name)
            except ResourceExistsError:
                status = "Blob already exists"
    else :
        status = "Uploading Blobs Not Permitted"
    return {"status": status}

#  ----- Delete Blob from Storage -----
@app.get("/delete/{blob}")
async def deleteBlob(blob: str):
    if config.getboolean('permissions', 'allowDelete'):
        container_client = blob_service_client.get_container_client(container)
        try:
            container_client.delete_blob(blob)
            status = "Successfully Deleted Blob {}".format(blob)
            addLog("delete", blob)
        except ResourceNotFoundError:
            status = "Blob does not exist"
    else:
        status = "Deleting Blobs Not Permitted"
    return {"status": status}

#  ----- Download a Blob -----
@app.get("/download/{blob}")
async def downloadBlob(blob: str):
    if config.getboolean('permissions', 'allowDownload'):
        blob_client = blob_service_client.get_blob_client(container, blob=blob)
        downloads_path = config['settings']['downloadsPath'][1:-1]
        try:
            blob_data = blob_client.download_blob()
            file = open("{}{}".format(downloads_path, blob), "wb")
            file.write(blob_data.readall())
            status = "Successfully Downloaded Blob {}".format(blob)
            addLog("download", blob)
        except ResourceNotFoundError:
            status = "Blob does not exist"
    else:
        status = "Downloading Blobs Not Permitted"
    return {"status": status}

#  ----- Get List of Blobs in Storage -----
@app.get("/list")
async def listBlobs():
    list_blobs = []
    if config.getboolean('permissions', 'allowList'):
        container_client = blob_service_client.get_container_client(container)
        blobs = container_client.list_blobs()
        for blob in blobs:
            list_blobs.append({"Name": blob['name'], "Size": blob['size']})
        if len(list_blobs) == 0:
            list_blobs.append({"status": "No Blobs in Storage"})
        addLog("list", "")
    else:
        list_blobs.append({"status": "Generating List of Blobs Not Permitted"})
    return list_blobs