from flask.ext.appbuilder import Model
from flask.ext.appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship

from . import db


class FeatureSourceType(Model, AuditMixin):
    __tablename__ = 'feature_source_type'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    username = Column(String)
    password = Column(String)
    uri = Column(String)
    feature_source = relationship('FeatureSource', backref='feature_source_type', lazy='dynamic')

    def test_connection(self):
        pass

    def __repr__(self):
        return self.name


class FeatureSource(Model, AuditMixin):
    __tablename__ = 'feature_source'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    feature_source_type_id = Column(Integer, ForeignKey('feature_source_type.id'), nullable=False)
    features = relationship('Features', backref='feature_source', lazy='dynamic')


    def __repr__(self):
        return self.name


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
    feature_source_id = Column(String, ForeignKey('feature_source.id'), nullable=False)
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
