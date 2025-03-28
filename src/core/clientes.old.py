from src.services import read_sheet, find_spreadsheet, get_google_sheets_service
from src.database import Database, Cliente, Ficha
from src.utils import parse_date, print_log
from src.config import SPREADSHEET_NAME, REGISTRADOS, NUEVOS


def sync_clients():
    # Conectar con Google Sheets
    sheet_id = find_spreadsheet(SPREADSHEET_NAME)
    sheet = get_google_sheets_service().spreadsheets()

    clientes_new = read_sheet(sheet_id, NUEVOS, sheet)
    clientes_old = read_sheet(sheet_id, REGISTRADOS, sheet)

    # Instancia de la base de datos
    db = Database()

    # Documentos ya registrados en la hoja secundaria
    registered_documents = {
        cliente[5].strip().replace('.', '') \
            for cliente in clientes_old[1:]
    }


    clientes_procesados = []
    filas_procesadas = []
    errores = []

    try:
        for idx, cliente in enumerate(clientes_new[1:], start=2):  # Saltar encabezado
            try:
                createdAt, email, fullName, birthDate, gender, document, phone,\
                address, goal, medicalHistory, medication, recentInjury,\
                emergencyContact, medicalCertificate, tyc, confirmation = cliente
            except Exception as e:
                error_msg = f"Error al desempaquetar datos en fila {idx}: {e}"
                print_log(f"❌ {error_msg}")
                errores.append((idx, error_msg))
                continue

            # Normalizar documento
            document = document.strip().replace('.', '')

            # Evitar duplicados
            if document in registered_documents or db.get_client(document):
                print_log(f"⚠️ Duplicado detectado en fila {idx}: {document}")
                continue

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
            except Exception as e:
                error_msg = f"Error al crear cliente y ficha, fila:{idx} exception:{e}"
                print_log(f"❌ {error_msg}")
                errores.append((idx, error_msg))
                continue

            # Registrar en la base de datos
            try:
                db.add_client(new_client, ficha)
                clientes_procesados.append(cliente)
                filas_procesadas.append(idx)
                print_log(f"✅ Cliente agregado con éxito: {fullName} ({document})")
                
            except Exception as e:
                error_msg = f"Error al insertar en DB, fila {idx}: {e}"
                print_log(f"❌ {error_msg}")
                errores.append((idx, error_msg))

    except Exception as e:
        print_log(f"Error general al procesar clientes: {e}")

    # Mover alumnos procesados a la hoja "Alumnos Registrados"
    if clientes_procesados:
        try:
            sheet.values().append(
                spreadsheetId=sheet_id,
                range=REGISTRADOS,
                valueInputOption="RAW",
                body={"values": clientes_procesados}
            ).execute()
            print_log(f"✅ {len(clientes_procesados)} clientes movidos a '{REGISTRADOS}'.")
        except Exception as e:
            print_log(f"❌ Error al mover datos a '{REGISTRADOS}': {e}")

    # Eliminar solo las filas procesadas en "NUEVOS"
    if filas_procesadas:
        try:
            # Invertir el orden para no desplazar índices al eliminar filas
            for idx in sorted(filas_procesadas, reverse=True):
                sheet.batchUpdate(
                    spreadsheetId=sheet_id,
                    body={
                        "requests": [{
                            "deleteDimension": {
                                "range": {
                                    "sheetId": NUEVOS,
                                    "dimension": "ROWS",
                                    "startIndex": idx - 1,  # Ajustar índice 0-based
                                    "endIndex": idx
                                }
                            }
                        }]
                    }
                ).execute()
            print_log(f"🗑️ {len(filas_procesadas)} filas eliminadas de '{NUEVOS}'.")
        except Exception as e:
            print_log(f"❌ Error al eliminar filas de '{NUEVOS}': {e}")

    # Registro final de errores
    if errores:
        print_log(f"⚠️ Errores encontrados: {len(errores)}")
        for idx, error in errores:
            print_log(f"   - Fila {idx}: {error}")


def sync_google_sheets():
    """Ejecuta la sincronización con Google Sheets."""
    try:
        print_log("🔄 Iniciando sincronización con Google Sheets...")
        sync_clients()
        print_log("✅ Sincronización completada.")
    except Exception as e:
        error_msg = f"❌ Error durante la sincronización: {e} {type(e)}"
        print_log(error_msg)


if __name__ == "__main__":
    sync_google_sheets()
