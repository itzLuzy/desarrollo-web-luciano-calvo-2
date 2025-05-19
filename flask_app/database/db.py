from sqlalchemy import create_engine, Column, BigInteger, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# --- Models ---

class Region(Base):
    __tablename__ = 'region'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre= Column(String(200), nullable=False)

class Comuna(Base):
    __tablename__ = 'comuna'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    region_id = Column(String(255),ForeignKey('region.id') ,nullable=False)

class Actividad(Base):
    __tablename__ = 'actividad'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    comuna_id = Column(BigInteger, ForeignKey('comuna.id'), nullable=False)
    nombre = Column(String(200), nullable=False)
    dia_hora_inicio = Column(DateTime, nullable=False)
    dia_hora_termino = Column(DateTime, nullable=False)
    sector = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=False)
    descripcion = Column(String(500), nullable=False)

class Foto(Base):
    __tablename__ = 'foto'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    actividad_id = Column(BigInteger, ForeignKey('actividad.id'), nullable=False)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)

contactos = ['whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra']
class ContactarPor(Base):
    __tablename__ = 'contactar_por'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    actividad_id = Column(BigInteger, ForeignKey('actividad.id'), nullable=False)
    nombre = Column(Enum(*contactos), nullable=False)
    identificador = Column(String(150), nullable=False)

temas = ['música', 'deporte', 'ciencias', 'religión', 'política', 'tecnología', 'juegos', 'baile', 'comida', 'otro']
class ActividadTema(Base):
    __tablename__ = 'actividad_tema'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    actividad_id = Column(BigInteger, ForeignKey('actividad.id'), nullable=False)
    tema = Column(Enum(*temas), nullable=False)
    glosa_otro = Column(String(15), nullable=True)

# --- Database Functions ---

def get_activity_by_id(activity_id):
    session = SessionLocal()
    activity = session.query(Actividad).filter_by(id=activity_id).first()
    session.close()
    return activity

def get_activities(page_size=5, offset=0):
    session = SessionLocal()
    activities = session.query(Actividad).limit(page_size).offset(offset).all()
    session.close()
    return activities

def count_activities():
    session = SessionLocal()
    count = session.query(Actividad).count()
    session.close()
    return count

def count_photos_by_activity(activity_id):
    session = SessionLocal()
    count = session.query(Foto).filter_by(actividad_id=activity_id).count()
    session.close()
    return count

def get_regions():
    session = SessionLocal()
    regions = session.query(Region).all()
    session.close()
    return regions

def get_comunas_by_region(region_id):
    session = SessionLocal()
    comunas = session.query(Comuna).filter_by(region_id=region_id).all()
    session.close()
    return comunas

def get_region_id_by_name(region_name):
    session = SessionLocal()
    region = session.query(Region).filter_by(nombre=region_name).first()
    session.close()
    return region.id if region else None

def get_comuna_id_by_name(comuna_name, region_id):
    session = SessionLocal()
    comuna = session.query(Comuna).filter_by(nombre=comuna_name, region_id=region_id).first()
    session.close()
    return comuna.id if comuna else None

def get_comuna_by_id(comuna_id):
    session = SessionLocal()
    comuna = session.query(Comuna).filter_by(id=comuna_id).first()
    session.close()
    return comuna

def get_activity_photos(activity_id):   
    session = SessionLocal()
    photos = session.query(Foto).filter_by(actividad_id=activity_id).all()
    session.close()
    return photos

def get_activity_contact_methods(activity_id):
    session = SessionLocal()
    contact_methods = session.query(ContactarPor).filter_by(actividad_id=activity_id).all()
    session.close()
    return contact_methods

def get_theme_by_activity(activity_id):
    session = SessionLocal()
    theme = session.query(ActividadTema).filter_by(actividad_id=activity_id).first()
    session.close()
    return theme

def get_activity_id_by_name(name):
    session = SessionLocal()
    activity = session.query(Actividad).filter_by(nombre=name).first()
    session.close()
    return activity.id if activity else None

def create_photo(activity_id, path, name):
    session = SessionLocal()
    new_photo = Foto(actividad_id=activity_id, ruta_archivo=path, nombre_archivo=name)
    session.add(new_photo)
    session.commit()
    session.close()

def create_activity(comuna_id, name, init_date, end_date, sector, email, celular, description):
    session = SessionLocal()
    new_activity = Actividad(
        comuna_id=comuna_id,
        nombre=name,
        dia_hora_inicio=init_date,
        dia_hora_termino=end_date,
        sector=sector,
        email=email,
        celular=celular,
        descripcion=description
    )
    session.add(new_activity)
    session.commit()
    session.close()

def create_photo(activity_id, path, name):
    session = SessionLocal()
    new_photo = Foto(actividad_id=activity_id, ruta_archivo=path, nombre_archivo=name)
    session.add(new_photo)
    session.commit()
    session.close()

def create_contact_method(activity_id, identifier, name):
    session = SessionLocal()
    new_contact_method = ContactarPor(actividad_id=activity_id, nombre=name, identificador=identifier)
    session.add(new_contact_method)
    session.commit()
    session.close()

def create_activity_theme(activity_id, tema, glosa_otro=None):
    session = SessionLocal()
    new_activity_theme = ActividadTema(actividad_id=activity_id, tema=tema, glosa_otro=glosa_otro)
    session.add(new_activity_theme)
    session.commit()
    session.close()