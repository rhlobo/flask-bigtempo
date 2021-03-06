#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

from .blueprint import new_blueprint
from .storages import SQLAlchemyStorage


class DatastoreAPI(object):

    def __init__(self, app=None, sql_engine=None):
        self._storage = None

        self.app = app
        self.sql_engine = sql_engine

        if app is not None and sql_engine is not None:
            self.init_app(app, sql_engine)

    def init_app(self, app, sql_engine):
        app.register_blueprint(new_blueprint(self.instance))

    def _lazyload_instance(self):
        if self._storage is None:
            self._storage = SQLAlchemyStorage(self.sql_engine, '{reference}__{symbol}')
        return self._storage

    @property
    def instance(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'bigtempo_datastore_instance'):
                ctx.bigtempo_datastore_instance = self._lazyload_instance()
            return ctx.bigtempo_datastore_instance
        else:
            return self._lazyload_instance()
