Azure Data Pipeline Implementation

This assignment demonstrates the implementation of an end-to-end data pipeline using Azure services.

A Resource Group and Storage Account were created, followed by Blob Containers for storing source and processed data. A CSV file was uploaded as the source dataset.

Azure Data Factory was used to create Linked Services and datasets connecting the storage account. A pipeline was built using Get Metadata and Copy Data activities to validate and transfer the data.

The pipeline was successfully executed, copying the file from the source container to the destination container. Monitoring tools were used to verify execution, and IAM roles (Reader and Contributor) were assigned to ensure proper access control.

This demonstrates a complete data movement pipeline in Azure.
