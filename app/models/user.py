from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    """
    Modelo representativo de los usuarios en el sistema.
    Asociado a la tabla 'users'.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # Email único utilizado para la autenticación
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)

    # Relación uno-a-muchos con el modelo Task
    tasks = relationship("Task", back_populates="owner")
