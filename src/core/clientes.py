from src.services import read_sheet, find_spreadsheet, get_google_sheets_service
from src.database import Database, Cliente, Ficha
from src.utils import parse_date

def sync_clients():
    # Configuración
    SPREADSHEET_NAME = "Formulario de Inscripción (Respuestas)"
    REGISTRADOS = "Alumnos Registrados"
    NUEVOS = "Respuestas de formulario 1"

    # Conectar con Google Sheets
    sheet_id = find_spreadsheet(SPREADSHEET_NAME)
    sheet = get_google_sheets_service().spreadsheets()

    clientes_new = read_sheet(sheet_id, NUEVOS, sheet)
    clientes_old = read_sheet(sheet_id, REGISTRADOS, sheet)

    # Instancia de la base de datos
    db = Database()

    # Documentos ya registrados en la base de datos y en la hoja secundaria
    # El índice 5 hace referencia al documento
    registered_documents = {cliente[5].strip().replace('.', '') for cliente in clientes_old[1:]}

    clientes_procesados = []
    try:
        for cliente in clientes_new[1:]:
            try:
                createdAt, email, fullName, birthDate, gender, document, phone,\
                address, goal, medicalHistory, medication, recentInjury,\
                emergencyContact, medicalCertificate, tyc, confirmation = cliente
            except Exception as e:
                print(f"❌ Error al registrar: {cliente}, error={e}")
                continue
            
            # Convertir fechas
            createdAt = parse_date(createdAt)
            birthDate = parse_date(birthDate)

            # Normalizar documento
            document = document.strip().replace('.', '')

            # Evitar duplicados
            if document in registered_documents or db.get_client(document):
                continue # Saltar si ya existe

            # Crear cliente
            new_client = Cliente(
                fullName=fullName,
                document=document,
                email=email,
                phone=phone,
                birthDate=birthDate,
                gender=gender,
                address=address,
                goal=goal,
                createdAt=createdAt,
                needCheck=True # Nuevo alumno necesita verificación
            )

            ficha = Ficha(
                clientId=None,
                medicalHistory=medicalHistory,
                medication=medication,
                recentInjury=recentInjury,
                emergencyContact=emergencyContact,
                medicalCertificate=medicalCertificate
            )

            # Registrar en la base de datos
            db.add_client(new_client, ficha)
            clientes_procesados.append(cliente)
    except Exception as e:
        print(f"Error al procesar alumnos: {e}")

    # Mover alumnos procesados a la hoja "Alumnos Registrados"
    # y eliminarlos de "Respuestas de formulario 1"
    if len(clientes_procesados)>0:
        sheet.values().append(
            spreadsheetId=sheet_id,
            range=REGISTRADOS,
            valueInputOption="RAW",
            body={"values": clientes_procesados}
        ).execute()

        for cliente in clientes_procesados:
            sheet.values().clear(
                spreadsheetId=sheet_id,
                range=NUEVOS
            ).execute()

    # Confirmar que los alumnos de "Alumnos Registrados" estén en la base de datos
    try:
        for idx, cliente in enumerate(clientes_old[1:]):
            try:
                createdAt, email, fullName, birthDate, gender, document, phone,\
                address, goal, medicalHistory, medication, recentInjury,\
                emergencyContact, medicalCertificate = cliente
            except ValueError:
                createdAt = cliente[0]
                email = cliente[1]
                fullName = cliente[2]
                birthDate = cliente[3]
                gender = cliente[4]
                document = cliente[5]
                phone = cliente[6]
                address = cliente[7]
                goal = cliente[8]
                medicalHistory = cliente[9]
                medication = cliente[10]
                recentInjury = cliente[11]
                emergencyContact = cliente[12]
                medicalCertificate = ""
            except Exception as e:
                raise e
            
            createdAt = parse_date(createdAt)
            birthDate = parse_date(birthDate)
            print(f"[{idx}] Cliente.birthDate: {birthDate} type:{type(birthDate)}, Cliente.createdAt: {createdAt} type:{type(createdAt)}")

            # Normalizar documento
            document = document.strip().replace('.', '')

            if not db.get_client(document):
                cliente = Cliente(
                    fullName=fullName,
                    document=document,
                    email=email,
                    phone=phone,
                    birthDate=birthDate,
                    gender=gender,
                    address=address,
                    goal=goal,
                    createdAt=createdAt,
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
                db.add_client(cliente, ficha)
                print(f"[INFO] Cliente añadido: {document}")
    except Exception as e:
        print(f"Error al corroborar datos: {e}")