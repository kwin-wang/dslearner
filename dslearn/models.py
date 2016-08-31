import logging
from flask.ext.appbuilder import Model
from flask.ext.appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, MetaData, create_engine, Text
from sqlalchemy.orm import relationship

from . import db
from . import utils as utils


class FeatureSourceType(Model, AuditMixin):
    __tablename__ = 'feature_source_type'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    username = Column(String)
    password = Column(String)
    uri = Column(String)
    feature_source = relationship('FeatureSource', backref='feature_source_type', lazy='dynamic')
    is_db = Column(Boolean, default=True)
    is_file = Column(Boolean, default=False)

    def test_connection(self):
        if self.is_db:
            try:
                eng = self.get_sqla_engine()
                eng.connection()
                return True
            except Exception as e:
                logging.exception(e)
                return False

    def get_sqla_engine(self):
        return create_engine(self.uri)

    def get_table(self, table_name, schema=None):
        """
        get table object if feature source type is sqla (database)
        :return:
        """
        meta = MetaData()
        return Table(
            table_name,
            meta,
            schema=schema or None,
            autoload=True,
            autoload_with=self.get_sqla_engine())

    def get_columns(self, Table_name, schema):
        table = self.get_table(table_name, schema)
        return table.columns.keys()

    def __repr__(self):
        return self.name


class FeatureSource(Model, AuditMixin):
    __tablename__ = 'feature_source'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    feature_source_type_id = Column(Integer,
                                    ForeignKey('feature_source_type.id'),
                                    nullable=False)
    features = relationship('Features', backref='feature_source', lazy='dynamic')
    # table_columns_id = Column(String, ForeignKey('table_columns.id'))
    table_columns = relationship('TableColumns', back_populates='feature_source')
    schema = Column(String)

    def fetch_table_metadata(self):
        table = self.feature_source_type.get_table(self.name)
        """Fetches the metadata for the table and merges it in"""
        try:
            table = self.feature_source_type.get_table(self.name, schema=self.schema)
        except Exception as e:
            flasher(str(e))
            flasher(
                "Table doesn't seem to exist in the specified database, "
                "couldn't fetch column information", "danger")
            return

        TC = TableColumns  # noqa shortcut to class
        for col in table.columns:
            try:
                datatype = "{}".format(col.type).upper()
            except Exception as e:
                datatype = "UNKNOWN"
                logging.error(
                    "Unrecognized data type in {}.{}".format(table, col.name))
                logging.exception(e)
            print('>>>>>>>>')
            print(type(TC.feature_source))
            print(type(self))
            dbcol = (
                db.session
                .query(TC)
                .filter(TC.feature_source == self)
                .filter(TC.column_name == col.name)
                .first()
            )
            db.session.flush()
            if not dbcol:
                dbcol = TableColumns(column_name=col.name, type=datatype)
                dbcol.is_dttm = dbcol.is_time

            db.session.merge(self)
            self.table_columns.append(dbcol)
            db.session.commit()

    def fetch_file_metadata(self):
        pass

    def __repr__(self):
        return self.name


class TableColumns(Model, AuditMixin):
    __tablename__ = 'table_columns'
    id = Column(Integer, primary_key=True)
    column_name = Column(String, nullable=False, unique=True)
    is_dttm = Column(Boolean, default=False)
    is_feature = Column(Boolean, default=True)
    type = Column(String, default='')
    description = Column(Text, default='')
    feature_source_id = Column(Integer, ForeignKey('feature_source.id') )
    feature_source = relationship('FeatureSource', back_populates='table_columns')

    num_types = ('DOUBLE', 'FLOAT', 'INT', 'BIGINT', 'LONG')
    date_types = ('DATE', 'TIME')
    str_types = ('VARCHAR', 'STRING', 'CHAR')

    @property
    def isnum(self):
        return any([t in self.type.upper() for t in self.num_types])

    @property
    def is_time(self):
        return any([t in self.type.upper() for t in self.date_types])

    @property
    def is_string(self):
        return any([t in self.type.upper() for t in self.str_types])


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
    feature_source_id = Column(Integer, ForeignKey('feature_source.id'), nullable=False)
    filed_name = Column(String, default=name)
    statistical_caliber = Column(String)
    method_update = Column(String)
    is_valid = Column(Boolean, default=True)
    is_model_register = Column(Boolean, default=False)
    feature_types_id = Column(Integer, ForeignKey('feature_types.id'), nullable=False)
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
    features = relationship('Features', backref='feature_types', lazy='dynamic')

    def __repr__(self):
        return self.name
