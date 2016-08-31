from dslearn import db
from dslearn import models as m


def init_data():
    hive_db = m.FeatureSourceType(name='HiveServer2', uri='hive://localhost:10000')

    feature_type_num = m.FeatureTypes(name='Number')
    feature_type_ctg = m.FeatureTypes(name='Categroy')

    hive_tb = m.FeatureSource(name='dw.dw_pub_gds_info_td',
                    feature_source_type=hive_db)

    db.session.add_all([hive_db, feature_type_num, feature_type_ctg, hive_tb])
    db.session.commit()

if __name__ == '__main__':
    init_data()
