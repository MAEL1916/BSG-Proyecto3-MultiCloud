# Proyecto 3: Pipeline Multi-Cloud (Azure Blob Storage → Google BigQuery)

**Autor:** Elias Martinez  
**Curso:** Data Engineering - BSG 2026  

## Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Arquitectura](#arquitectura)
3. [Justificación Técnica](#justificación-técnica-cambio-de-aws-redshift-a-gcp-bigquery)
4. [Prerequisitos](#prerequisitos)
5. [Configuración Paso a Paso](#configuración-paso-a-paso)
   - [Paso 1: Azure Blob Storage](#paso-1-configurar-azure-blob-storage)
   - [Paso 2: Google Cloud Platform](#paso-2-configurar-google-cloud-platform-gcp)
   - [Paso 3: Configuración Local](#paso-3-configuración-local)
   - [Paso 4: Ejecutar Pipeline](#paso-4-ejecutar-el-pipeline)
   - [Paso 5: Validación](#paso-5-validación-de-datos)
6. [Troubleshooting](#troubleshooting)
7. [Estructura del Proyecto](#estructura-del-proyecto)

---

## Descripción del Proyecto

Este proyecto implementa un **pipeline de datos multi-cloud** que transfiere datos desde **Azure Blob Storage** hacia **Google BigQuery** utilizando Python.

**Dataset:** Spotify Wrapped 2025 - Top 50 Artistas Globales (50 registros, 11 columnas)

---

## Arquitectura

![Arquitectura del Pipeline](docs/screenshots/diagrama-flujo-proyecto3.jpg)

**Componentes:**
- **Origen:** Azure Blob Storage (Container: `source-data`)
- **Procesamiento:** Python 3.13 + Pandas
- **Destino:** Google BigQuery (Dataset: `proyecto3_dw`)
- **Librerías:** 
  - `azure-storage-blob` (conexión a Azure)
  - `google-cloud-bigquery` (conexión a BigQuery)
  - `pandas` (transformación de datos)
  - `python-dotenv` (gestión de credenciales)

---

## Justificación Técnica: Cambio de AWS Redshift a GCP BigQuery

**Problema encontrado:**
- Amazon Redshift Serverless requiere habilitación manual de la cuenta AWS que no se completó a tiempo
- Error: "Account opt-in required for Redshift Serverless"

**Solución implementada:**
- Se cambió el destino a **Google BigQuery**
- El proyecto mantiene el objetivo: **Data Warehouse analítico en la nube**
- La arquitectura sigue siendo **Multi-Cloud** (Azure + GCP)

**Ventajas de BigQuery:**
- Serverless nativo (sin configuración de infraestructura)
- Auto-escalable
- Pricing por consulta (pay-as-you-go)
- Integración nativa con Python SDK
- No requiere aprovisionamiento de clusters

---

## Prerequisitos

### Software necesario:

| Software | Versión mínima | Instalación |
|----------|----------------|-------------|
| Python | 3.8+ | [python.org](https://www.python.org/downloads/) |
| pip | 20.0+ | Incluido con Python |
| Google Cloud SDK | Última | [cloud.google.com/sdk](https://cloud.google.com/sdk/docs/install) |
| Git | 2.0+ | [git-scm.com](https://git-scm.com/downloads) |

### Cuentas requeridas:
- Cuenta de **Microsoft Azure** (con suscripción activa)
- Cuenta de **Google Cloud Platform** (con proyecto creado)
- Cuenta de **GitHub** (para clonar repositorio)

### Verificar instalaciones:

**Mac/Linux:**
```bash
python3 --version
pip3 --version
gcloud --version
git --version
Windows:

cmd
python --version
pip --version
gcloud --version
git --version
Configuración Paso a Paso

PASO 1: Configurar Azure Blob Storage

1.1 Crear Storage Account

Ve a Azure Portal
Busca "Storage accounts" en la barra de búsqueda
Clic en "+ Create"
Completa el formulario:
Resource group: Crea uno nuevo o usa existente
Storage account name: tu nombre único
Region: East US
Performance: Standard
Redundancy: LRS (Locally-redundant storage)
Clic en "Review + create" → "Create"
Capturas de referencia:

![Azure Portal Home](docs/screenshots/azure-console.png)

![Storage Accounts List](docs/screenshots/storage-accounts.png)

![Storage Account Details](docs/screenshots/detalles-storage-account.png)

1.2 Crear Container

Dentro de tu Storage Account, ve a "Containers" (menú izquierdo)
Clic en "+ Container"
Nombre: source-data
Public access level: Private
Clic en "Create"
Capturas de referencia:

![Containers List](docs/screenshots/container.png)

Vista detallada del container creado:

![Container Detail](docs/screenshots/container-detail.png)

1.3 Subir archivo CSV

Entra al container source-data
Clic en "Upload"
Selecciona el archivo spotify_wrapped_2025_top50_artists.csv (ubicado en data/)
Clic en "Upload"
Captura de referencia:

![CSV en Blob Storage](docs/screenshots/source-data-azure.png)

1.4 Obtener Connection String

En tu Storage Account, ve a "Access keys" (menú izquierdo)
Clic en "Show keys"
Copia el "Connection string" de key1
GUÁRDALO (lo necesitarás para el archivo .env)
PASO 2: Configurar Google Cloud Platform (GCP)

2.1 Crear Proyecto GCP

Ve a Google Cloud Console
Clic en el selector de proyectos (arriba)
Clic en "New Project"
Nombre del proyecto: tu nombre único
Clic en "Create"
Capturas de referencia:

![GCP Console Home](docs/screenshots/gcp-console.png)

![Crear Proyecto GCP](docs/screenshots/gcp-crear-proyecto.png)

Confirmación del proyecto creado:

![Crear Proyecto GCP - Confirmación](docs/screenshots/crear-proyecto-gcp-1.png)

![Proyecto Seleccionado](docs/screenshots/proyecto-consola-gcp.png)

2.2 Habilitar BigQuery API

Menú hamburguesa (☰) → "APIs & Services" → "Enabled APIs & services"
Clic en "+ Enable APIs and Services"
Busca: BigQuery API
Clic en "Enable"
Captura de referencia:

![Menú GCP](docs/screenshots/menu-gcp.png)

2.3 Crear Dataset en BigQuery

Opción A: Desde la consola web

Menú hamburguesa (☰) → "BigQuery"
En el explorador (panel izquierdo), clic en tu proyecto
Clic en los 3 puntos → "Create dataset"
Completa:
Dataset ID: proyecto3_dw
Location: us-central1
Default table expiration: Never
Clic en "Create dataset"
Opción B: Desde Terminal (recomendado)

bash
bq mk --dataset --location=us-central1 PROYECTO_ID:proyecto3_dw
Nota: Reemplaza PROYECTO_ID con tu ID de proyecto GCP.

Capturas de referencia:

![BigQuery Workspace](docs/screenshots/bigquery-gcp.png)

![Dataset Details](docs/screenshots/dataset-bigquery.png)

2.4 Configurar autenticación con gcloud

Mac/Linux:

bash
# Autenticarse en GCP
gcloud auth login

# Configurar credenciales para Python SDK
gcloud auth application-default login

# Establecer proyecto por defecto
gcloud config set project PROYECTO_ID

# Establecer proyecto de cuotas
gcloud auth application-default set-quota-project PROYECTO_ID
Windows:

cmd
gcloud auth login
gcloud auth application-default login
gcloud config set project PROYECTO_ID
gcloud auth application-default set-quota-project PROYECTO_ID
Nota: Reemplaza PROYECTO_ID con tu ID de proyecto (ej: proyecto3-mael-1916)

Capturas de referencia:

![Terminal gcloud auth](docs/screenshots/gcp-terminal.png)

![Terminal set project](docs/screenshots/gcp-project-configure.png)

2.5 Crear Service Account (Opcional)

Menú hamburguesa (☰) → "IAM & Admin" → "Service Accounts"
Clic en "+ Create Service Account"
Completa:
Service account name: bigquery-loader-proyecto3
Description: Service account para cargar datos a BigQuery
Clic en "Create and Continue"
Asigna roles:
BigQuery Data Editor
BigQuery Job User
Clic en "Done"
Capturas de referencia:

![IAM Service Accounts](docs/screenshots/iam-cuentas-servicios.png)

![Service Account Details](docs/screenshots/proyecto3-loader.png)

PASO 3: Configuración Local

3.1 Clonar repositorio

Mac/Linux:

bash
cd ~/Desktop
git clone https://github.com/MAEL1916/BSG-Proyecto3-MultiCloud.git
cd BSG-Proyecto3-MultiCloud
Windows:

cmd
cd %USERPROFILE%\Desktop
git clone https://github.com/MAEL1916/BSG-Proyecto3-MultiCloud.git
cd BSG-Proyecto3-MultiCloud
3.2 Crear archivo .env

Copiar archivo de ejemplo:

Mac/Linux:

bash
cp .env.example .env
Windows:

cmd
copy .env.example .env
Abrir .env en tu editor:

Mac:

bash
open -a "Visual Studio Code" .env
Windows:

cmd
code .env
Completar con tus credenciales:

env
# Azure Blob Storage
AZURE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=TU_STORAGE_ACCOUNT;AccountKey=TU_ACCOUNT_KEY;EndpointSuffix=core.windows.net
AZURE_CONTAINER_NAME=source-data

# GCP BigQuery Configuration
GCP_PROJECT_ID=tu-proyecto-gcp
BQ_DATASET_ID=proyecto3_dw
BQ_TABLE_ID=spotify_wrapped_2025_top50_artists
BQ_LOCATION=us-central1
IMPORTANTE:

Reemplaza TU_STORAGE_ACCOUNT con el nombre de tu storage account de Azure
Reemplaza TU_ACCOUNT_KEY con el Access Key que copiaste en el Paso 1.4
Reemplaza tu-proyecto-gcp con tu Project ID de GCP
3.3 Instalar dependencias

Mac/Linux:

bash
pip3 install -r requirements.txt
Windows:

cmd
pip install -r requirements.txt
Capturas de referencia:

![Instalación de requirements](docs/screenshots/install-requirements.png)

Verificación de librerías de GCP instaladas:

![Requirements GCP Instalados](docs/screenshots/requirements-gcp.png)

Output esperado:

Code
Successfully installed:
  - azure-storage-blob-12.28.0
  - google-cloud-bigquery-3.25.0
  - pandas-2.2.0
  - python-dotenv-1.0.0
PASO 4: Ejecutar el Pipeline

4.1 Verificar configuración

Mac/Linux:

bash
ls -la
cat .env
Windows:

cmd
dir
type .env
Asegúrate de que:

Existe el archivo azure_to_bigquery.py
El archivo .env tiene todas las credenciales
La carpeta data/ contiene el CSV
4.2 Ejecutar el script

Mac/Linux:

bash
python3 azure_to_bigquery.py
Windows:

cmd
python azure_to_bigquery.py
Captura de referencia:

![Ejecución del script](docs/screenshots/script-azure-gcp.png)

Output esperado:

Code
════════════════════════════════════════════════
 Pipeline Multi-Cloud: Azure Blob → Google BigQuery
════════════════════════════════════════════════

 Conectando a Azure Blob Storage...
   Container: 'source-data'

 Buscando archivos CSV...
 Archivos CSV encontrados: 1

 Conectando a BigQuery...
   Proyecto: proyecto3-mael-1916
   Dataset: proyecto3_dw
   Tabla: spotify_wrapped_2025_top50_artists

[1/1]  Procesando: spotify_wrapped_2025_top50_artists.csv
    ↓ Descargando desde Azure...
     CSV leído: 50 filas, 11 columnas
    ↑ Cargando a BigQuery...
     Cargado exitosamente a BigQuery
       └─ Tabla: proyecto3-mael-1916.proyecto3_dw.spotify_wrapped_2025_top50_artists
       └─ Filas totales: 50
       └─ Tamaño: 4.96 KB

 Validando datos en BigQuery...
 Filas totales en BigQuery: 50
PASO 5: Validación de Datos

5.1 Verificar tabla en BigQuery Console

Ve a BigQuery Console
En el explorador (panel izquierdo), expande tu proyecto
Expande el dataset proyecto3_dw
Clic en la tabla spotify_wrapped_2025_top50_artists
Verás el esquema y preview de datos
Captura de referencia:

![BigQuery Tabla Preview](docs/screenshots/bigquery-spotify-wrapped.png)

5.2 Ejecutar queries de validación

Query 1: Contar filas totales

SQL
SELECT COUNT(*) as total_filas
FROM `PROYECTO_ID.proyecto3_dw.spotify_wrapped_2025_top50_artists`;
Resultado esperado: 50

Captura de referencia:

![Query Count](docs/screenshots/count-sql-gcp.png)

Query 2: Ver Top 10 artistas

SQL
SELECT *
FROM `PROYECTO_ID.proyecto3_dw.spotify_wrapped_2025_top50_artists`
ORDER BY wrapped_2025_rank
LIMIT 10;
Captura de referencia:

![Query Top 10](docs/screenshots/query-top10-gcp.png)

Query 3: Top 5 artistas por oyentes

SQL
SELECT 
    wrapped_2025_rank,
    artist_name,
    monthly_listeners_millions_mar2026,
    primary_genre,
    country
FROM `PROYECTO_ID.proyecto3_dw.spotify_wrapped_2025_top50_artists`
ORDER BY monthly_listeners_millions_mar2026 DESC
LIMIT 5;
Resultado esperado:

Rank	Artist	Listeners (M)	Genre	Country
1	The Weeknd	110.4	Pop	Canada
2	Taylor Swift	107.5	Pop	USA
Nota: Más queries disponibles en: sql/queries_validacion.sql

Troubleshooting

Error: "No module named 'azure'"

Solución:

bash
pip3 install azure-storage-blob
Error: "403 BigQuery API has not been used in project"

Causa: BigQuery API no está habilitada o estás usando el proyecto incorrecto.

Solución:

bash
# Verificar proyecto actual
gcloud config get-value project

# Cambiar proyecto
gcloud config set project TU_PROYECTO_ID

# Establecer quota project
gcloud auth application-default set-quota-project TU_PROYECTO_ID

# Habilitar BigQuery API
gcloud services enable bigquery.googleapis.com
Error: "DefaultCredentialsError: Could not automatically determine credentials"

Causa: No has autenticado con gcloud.

Solución:

bash
gcloud auth application-default login
Error: "BlobNotFound" en Azure

Causa: El archivo CSV no está en el container o el nombre es incorrecto.

Solución:

Verifica que el archivo existe en Azure Portal
Verifica el nombre del container en tu .env
Verifica el Connection String
Error: "Dataset not found"

Causa: El dataset no existe en BigQuery.

Solución:

bash
bq mk --dataset --location=us-central1 TU_PROYECTO_ID:proyecto3_dw
El script no encuentra el archivo .env

Causa: Estás ejecutando el script desde otra carpeta.

Solución:

bash
# Verificar que estás en la carpeta correcta
pwd

# Ir a la carpeta del proyecto
cd ~/Desktop/BSG_modulo6/Proyecto3

# Ejecutar script
python3 azure_to_bigquery.py
Estructura del Proyecto

Code
Proyecto3/
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
├── azure_to_bigquery.py
├── data/
│   └── spotify_wrapped_2025_top50_artists.csv
├── docs/
│   └── screenshots/
│       ├── azure-console.png
│       ├── storage-accounts.png
│       ├── detalles-storage-account.png
│       ├── container.png
│       ├── container-detail.png
│       ├── source-data-azure.png
│       ├── gcp-console.png
│       ├── gcp-crear-proyecto.png
│       ├── crear-proyecto-gcp-1.png
│       ├── proyecto-consola-gcp.png
│       ├── menu-gcp.png
│       ├── bigquery-gcp.png
│       ├── dataset-bigquery.png
│       ├── gcp-terminal.png
│       ├── gcp-project-configure.png
│       ├── iam-cuentas-servicios.png
│       ├── proyecto3-loader.png
│       ├── install-requirements.png
│       ├── requirements-gcp.png
│       ├── script-azure-gcp.png
│       ├── bigquery-spotify-wrapped.png
│       ├── count-sql-gcp.png
│       ├── query-top10-gcp.png
│       └── diagrama-flujo-proyecto3.jpg
└── sql/
    └── queries_validacion.sql
Conclusiones

Este proyecto demuestra la implementación exitosa de un pipeline multi-cloud que:

Integra servicios de Azure y Google Cloud Platform
Automatiza la transferencia de datos entre nubes
Utiliza tecnologías modernas de procesamiento de datos
Implementa mejores prácticas de seguridad (credenciales en .env)
Proporciona validación completa de datos cargados
Tecnologías dominadas:

Azure Blob Storage
Google BigQuery
Python 3.13
Pandas
Google Cloud SDK

