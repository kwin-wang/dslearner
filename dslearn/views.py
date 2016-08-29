from flask import render_template
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder import ModelView
from . import appbuilder, db
from . import models

"""
    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(MyModelView, "My View", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
"""

"""
    Application wide 404 error handler
"""


class FeaturesModelView(ModelView):
    datamodel = SQLAInterface(models.Features)
    search_columns = ["name", "filed_name"]
    exclude_cols = ['changed_by', 'changed_on', 'created_by', 'created_on'\
                    ]
    columns = ['name', 'filed_name', 'feature_type', 'statistical_caliber', 'method_update', 'is_valid']
    list_columns = columns
    # edit_columns = columns
    # add_columns = columns
    edit_exclude_columns = exclude_cols
    add_exclude_columns = exclude_cols


class FeatureTablesModelView(ModelView):
    datamodel = SQLAInterface(models.FeatureTables)
    list_columns = ['name']
    edit_columns = ["name"]
    add_columns = ["name"]
    related_views = [FeaturesModelView]


class MachineLearningModelView(ModelView):
    datamodel = SQLAInterface(models.MlModels)
    search_columns = ['name']


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()
appbuilder.add_view(FeaturesModelView, 'List Features', category='Feature Manager')
appbuilder.add_view(FeatureTablesModelView, 'List Tables', category='Feature Manager')


