"""
Pipeline Multi-Cloud: Azure Blob Storage → Google BigQuery
Autor: MAEL1916
Proyecto 3 - Data Engineering
"""

import os
import io
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from google.cloud import bigquery
import pandas as pd

# Cargar variables de entorno
load_dotenv()

# Configuración Azure
AZURE_CONNECTION_STRING = os.getenv('AZURE_CONNECTION_STRING')
AZURE_CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME')

# Configuración BigQuery
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
BQ_DATASET_ID = os.getenv('BQ_DATASET_ID')
BQ_TABLE_ID = os.getenv('BQ_TABLE_ID')
BQ_LOCATION = os.getenv('BQ_LOCATION', 'us-central1')

def main():
    print("\n" + "="*60)
    print(" Pipeline Multi-Cloud: Azure Blob → Google BigQuery")
    print("="*60 + "\n")
    
    # Validar credenciales Azure
    if not AZURE_CONNECTION_STRING:
        print(" Error: AZURE_CONNECTION_STRING no configurado en .env")
        return
    
    # Validar configuración BigQuery
    if not all([GCP_PROJECT_ID, BQ_DATASET_ID, BQ_TABLE_ID]):
        print(" Error: Configuración de BigQuery incompleta en .env")
        return
    
    try:
        # 1. Conectar a Azure Blob Storage
        print(f" Conectando a Azure Blob Storage...")
        print(f"   Container: '{AZURE_CONTAINER_NAME}'")
        
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
        
        # 2. Listar archivos CSV en Azure
        print(f"\n Buscando archivos CSV...")
        
        blobs = [blob for blob in container_client.list_blobs() if blob.name.endswith('.csv')]
        
        if not blobs:
            print("  No se encontraron archivos CSV en el container")
            return
        
        print(f" Archivos CSV encontrados: {len(blobs)}\n")
        
        # 3. Conectar a BigQuery
        print(f" Conectando a BigQuery...")
        print(f"   Proyecto: {GCP_PROJECT_ID}")
        print(f"   Dataset: {BQ_DATASET_ID}")
        print(f"   Tabla: {BQ_TABLE_ID}\n")
        
        bq_client = bigquery.Client(project=GCP_PROJECT_ID, location=BQ_LOCATION)
        
        # 4. Procesar cada archivo CSV
        for idx, blob in enumerate(blobs, 1):
            print(f"[{idx}/{len(blobs)}]  Procesando: {blob.name}")
            
            try:
                # Descargar CSV desde Azure
                print(f"    ↓ Descargando desde Azure...")
                blob_client = container_client.get_blob_client(blob.name)
                blob_data = blob_client.download_blob().readall()
                
                # Convertir a DataFrame
                df = pd.read_csv(io.BytesIO(blob_data))
                print(f"     CSV leído: {len(df)} filas, {len(df.columns)} columnas")
                
                # Construir ID completo de la tabla
                table_id = f"{GCP_PROJECT_ID}.{BQ_DATASET_ID}.{BQ_TABLE_ID}"
                
                # Configurar job de carga
                job_config = bigquery.LoadJobConfig(
                    write_disposition="WRITE_TRUNCATE",  # Sobrescribir si existe
                    autodetect=True,  # Detectar esquema automáticamente
                )
                
                # Cargar a BigQuery
                print(f"    ↑ Cargando a BigQuery...")
                job = bq_client.load_table_from_dataframe(
                    df, 
                    table_id, 
                    job_config=job_config
                )
                
                # Esperar a que termine el job
                job.result()
                
                # Obtener info de la tabla
                table = bq_client.get_table(table_id)
                
                print(f"      Cargado exitosamente a BigQuery")
                print(f"       └─ Tabla: {table_id}")
                print(f"       └─ Filas totales: {table.num_rows}")
                print(f"       └─ Tamaño: {blob.size / 1024:.2f} KB\n")
                
            except Exception as e:
                print(f"     Error procesando {blob.name}: {str(e)}\n")
                continue
        
        print("="*60)
        print(" Pipeline completado exitosamente")
        print("="*60)
        
        # Validación final
        print(f"\n Validando datos en BigQuery...")
        query = f"""
            SELECT COUNT(*) as total_rows
            FROM `{GCP_PROJECT_ID}.{BQ_DATASET_ID}.{BQ_TABLE_ID}`
        """
        query_job = bq_client.query(query)
        results = query_job.result()
        
        for row in results:
            print(f" Filas totales en BigQuery: {row.total_rows}")
        
    except Exception as e:
        print(f"\n Error general: {str(e)}")
        raise

if __name__ == "__main__":
    main()