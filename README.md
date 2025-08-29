# DICOM Stack Prod

This project deploys a complete open-source DICOM ecosystem using Docker Compose. It bundles an Orthanc PACS server, the OHIF v3 web viewer, and a Python-based simulator that sends sample DICOM files to the PACS.

## ✨ Components

- **PACS Server**: [Orthanc](https://www.orthanc-server.com/) with DICOMweb enabled.
- **DICOM Viewer**: [OHIF Viewer v3](https://ohif.org/) configured to query Orthanc over DICOMweb.
- **Simulator**: A Python service using `pynetdicom` to emulate a modality sending files.

## 🚀 Quick Start

### Prérequis

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. **Cloner le dépôt :**
   ```bash
   git clone <YOUR_REPO_URL>
   cd dicom-stack-prod
   ```
2. **Ajouter des fichiers DICOM :**
   Placez vos fichiers DICOM dans le dossier `dicom-sender/sample-dicoms/`.
3. **Lancer la stack :**
   ```bash
   docker-compose up -d --build
   ```
   *(Le flag `--build` est nécessaire lors du premier lancement pour construire l'image du sender.)*

### Accès aux services

- **OHIF Viewer** : [http://localhost:3001](http://localhost:3001)
- **Orthanc Explorer** : [http://localhost:8042](http://localhost:8042)

### Utilisation

Au démarrage (`docker-compose up`), le service `dicom-sender` attend 25 secondes puis envoie automatiquement tous les fichiers DICOM du répertoire `dicom-sender/sample-dicoms/` vers Orthanc. Les études reçues apparaîtront ensuite dans Orthanc Explorer et dans OHIF.

## License

Ce projet est sous licence MIT.
