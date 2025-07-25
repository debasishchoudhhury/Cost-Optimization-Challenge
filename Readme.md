\# Azure Cosmos DB Archival Framework



This repository provides a \*\*cost-optimized archival strategy\*\* for Azure Cosmos DB billing records using Azure Data Factory, Azure Blob Storage, and Azure DevOps pipelines — \*\*without impacting existing APIs\*\*.



---



\## 🔍 Problem Statement



We have a serverless architecture where a Cosmos DB collection stores billing records. The system is \*\*read-heavy\*\*, but records older than 3 months are rarely accessed. As data grows, \*\*storage costs increase\*\*, even for rarely accessed records.



---



\## ✅ Solution Overview



We archive old records to \*\*Azure Blob Storage in Parquet format\*\*, while maintaining a reference to their location in a \*\*Cosmos DB `archive-tracker` container\*\*. Optional API fallback logic can fetch archived records on-demand.



---



\## 📐 Architecture Diagram



!\[Architecture Diagram](./docs/arch.png)



---



\## 🧩 Components



\### 🔁 Azure Data Factory (ADF)

\- `adf/ArchiveBillingRecords.json`: Main pipeline to copy filtered Cosmos DB records to Blob as Parquet

\- `adf/CosmosBillingInput.json`: Linked Service \& Dataset for Cosmos DB input

\- `adf/BlobParquetOutput.json`: Dataset definition for writing Parquet to Blob



\### ⚙️ Azure DevOps Pipeline

\- `ado/archive-billing.yml`: Monthly pipeline triggering the ADF archival job with dynamic date parameters



\### 🧠 Fallback Logic (Optional)

\- `scripts/api\_fallback\_example.py`: Shows how your API can fallback to Blob Storage if a record isn't found in Cosmos DB



---



\## 🗃️ Data Models



\### Cosmos DB: `billing-records` (active)

```json

{

&nbsp; "record\_id": "string",

&nbsp; "customer\_id": "string",

&nbsp; "amount": 123.45,

&nbsp; "timestamp": "2024-02-10T10:00:00Z"

}



