# DICOM Stack Prod

This project deploys a complete, production-ready DICOM ecosystem using Docker Compose. It includes a Dicoogle PACS server, the OHIF v3 web viewer, and a simulator to send DICOM files.

## ✨ Components

  - **PACS Server**: [Dicoogle](https://www.dicoogle.com/) - An open-source, extensible PACS server.
  - **DICOM Viewer**: [OHIF Viewer v3](https://ohif.org/) - A modern and configurable web-based viewer.
  - **Simulator**: A custom Python service using `pynetdicom` to simulate sending files from a medical modality (e.g., a CT scanner).

## 🚀 Quick Start

### Prerequisites

  - [Docker](https://www.docker.com/get-started)
  - [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1.  **Clone this repository:**

    ```bash
    git clone <YOUR_REPO_URL>
    cd dicom-stack-prod
    ```

2.  **Set up the environment:**
    Create a `.env` file in the root directory. You can copy the contents from the project description. The default values should work without modification.

3.  **Add sample DICOM files:**
    Download some sample DICOM files and place them inside the `dicom-sender/sample-dicoms/` directory.
    You can find public datasets here:

      - [The Cancer Imaging Archive (TCIA)](https://www.cancerimagingarchive.net/)
      - [Visible Human Project](https://www.nlm.nih.gov/research/visible/visible_human.html)

4.  **Launch the ecosystem:**

    ```bash
    docker-compose up -d --build
    ```

    *(The `--build` flag is important on the first run to build the `dicom-sender` image).*

### Accessing Services

  - **OHIF Viewer**: Open your browser and navigate to [http://localhost:3002](https://www.google.com/search?q=http://localhost:3002)
  - **Dicoogle Web Interface**: Open your browser and navigate to [http://localhost:8080](https://www.google.com/search?q=http://localhost:8080)

### Usage

On startup (`docker-compose up`), the `dicom-sender` service will wait for 20 seconds, then automatically send all DICOM files from the `dicom-sender/sample-dicoms/` directory to Dicoogle.

You can check the logs to see the process:

```bash
docker-compose logs -f dicom-sender
```

Once the files are sent, they will appear in the study list on OHIF and within the Dicoogle web interface.

## 🔧 Scalability and Production

This project is designed with "prod-ready" principles in mind:

  - **Externalized Configuration**: All configuration is managed in the `.env` file.
  - **Data Persistence**: The `dicoogle_data` volume ensures that your DICOM data is not lost when the container restarts.
  - **Isolated Network**: Services communicate over a private Docker network (`dicom_net`).

For scaling up to a larger deployment:

  - **Database**: Dicoogle can be configured to use an external database (PostgreSQL, MySQL). You could add a database service to the `docker-compose.yml` file or connect to a managed service (like AWS RDS).
  - **Storage**: For very large volumes, DICOM storage could be offloaded to a distributed file system or an object storage provider (like S3), depending on available Dicoogle plugins.
  - **High Availability**: Use an orchestrator like Kubernetes with replicas for stateless services (OHIF) and a StatefulSet for Dicoogle.
  - **Reverse Proxy**: In a production environment, it is essential to place this stack behind a reverse proxy (like Nginx, Traefik, or Caddy) to handle SSL/TLS (HTTPS) and routing.

## 🤝 Contributing

Feel free to check `CONTRIBUTING.md` for more details on how to contribute to this project.

## License

This project is licensed under the MIT License.