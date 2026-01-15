class Config:
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/gestion_concours_qcm'
    SQLALCHEMY_TRACK_MODIFICATIONS = False