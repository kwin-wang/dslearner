#!/user/bin/env python
from dslearn import app, db, appbuilder
from dslearn.models import Features, FeatureSource
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


def init_manage():
    manager = Manager(app)
    migrate = Migrate(app, db)

    def make_shell_context():
        return dict(app=app, db=db, Features=Features, FeatureSource=FeatureSource)
    manager.add_command('shell', Shell(make_context=make_shell_context))
    manager.add_command('db', MigrateCommand)

    return manager


def main():
    manager = init_manage()
    manager.run()

if __name__ == "__main__":
    main()
