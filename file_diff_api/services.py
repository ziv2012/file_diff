import db.database as _database
import db.models as _models


def _add_tables():
    return _database, _database.Base.metadata.create_all(bind=_database.engine)
