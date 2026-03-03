# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    @classmethod
    def get_list(cls):
        return cls.query.all()

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return

# ==========================
# QCM MODELS
# ==========================

class QCM(db.Model):

    __tablename__ = 'qcms'

    id            = db.Column(db.Integer, primary_key=True)
    title         = db.Column(db.String(200), nullable=False)
    description   = db.Column(db.Text, nullable=True)

    date_created  = db.Column(db.DateTime, default=dt.datetime.utcnow)
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    # relation
    questions = relationship("Question", backref="qcm", cascade="all, delete", lazy=True)

    def __init__(self, **kwargs):
        super(QCM, self).__init__(**kwargs)

    def __repr__(self):
        return f"QCM: {self.title}"

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise InvalidUsage(str(e), 422)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise InvalidUsage(str(e), 422)


class Question(db.Model):

    __tablename__ = 'questions'

    id      = db.Column(db.Integer, primary_key=True)
    text    = db.Column(db.Text, nullable=False)

    qcm_id  = db.Column(db.Integer, db.ForeignKey('qcms.id'), nullable=False)

    choices = relationship("Choice", backref="question", cascade="all, delete", lazy=True)

    def __repr__(self):
        return f"Question: {self.text[:30]}"


class Choice(db.Model):

    __tablename__ = 'choices'

    id           = db.Column(db.Integer, primary_key=True)
    text         = db.Column(db.String(300), nullable=False)
    is_correct   = db.Column(db.Boolean, default=False)

    question_id  = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)

    def __repr__(self):
        return f"Choice: {self.text}"