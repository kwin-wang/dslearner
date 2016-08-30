# -*- coding: utf-8
from flask import render_template
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder import ModelView
from . import appbuilder, db
from . import models

class FeaturesModelView(ModelView):
    datamodel = SQLAInterface(models.Features)
    search_columns = ["name", "filed_name"]
    exclude_cols = ['changed_by', 'changed_on', 'created_by', 'created_on']
    columns = ['name', 'filed_name', 'feature_type', 'statistical_caliber', 'method_update', 'is_valid']
    list_columns = columns
    # edit_columns = columns
    # add_columns = columns
    edit_exclude_columns = exclude_cols
    add_exclude_columns = exclude_cols



class FeatureSourceModelView(ModelView):
    datamodel = SQLAInterface(models.FeatureSource)
    list_columns = ['name', 'feature_source_type']
    edit_columns = ["name"]
    add_columns = ["name", 'feature_source_type']
    related_views = [FeaturesModelView]
    

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


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()
appbuilder.add_view(FeatureSourceTypeModelView, 'List Feature Source Type', category="Feature Manager")
appbuilder.add_view(FeaturesModelView, 'List Features', category='Feature Manager')
appbuilder.add_view(FeatureSourceModelView, 'List Feature Source', category='Feature Manager')
appbuilder.add_view(MachineLearningModelView, 'List Models', category="Model Manager")
