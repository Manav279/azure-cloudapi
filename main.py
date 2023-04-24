from fastapi import FastAPI
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError

# Enter your azure storage account connection string
storage_conn_str = "[Your Storage Account Connection String]"
# Enter your container name
container = "[Storage Container Name]"

blob_service_client = BlobServiceClient.from_connection_string(storage_conn_str)

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

#  ------ Upload File to Storage -----
@app.get("/upload/{loc:path}")
async def upload_file(loc: str):
    file_name = loc.split("/")[-1]
    blob_client = blob_service_client.get_blob_client(container, blob=file_name)
    with open(loc, "rb") as data:
        try:
                blob_client.upload_blob(data)
                status = "Uploaded {} successfully".format(file_name)
        except ResourceExistsError:
             status = "File already exists"
    return {"status": status}

#  ----- Delete File from Storage -----
@app.get("/delete/{blob}")
async def delete_file(blob: str):
     container_client = blob_service_client.get_container_client(container)
     blobs = container_client.list_blobs()
     try:
            container_client.delete_blob(blob)
            status = "Successfully Deleted Blob {}".format(blob)
     except ResourceNotFoundError:
            status = "File does not exist"
     return status