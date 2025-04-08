from src.services import read_sheet, find_spreadsheet, get_google_sheets_service
from src.database import Database, Cliente, Ficha
from src.utils import parse_date, print_log
from src.config import SPREADSHEET_NAME, REGISTRADOS, NUEVOS

def delete_records(records, sheet, spreadsheetId, _from=NUEVOS):
    try:
        sheets_props = sheet.get(spreadsheetId=spreadsheetId, \
                                 fields="sheets(properties(sheetId,title))")\
                                .execute()["sheets"]
        sheetId = None
        for prop in sheets_props:
            if prop['properties']["title"]==_from:
                sheetId = prop['properties']["sheetId"]
                break
            
        # Invertir el orden para no desplazar índices al eliminar filas
        for idx in sorted(records, reverse=True):
            sheet.batchUpdate(
                spreadsheetId=spreadsheetId,
                body={
                    "requests": [{
                        "deleteDimension": {
                            "range": {
                                "sheetId": sheetId,
                                "dimension": "ROWS",
                                "startIndex": idx - 1,  # Ajustar índice 0-based
                                "endIndex": idx
                            }
                        }
                    }]
                }
            ).execute()
        print_log(f"[INFO] {len(records)} filas eliminadas de '{_from}'.")
    except Exception as e:
        print_log(f"[ERROR] al eliminar filas de '{_from}': {e}")


def move_clients(clients, spreadsheetId, sheet):
    try:
        sheet.values().append(
            spreadsheetId=spreadsheetId,
            range=REGISTRADOS,
            valueInputOption="RAW",
            body={"values": clients}
        ).execute()
        print_log(f"[INFO] {len(clients)} clientes movidos de '{NUEVOS}' a '{REGISTRADOS}'.")
    except Exception as e:
        print_log(f"[ERROR] al mover datos de '{NUEVOS}' a '{REGISTRADOS}': {e}")
    

def process_client(cliente, idx):
    try:
        if len(cliente)==16:
            createdAt, email, fullName, birthDate, gender, document, phone,\
            address, goal, medicalHistory, medication, recentInjury,\
            emergencyContact, medicalCertificate, _, _ = cliente
        elif len(cliente)==14:
            createdAt, email, fullName, birthDate, gender, document, phone,\
            address, goal, medicalHistory, medication, recentInjury,\
            emergencyContact, medicalCertificate = cliente
        elif len(cliente)==13:
            createdAt, email, fullName, birthDate, gender, document, phone,\
            address, goal, medicalHistory, medication, recentInjury,\
            emergencyContact = cliente
            medicalCertificate = ""
    except Exception as e:
        error_msg = f"[ERROR] al desempaquetar datos en fila {idx}: {e}"
        print_log(f"{error_msg}")
        return None, None, None

    # Normalizar documento
    document = document.strip().replace('.', '')

    try:
        # Crear cliente y ficha
        new_client = Cliente(
            fullName=fullName,
            document=document,
            email=email,
            phone=phone,
            birthDate=parse_date(birthDate),
            gender=gender,
            address=address,
            goal=goal,
            createdAt=parse_date(createdAt),
            needCheck=True
        )

        ficha = Ficha(
            clientId=None,
            medicalHistory=medicalHistory,
            medication=medication,
            recentInjury=recentInjury,
            emergencyContact=emergencyContact,
            medicalCertificate=medicalCertificate
        )

        return new_client, ficha, document
    except Exception as e:
        error_msg = f"[ERROR] al crear cliente y ficha, fila {idx}: {e}"
        print_log(f"{error_msg}")
        return None, None, None


def sync_clients():
    # Conectar con Google Sheets
    spreadsheetId = find_spreadsheet(SPREADSHEET_NAME)
    sheet = get_google_sheets_service().spreadsheets()

    clientes_new = read_sheet(spreadsheetId, NUEVOS, sheet)
    clientes_old = read_sheet(spreadsheetId, REGISTRADOS, sheet)

    # Instancia de la base de datos
    db = Database()

    try:
        # Documentos ya registrados en la hoja secundaria
        registered_documents = {
            cliente[5].strip().replace('.', '') for cliente in clientes_old[1:]
        } # <- set()

        # Documentos de la nase de datos
        clients = db.get_all_clients()
        db_documents = {
            cliente.document for cliente in clients
        } # <- set()

        # Documentos nuevos
        new_documents = {
            cliente[5].strip().replace('.', '') for cliente in clientes_new[1:]
        }

        registered_not_in_db = registered_documents - db_documents
        new_not_registered = new_documents - registered_not_in_db
    except Exception as e:
        print_log("[ERROR] Excepción inesperada al obtener diferencias.")
        print_log("[INFO] Abortando.")
        return None
    
    primera_ocurrencia = {}
    duplicados = []
    clientes_procesados = []
    filas_procesadas = []

    # Proceso alumnos nuevos
    print_log("[INFO] Procesando alumnos nuevos...")
    for idx, cliente in enumerate(clientes_new[1:], start=2):
        client, ficha, document = process_client(cliente, idx)
        if not client:
            continue

        if document in new_not_registered: # No añadidos a la bd
            # Registrar en la base de datos
            try:
                db.add_client(document, ficha)
                print_log(f"[INFO] Cliente agregado con éxito: ({document})")
            except Exception as e:
                error_msg = f"[ERROR] al insertar en DB, fila {idx}: {type(e)}"
                print_log(f"{error_msg}")

        clientes_procesados.append(cliente)
        filas_procesadas.append(idx)

    # Procesar alumnos viejos
    print_log("[INFO] Procesando alumnos registrados...")
    for idx, cliente in enumerate(clientes_old[1:], start=2):
        client, ficha, document = process_client(cliente, idx)
        if not client:
            continue

        if document not in primera_ocurrencia.keys():
            primera_ocurrencia[document] = idx
            if document in registered_not_in_db: # No añadidos a la bd
                # Registrar en la base de datos
                try:
                    if db.add_client(client, ficha):
                        print_log(f"[INFO] Cliente agregado con éxito: ({document})")
                    else: raise Exception
                except Exception as e:
                    error_msg = f"[ERROR] al insertar en DB, fila {idx}: {e}, type:{type(e)}"
                    print_log(f"{error_msg}")
        else:
            error_msg = f"⚠️ Duplicado detectado en fila {idx}: {document}"
            print_log(error_msg)
            duplicados.append(idx)

    print_log("[INFO] Modificando hojas...")
    move_clients(clientes_procesados, spreadsheetId, sheet)
    delete_records(filas_procesadas, sheet, spreadsheetId)
    print_log(f"[INFO] Eliminando duplicados ({len(duplicados)})...")
    delete_records(duplicados, sheet, spreadsheetId, _from=REGISTRADOS)


def sync_google_sheets():
    """Ejecuta la sincronización con Google Sheets."""
    try:
        print_log("[INFO] Iniciando sincronización con Google Sheets...")
        sync_clients()
        print_log("[INFO] Sincronización completada.")
    except Exception as e:
        error_msg = f"[ERROR] durante la sincronización: {e} {type(e)}"
        print_log(error_msg)


if __name__ == "__main__":
    sync_google_sheets()
