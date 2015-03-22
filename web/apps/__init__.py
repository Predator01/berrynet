# -*- encoding:utf-8 -*-


from flask import Flask
from abc import abstractmethod

from ..helpers import register_blueprints
from ..middlewares import HTTPMethodOverrideMiddleware



class AppFactory:

    SETTINGS_OBJECT = 'web.settings.development'
    SETTINGS_FILE = 'settings.cfg'
    SETTINGS_ENV = 'FLASK_SETTINGS'

    def __init__(
        self,
        package_name,
        package_path,
        settings_override=None,
        register_security_blueprint=True
    ):
        """Returns a :class:'Flask' application instance configured with common
        functionality.

        :param package_name: application package name
        :param package_path: application package path
        :param settings_override: a dictionary of settings to override
        :param register_security_blueprint: flag to specify if the Flask-Security
                                           Blueprint should be registered. Defaults
                                           to `True`.
        """

        app = Flask(package_name, instance_relative_config=True)
        app.config.from_object(cls.SETTINGS_OBJECT)
        app.config.from_pyfile(cls.SETTINGS_FILE, silent=True)
        app.config.from_object(settings_override)
        app.config.from_envvar(cls.SETTINGS_ENV, silent=True)
        register_blueprints(app, package_name, package_path)
        app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
        self.__app__ = app

        #app.secret_key = '\xf9\x96\xcf\x1e.{\xc1\xb8\nM\xe7@\xad\xbc\x88PG%\x961A\x14\xd7g'
        #db.init_app(app)
        #toolbar.init_app(app)
        #login_manager.init_app(app)
        #mail.init_app(app)
        # security.init_app(
        #     app,
        #     SQLAlchemyUserDatastore(db, User, Role),
        #     register_blueprint=register_security_blueprint)

    @abstractmethod
    def get_app(self):
        pass

    @abstractmethod
    def set_app_errors(self):
        # @app.errorhandler(SocialLoginError)
        # def social_login_error(error):
        #     return redirect(
        #         url_for('website.register', provider_id=error.provider.id, login_failed=1))
        pass

    @abstractmethod
    def set_app_constraints(self):
        # @app.before_first_request
        # def before_first_request():
        #     try:
        #         import apps.models
        #         apps.models.db.create_all()
        #     except Exception, e:
        #         app.logger.error(str(e))

        # @app.context_processor
        # def template_extras():
        #     return dict(
        #         google_analytics_id=app.config.get('GOOGLE_ANALYTICS_ID', None))
        pass

