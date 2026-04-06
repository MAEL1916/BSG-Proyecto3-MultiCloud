"""
Script para transferir archivos de Azure Blob Storage a AWS S3
Proyecto 3 - Pipeline de datos multi-cloud
"""

import os
from azure.storage.blob import BlobServiceClient
import boto3
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración desde .env
AZURE_CONNECTION_STRING = os.getenv('AZURE_CONNECTION_STRING')
AZURE_CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_PREFIX = os.getenv('S3_PREFIX', 'raw/')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')


def transfer_blobs_to_s3():
    """
    Transfiere todos los archivos de Azure Blob Storage a AWS S3
    """
    print("=" * 60)
    print(" Iniciando transferencia Azure Blob → AWS S3")
    print("=" * 60)
    
    # Cliente Azure
    print(f"\n Conectando a Azure container: '{AZURE_CONTAINER_NAME}'...")
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
    
    # Cliente AWS S3
    print(f"  Conectando a AWS S3 bucket: '{S3_BUCKET_NAME}' (región: {AWS_REGION})...\n")
    s3_client = boto3.client('s3', region_name=AWS_REGION)
    
    # Listar blobs
    blobs = list(container_client.list_blobs())
    
    if not blobs:
        print("  No se encontraron archivos en Azure.")
        return
    
    print(f" Archivos encontrados: {len(blobs)}\n")
    
    # Procesar cada blob
    for idx, blob in enumerate(blobs, 1):
        print(f"[{idx}/{len(blobs)}]  Procesando: {blob.name}")
        
        try:
            # Descargar de Azure
            blob_client = container_client.get_blob_client(blob.name)
            blob_data = blob_client.download_blob().readall()
            
            # Subir a S3
            s3_key = f"{S3_PREFIX}{blob.name}"
            s3_client.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=s3_key,
                Body=blob_data
            )
            
            print(f"          Subido a: s3://{S3_BUCKET_NAME}/{s3_key}")
            print(f"          Tamaño: {len(blob_data) / 1024:.2f} KB\n")
            
        except Exception as e:
            print(f"          Error: {str(e)}\n")


if __name__ == "__main__":
    # Validar que existan las variables de entorno
    if not AZURE_CONNECTION_STRING:
        print(" Error: AZURE_CONNECTION_STRING no está configurado en .env")
        exit(1)
    
    transfer_blobs_to_s3()