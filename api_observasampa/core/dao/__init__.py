from core.models.database import SessionLocal

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_obj():

    db_gen = get_db()

    return next(db_gen)