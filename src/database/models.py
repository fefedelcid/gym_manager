from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import List, Optional


class Cliente(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    fullName: str
    document: str = Field(unique=True)
    email: Optional[str] = Field(default=None, unique=True)
    phone: Optional[str] = Field(default=None)
    birthDate: datetime
    gender: str
    address: str
    goal: str
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    lastPayment: Optional[datetime] = Field(default=None)
    needCheck: bool = Field(default=False)

    # Relaciones
    ficha: Optional["Ficha"] = Relationship(back_populates="cliente", sa_relationship_kwargs={"uselist":False})
    movimientos: List["Movimiento"] = Relationship(back_populates="cliente")


class Ficha(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    clientId: int = Field(foreign_key="cliente.id")
    medicalHistory: Optional[str] = Field(default=None)
    medication: Optional[str] = Field(default=None)
    recentInjury: Optional[str] = Field(default=None)
    emergencyContact: Optional[str] = Field(default=None)
    medicalCertificate: Optional[str] = Field(default=None)

    # Relaciones
    cliente: Cliente = Relationship(back_populates="ficha")


class Movimiento(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    clientId: int = Field(foreign_key="cliente.id")
    amount: float
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relaciones
    cliente: Cliente = Relationship(back_populates="movimientos")