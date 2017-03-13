from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.profile import Base


POSTGRES_DB_URL = 'postgresql://samscott123:123456@localhost:5432/users'
# MYSQL_DB_URL = 'mysql+pymysql://samscott123:123456@localhost:3306/users'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './UPLOADED'

#engine = create_engine(MYSQL_DB_URL, echo=True)
engine = create_engine(POSTGRES_DB_URL, echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
