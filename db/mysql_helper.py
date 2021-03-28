from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

_CONNECTION_PATTERN = (
    'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8')


def create_session_factory(db, host, port, user, password, pool_size,
                           pool_recycle, max_overflow):

    if user:
        connection_url = _CONNECTION_PATTERN.format(
            db=db, host=host, port=port, user=user, password=password)
        engine = create_engine(
            connection_url,
            encoding='utf-8',
            echo=False,
            pool_size=pool_size,
            pool_recycle=pool_recycle,
            max_overflow=max_overflow,
            isolation_level='READ_COMMITTED')
    else:
        pass
    session_factory = sessionmaker(bind=engine)
    session_factory = scoped_session(session_factory)
    return session_factory


def create_row(sess, orm_row):

    sess.add(orm_row)


def get_count(sess, orm_item, filter_expr=None):
    query = sess.query(orm_item)
    if filter_expr is not None:
        query = query.filter(filter_expr)
    return query.count()


def delete_one(sess, orm_class, filter_expr):
    row = sess.query(orm_class).filter(filter_expr).one()
    sess.delete(row)
