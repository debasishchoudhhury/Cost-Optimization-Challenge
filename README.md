# Cost-Optimization-Challenge

# Azure Billing Records Archival (Cosmos DB ➜ Blob)

This repo provides a serverless, cost-optimized solution for archiving old billing records from Azure Cosmos DB to Azure Blob Storage using **Azure Data Factory (ADF)** and **Azure DevOps (ADO)** pipeline automation.

## Components

### 1. Cosmos DB
- **`billing-records`**: Active container holding billing data.
- **`archive-tracker`**: New container to track archived record paths.

### 2. Azure Blob Storage
- Container: `billing-archive`
- Stores monthly Parquet or JSON files of archived billing data.
- Lifecycle policy to auto-tier or delete old blobs.

### 3. Azure Data Factory
- Pipeline: `ArchiveBillingRecords`
- Inputs: `startDate` and `endDate` from ADO
- Activities:
  - Read records from `billing-records` (filtered by date)
  - Write them to blob
  - Log blob path in `archive-tracker`
  - Delete original record

### 4. Azure DevOps Pipeline
- Scheduled monthly
- Powershell script calculates archival date range (e.g. 4–3 months ago)
- Triggers ADF pipeline with parameters


