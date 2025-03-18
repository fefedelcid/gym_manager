from sqlmodel import SQLModel, Session, create_engine, select
from src.database.models import Cliente, Ficha, Movimiento
from src.utils import parse_date
from datetime import datetime

DATABASE_URL = "sqlite:///src/database/database.db"
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    """Inicializa la base de datos y crea las tablas si no existen."""
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")


def get_session():
    """Crea y retorna una nueva sesión de base de datos."""
    try:
        return Session(engine)
    except Exception as e:
        print(f"Error al crear la sesión: {e}")
        return None


class Database:
    def __init__(self):
        init_db()
        
    def add_client(self, cliente: Cliente, ficha: Ficha = None):
        """Agrega un cliente y opcionalmente su ficha médica."""
        try:
            with get_session() as session:
                session.add(cliente)
                session.commit()
                session.refresh(cliente)

                if ficha:
                    ficha.clientId = cliente.id
                    session.add(ficha)
                    session.commit()
                    session.refresh(ficha)
            return cliente
        except Exception as e:
            print(f"Error al agregar cliente: {e}")
            return None

    def get_client(self, document: str):
        """Obtiene un cliente por su documento."""
        try:
            with get_session() as session:
                statement = select(Cliente).where(Cliente.document == document)
                return session.exec(statement).first()
        except Exception as e:
            print(f"Error al obtener cliente por documento: {e}")
            return None

    def search_client(self, search_term: str):
        """Obtiene un cliente por documento, nombre o email."""
        try:
            with get_session() as session:
                # Filtramos por documento, nombre o email
                statement = select(Cliente).where(
                    Cliente.document.ilike(f"%{search_term}%") |  # Filtrar por documento
                    Cliente.fullName.ilike(f"%{search_term}%") |  # Filtrar por nombre
                    Cliente.email.ilike(f"%{search_term}%")  # Filtrar por email
                )
                return session.exec(statement).all()  # Retorna todos los resultados que coinciden
        except Exception as e:
            print(f"Error al obtener cliente: {e}")
            return None

    def get_client_by_id(self, clientId: int):
        """Obtiene un cliente por su ID."""
        try:
            with get_session() as session:
                return session.get(Cliente, clientId)
        except Exception as e:
            print(f"Error al obtener cliente por ID: {e}")
            return None

    def get_all_clients(self):
        """Obtiene todos los clientes."""
        try:
            with get_session() as session:
                statement = select(Cliente).order_by(Cliente.createdAt)
                return session.exec(statement).all()
        except Exception as e:
            print(f"Error al obtener todos los clientes: {e}")
            return []

    def add_payment(self, clientId: int, amount: float, date:datetime=None):
        """Registra un pago para un cliente y actualiza la fecha del último pago."""
        try:
            with get_session() as session:
                client = session.get(Cliente, clientId)
                if not client:
                    return None # Cliente no encontrado
                
                payment = Movimiento(clientId=clientId, amount=amount, createdAt=date)
                session.add(payment)
               
                # Actualizar la fecha del último pago
                lastPayment = client.lastPayment if client.lastPayment and client.lastPayment>date else date
                out = self.update_client(clientId, lastPayment=lastPayment)
                print(f"[INFO] Database.add_payment, update_client({clientId}, {lastPayment}), output: {out}")

                session.commit()
                session.refresh(payment)
                return payment
        except Exception as e:
            print(f"Error al agregar pago: {e}")
            return None
        
    def get_ficha(self, clientId:int):
        try:
            with get_session() as session:
                statement = select(Ficha).where(Ficha.clientId == clientId)
                return session.exec(statement).first()
        except Exception as e:
            print(f"Error al obtener ficha del cliente {clientId}: {e}")
            return None

    def get_payments(self, clientId: int):
        """Obtiene todos los pagos de un cliente."""
        try:
            with get_session() as session:
                statement = select(Movimiento).where(Movimiento.clientId == clientId)
                return session.exec(statement).all()
        except Exception as e:
            print(f"Error al obtener pagos del cliente {clientId}: {e}")
            return []

    def get_all_payments(self):
        """Obtiene todos los pagos."""
        try:
            with get_session() as session:
                statement = select(Movimiento).order_by(Movimiento.createdAt)
                return session.exec(statement).all()
        except Exception as e:
            print(f"Error al obtener todos los pagos: {e}")
            return []

    def update_client(self, clientId: int, **kwargs):
        """Actualiza los datos de un cliente."""
        try:
            with get_session() as session:
                client = session.get(Cliente, clientId)
                if not client:
                    return False # Cliente no encontrado
                
                for key, value in kwargs.items():
                    if hasattr(client, key):
                        if key in ['createdAt', 'lastPayment', 'birthDate']:
                            if key=='lastPayment' and value=='': value = None
                            else: value = parse_date(value)
                        setattr(client, key, value) # Modificar sólo atributos válidos

                if client.needCheck:
                    client.needCheck = 0

                session.commit()
                session.refresh(client)
                return client # Devolver cliente actualizado
        except Exception as e:
            print(f"Error al actualizar datos del cliente {clientId}: {e}")
            return None

    def update_ficha(self, clientId: int, **kwargs):
        """Actualiza los datos de la ficha médica del cliente."""
        try:
            with get_session() as session:
                statement = select(Ficha).where(Ficha.clientId == clientId)
                ficha = session.exec(statement).first()
                if not ficha:
                    return False # No hay ficha para este cliente
            
                for key, value in kwargs.items():
                    if hasattr(ficha, key):
                        setattr(ficha, key, value)
                    
                session.commit()
                session.refresh(ficha)
                return ficha # Devolver ficha actualizada
        except Exception as e:
            print(f"Error al actualizar ficha médica del cliente {clientId}: {e}")
            return None

    def delete_client(self, clientId: int):
        """Elimina un cliente junto con su ficha médica y pagos."""
        try:
            with get_session() as session:
                client = session.get(Cliente, clientId)
                if not client:
                    return False # Cliente no encontrado

                # Eliminar ficha médica si existe
                statement = select(Ficha).where(Ficha.clientId == clientId)
                ficha = session.exec(statement).first()
                if ficha:
                    session.delete(ficha)

                # Eliminar pagos del cliente
                statement = select(Movimiento).where(Movimiento.clientId == clientId)
                payments = session.exec(statement).all()
                for payment in payments:
                    session.delete(payment)

                # Eliminar cliente
                session.delete(client)
                session.commit()
                return True # Cliente eliminado correctamente
        except Exception as e:
            print(f"Error al eliminar cliente {clientId}: {e}")
            return False
        
if __name__=="__main__":
    init_db()