from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from datetime import datetime

Base = declarative_base()

class Tarea(Base):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True)
    descripcion = Column(String, nullable=False)
    completada = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Tarea(id={self.id}, descripcion='{self.descripcion}', completada={self.completada})>"

DATABASE_URL = "sqlite:///tareas.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)