# -*- coding: utf-8
import logging
from flask import render_template
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder import ModelView, CompactCRUDMixin
from . import appbuilder, db
from . import models
from . import utils as utils


class FeatureTypesModelView(ModelView):
    datamodel = SQLAInterface(models.FeatureTypes)
    exclude_cols = ['changed_by', 'changed_on', 'created_by', 'created_on']
    add_exclude_columns = exclude_cols
    edit_columns = exclude_cols


class FeaturesModelView(ModelView):
    datamodel = SQLAInterface(models.Features)
    search_columns = ["name", "filed_name"]
    exclude_cols = ['changed_by', 'changed_on', 'created_by', 'created_on']
    columns = ['name', 'filed_name', 'feature_type', 'statistical_caliber',
           'method_update', 'is_valid']

    edit_cols = ['name', 'feature_types', 'feature_source', 'filed_name', 'statistical_caliber',
       'method_update', 'is_valid', 'is_model_register']
    list_columns = columns
    # edit_columns = columns
    # add_columns = columns
    edit_columns = edit_cols
    add_columns = edit_cols


class TableColumnsModelView(ModelView, CompactCRUDMixin):
    can_delete = False
    datamodel = SQLAInterface(models.TableColumns)
    add_columns = ['column_name', 'type', 'is_feature', 'is_dttm','description']
    edit_form = add_columns
    list_columns = add_columns
    show_columns = add_columns
    name = 'hello'

appbuilder.add_view_no_menu(TableColumnsModelView)


class FeatureSourceModelView(ModelView):
    datamodel = SQLAInterface(models.FeatureSource)
    list_columns = ['name', 'feature_source_type']
    edit_columns = ["name"]
    add_columns = ["name", 'feature_source_type']
    related_views = [FeaturesModelView, TableColumnsModelView]

    def post_add(self, table):
        try:
            table.fetch_table_metadata()
        except Exception as e:
            logging.exception(e)
            utils.flasher('Table not exists!')

    def post_update(self, table):
        self.post_add(table)





class FeatureSourceTypeModelView(ModelView):
    datamodel = SQLAInterface(models.FeatureSourceType)
    exclude_cols = ['changed_by', 'changed_on', 'created_by', 'created_on', 'feature_source']
    edit_exclude_columns = exclude_cols
    add_exclude_columns = exclude_cols
    label_columns = {'src_tp': 'source type'}
    list_columns = ['name', 'username', 'password', 'uri']
    order_columns = ('src_tp', 'username', 'password', 'uri')


class MachineLearningModelView(ModelView):
    datamodel = SQLAInterface(models.MlModels)
    search_columns = ['name']
    exclude_cols = ['changed_by', 'changed_on', 'created_by', 'created_on']
    add_exclude_columns = exclude_cols
    edit_exclude_columns = exclude_cols


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404


db.create_all()

appbuilder.add_view(FeatureSourceTypeModelView, 'List Feature Source Types', category="Feature Manager")
appbuilder.add_view(FeatureTypesModelView, 'List Feature Types', category='Feature Manager')
appbuilder.add_view(FeaturesModelView, 'List Features', category='Feature Manager')
appbuilder.add_view(FeatureSourceModelView, 'List Feature Source', category='Feature Manager')

appbuilder.add_view(MachineLearningModelView, 'List Models', category="Model Manager")
