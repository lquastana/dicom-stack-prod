import os
import time
from pydicom import dcmread
from pynetdicom import AE, evt
from pynetdicom.sop_class import (
    CTImageStorage,
    MRImageStorage,
    SecondaryCaptureImageStorage,
    UltrasoundImageStorage,
    XRayAngiographicImageStorage
)

# --- Configuration lue depuis les variables d'environnement ---
PACS_HOSTNAME = os.getenv('PACS_HOSTNAME', 'localhost')
PACS_PORT = int(os.getenv('PACS_PORT', 11112))
PACS_AETITLE = os.getenv('PACS_AETITLE', 'DICOOGLE')
SENDER_AETITLE = os.getenv('SENDER_AETITLE', 'CT_SCANNER')
DICOM_DIR = '/dicoms'

def handle_store_response(event):
    """Gère la réponse C-STORE du PACS."""
    status = event.response.Status
    if status == 0x0000:
        print(f"  -> C-STORE success for {event.request.AffectedSOPInstanceUID}")
    else:
        print(f"  -> C-STORE failed with status {status:04x} for {event.request.AffectedSOPInstanceUID}")

def send_dicom_files(pacs_host, pacs_port, pacs_aetitle, sender_aetitle, directory):
    """Scanne un répertoire et envoie tous les fichiers .dcm au PACS."""
    
    # LIGNE DE VÉRIFICATION
    print("--- V2 DU SCRIPT EN COURS D'EXECUTION ---")
    
    print("--- Démarrage du simulateur d'envoi DICOM ---")
    print(f"Configuration:")
    print(f"  - PACS Host: {pacs_host}")
    print(f"  - PACS Port: {pacs_port}")
    print(f"  - PACS AE Title: {pacs_aetitle}")
    print(f"  - Notre AE Title: {sender_aetitle}")
    print(f"  - Répertoire des fichiers: {directory}")
    print("-------------------------------------------------")
    
    ae = AE(ae_title=sender_aetitle)
    
    ae.add_requested_context(CTImageStorage)
    ae.add_requested_context(MRImageStorage)
    ae.add_requested_context(SecondaryCaptureImageStorage)
    ae.add_requested_context(UltrasoundImageStorage)
    ae.add_requested_context(XRayAngiographicImageStorage)

    handlers = [(evt.EVT_C_STORE, handle_store_response)]

    print(f"Tentative d'association avec le PACS {pacs_aetitle}@{pacs_host}:{pacs_port}")
    
    assoc = ae.associate(pacs_host, pacs_port, ae_title=pacs_aetitle, evt_handlers=handlers)

    if not assoc.is_established:
        print("L'association avec le PACS a échoué. Vérifiez la configuration et la connectivité.")
        return

    print("Association avec le PACS réussie.")
    file_count = 0
    
    try:
        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    dataset = dcmread(filepath)
                    
                    print(f"\nEnvoi du fichier: {filename} (SOP UID: {dataset.SOPInstanceUID})")
                    
                    response = assoc.send_c_store(dataset)

                    if response is None or response.Status != 0x0000:
                         print(f"Échec de l'envoi pour {filename}")
                    
                    file_count += 1

                except Exception as e:
                    print(f"Erreur lors du traitement de {filepath}: {e}")

    finally:
        assoc.release()
        print("\nAssociation avec le PACS terminée.")
        print(f"--- {file_count} fichier(s) traité(s). Fin du script. ---")


if __name__ == "__main__":
    send_dicom_files(PACS_HOSTNAME, PACS_PORT, PACS_AETITLE, SENDER_AETITLE, DICOM_DIR)