from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature
from hello_flask_app.search import add_to_index, query_index, remove_from_index
from hello_flask_app.extensions import db


class SearchableMixin:
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []

        for each, index in enumerate(ids):
            when.append((each, index))
        print(ids)
        return (
            cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)),
            total,
        )

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted),
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(index=obj.__tablename__, model=obj)

        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(index=obj.__tablename__, model=obj)

        for obj in session._changes['delete']:
            remove_from_index(index=obj.__tablename__, model=obj)

    # set index for all data
    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


secret_key = 'hard to gess string'


def Generate_reset_password_token(email, expiration=3600):
    s = Serializer(secret_key, expires_in=expiration)
    return s.dumps({"email": email})


def verify_reset_password(token):
    try:
        s = Serializer(secret_key)
        data = s.loads(token)
        return data["email"]
    except BadSignature:
        return None


class SerializeMixin:
    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
            return d


# def make_celery(hello_flask_app):
#     celery = Celery(hello_flask_app.import_name, broker=hello_flask_app.config['CELERY_BROKER_URL'])
#     celery.conf.update(hello_flask_app.config)
#     TaskBase = celery.Task
#     class ContextTask(TaskBase):
#         abstract = True
#         def __call__(self, *args, **kwargs):
#             with hello_flask_app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#     celery.Task = ContextTask
#     return celery


# token = Generate_reset_password_token('fjl2401')
# print(token)
# print verify_reset_password(token)

from flask import abort
import math


# 将list 转换为分页对象


class ListPagination:
    def __init__(self, iterable, page=1, per_page=20):

        if page < 1:
            abort(404)

        self.iterable = iterable
        self.page = page
        self.per_page = per_page

        self.total = len(iterable)

        start_index = (page - 1) * per_page
        end_index = page * per_page

        self.items = iterable[start_index:end_index]

        if not self.items and page != 1:
            abort(404)

    @property
    def pages(self):
        """The total number of pages"""
        return int(math.ceil(self.total / float(self.per_page)))

    def prev(self):
        assert (
            self.iterable is not None
        ), "an object is required for this method to work"
        iterable = self.iterable
        return self.__class__(iterable, self.page - 1, self.per_page)

    @property
    def prev_num(self):
        """Number of the previous page."""
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1

    def next(self):
        assert (
            self.iterable is not None
        ), "an object is required for this method to work"
        iterable = self.iterable
        return self.__class__(iterable, self.page + 1, self.per_page)

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page"""
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        """Iterates over the page numbers in the pagination.  The four
        parameters control the thresholds how many numbers should be produced
        from the sides.  Skipped page numbers are represented as `None`.
        """
        last = 0
        for num in range(1, self.pages + 1):
            if (
                num <= left_edge
                or num > self.pages - right_edge
                or (
                    num >= self.page - left_current and num <= self.page + right_current
                )
            ):
                if last + 1 != num:
                    yield None
                yield num
                last = num
        if last != self.pages:
            yield None
