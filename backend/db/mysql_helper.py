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
    """
    Create a new row.

    Raise at sess.commit():
      sqlalchemy.exc.IntegrityError: If inserted row have duplicated key.

    Args:
      sess: A seesion obj.
      orm_row: orm row instance.
    """
    sess.add(orm_row)


def read_single(sess, orm_item, filter_expr):
    """
    Read item from a single row.

    Raise at sess.commit():
      sqlalchemy.orm.exc.NoResultFound: If no row match filter expr.
      sqlalchemy.orm.exc.MultipleResultsFound: If more than one row match.

    Args:
      sess: A seesion obj.
      orm_item: An orm item or a tuple of orm items to read. item is a orm
        class or orm class's member.
      filter_expr: Filter expression to filter row returned. Make sure that
        one and only one row match filter expression.

    Returns:
      An orm item instance or a tuple orm item instance. Depends on the
      input orm_item.
    """
    return sess.query(orm_item).filter(filter_expr).one()


def get_count(sess, orm_item, filter_expr=None):
    """
    Get num of row that meets filter_expr.

    Args:
      sess: A seesion obj.
      orm_item: An orm item. item is a orm class or orm class's member.
      filter_expr: Filter expression to filter row returned.
    """
    query = sess.query(orm_item)
    if filter_expr is not None:
        query = query.filter(filter_expr)
    return query.count()


def delete_one(sess, orm_class, filter_expr):
    """
    Delete a single row.

    Raise at sess.commit():
      sqlalchemy.orm.exc.NoResultFound: If no row match filter expr.
      sqlalchemy.orm.exc.MultipleResultsFound: If more than one row match.

    Args:
      sess: A seesion obj.
      orm_class: The orm class to update.
      filter_expr: Filter expression to filter row returned. Make sure one and
        only one row match filter expression.
    """
    row = sess.query(orm_class).filter(filter_expr).one()
    sess.delete(row)


def read_multiple(sess, orm_item, filter_expr=None,
                  order_by=None, offset=None, limit=None):
    """
    Read item from multiple rows.

    Args:
      sess: A seesion obj.
      orm_item: An orm item or a tuple of orm items to read. item is a orm
        class or orm class's member.
      filter_expr: Filter expression to filter row returned.
      order_by: orm item for order by.
      offset: integer for offset in SELECT expression.
      limit: integer for limit in SELECT expression.

    Returns:
      A list of result. Each result is an orm item instance or a tuple orm
      item instance. Depends on the input orm_item.
    """
    query = sess.query(orm_item)
    if filter_expr is not None:
        query = query.filter(filter_expr)
    if order_by is not None:
        query = query.order_by(order_by)
    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)
    return query.all()
