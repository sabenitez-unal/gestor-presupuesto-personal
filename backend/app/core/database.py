#Para inicializar la sesión y crear la conexión con la DB postgresql.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

engine = create_engine(settings.database_url)   # Para conectar la DB.
SessionLocal = sessionmaker(autoflush=False, bind=engine)   # Generador de sesiones para cada request.
Base = declarative_base()   # Todas las tablas heredan esta clase.
