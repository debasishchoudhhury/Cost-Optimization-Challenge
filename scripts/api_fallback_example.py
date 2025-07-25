import requests
import json
from azure.storage.blob import BlobServiceClient
import pyarrow.parquet as pq
import pyarrow as pa
from io import BytesIO

# === CONFIG ===
COSMOS_DB_API_URL = "https://your-api-endpoint.com/billing-records"
AZURE_BLOB_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net"
BLOB_CONTAINER_NAME = "billing-archive"

# === Function to call existing Cosmos DB API ===
def get_record_from_cosmos(record_id):
    response = requests.get(f"{COSMOS_DB_API_URL}/{record_id}")
    if response.status_code == 200:
        return response.json()
    return None

# === Function to check archive tracker ===
def lookup_archive_metadata(record_id):
    # Mocked lookup (in production, query archive-tracker container in Cosmos DB)
    return {
        "blob_path": "billing-archive/2024/02/batch-01.parquet"
    }

# === Function to load from Blob Parquet file ===
def get_record_from_blob(record_id, blob_path):
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_BLOB_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=blob_path)
    
    download_stream = blob_client.download_blob().readall()
    parquet_file = pq.ParquetFile(BytesIO(download_stream))
    
    for batch in parquet_file.iter_batches():
        table = pa.Table.from_batches([batch])
        for row in table.to_pylist():
            if row.get("record_id") == record_id:
                return row
    return None

# === API fallback flow ===
def get_billing_record(record_id):
    # 1. Try Cosmos DB
    record = get_record_from_cosmos(record_id)
    if record:
        print("Found in Cosmos DB")
        return record

    # 2. Look up archived blob path
    metadata = lookup_archive_metadata(record_id)
    blob_path = metadata.get("blob_path")

    # 3. Fetch from Blob
    archived_record = get_record_from_blob(record_id, blob_path)
    if archived_record:
        print(" Found in Blob Archive")
        return archived_record

    print(" Record not found anywhere.")
    return None

# === Example usage ===
if __name__ == "__main__":
    record_id = "example-record-id-1234"
    record = get_billing_record(record_id)
    print(json.dumps(record, indent=2) if record else "No record found.")
