from flask.ext.appbuilder import Model
from flask.ext.appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship

from . import db

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""


class FeatureTables(Model, AuditMixin):
    __tablename__ = 'feature_tables'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    features = relationship('Features', backref='feature_tables', lazy='dynamic')

    def __repr__(self):
        return self.name


registrations = db.Table('registrations',
                         Column('id', Integer, primary_key=True),
                         Column('features_id', Integer, ForeignKey('features.id')),
                         Column('mlmodels_id', Integer, ForeignKey('mlmodels.id')))
#
# class Registrations(Model):
#     __tablename__ = 'registrations'
#     Column('features_id', Integer, ForeignKey('features.id'))
#     Column('model_id', Integer, ForeignKey('mlmodels.id'))

class MlModels(Model, AuditMixin):
    __tablename__ = 'mlmodels'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # features_id = Column(String, ForeignKey('features.id'), nullable=False)

    def __repr__(self):
        return self.name


class Features(Model, AuditMixin):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    feature_tables_id = Column(String, ForeignKey('feature_tables.id'), nullable=False)
    filed_name = Column(String, default=name)
    feature_type = Column(String, nullable=False)
    statistical_caliber = Column(String)
    method_update = Column(String)
    is_valid = Column(Boolean, default=True)
    is_model_register = Column(Boolean, default=False)
    # describe_b = Column(String)

    # mlmodels = db.relationship('MlModels',
    #                         secondary='registrations',
    #                         backref='features',
    #                         lazy='dynamic')

    def __repr__(self):
        return self.name


class FeatureTypes(Model, AuditMixin):
    __tablename__ = 'feature_types'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    describe = Column(String)






