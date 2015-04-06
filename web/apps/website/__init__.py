# -*- coding: utf-8 -*-
"""
    berrynet.web.website
    -----------

    berrynet website application package
"""


import werkzeug.exceptions

from functools import wraps

from flask import request
from flask_assets import Environment, Bundle

from web.helpers import JSONEncoder
from .. import AppFactory



class Website(AppFactory):

    def __init__(
        self, 
        settings_override=None, 
        register_security_blueprint=False
    ):
        """Set the Berrynet Website application instance"""
        super(Website, self).__init__(
            __name__,
            __path__,
            settings_override=settings_override,
            register_security_blueprint=register_security_blueprint)

        assets = Environment(self.__app__)
        self.set_app_assets(assets)


    def get_app(self):
        """Returns the Cancan API application instance"""
        return self.__app__

    def set_app_errors(self):
        pass
        # self.__app__.errorhandler(OverholtError)(on_overholt_error)
        # self.__app__.errorhandler(OverholtFormError)(on_overholt_form_error)
        # self.__app__.errorhandler(404)(on_404)pass

    def set_app_constraints(self):
        pass

    def set_app_assets(self, assets):
        #: application css bundle
        # css_overholt = Bundle("less/overholt.less",
        #                        #filters="less", 
        #                        output="css/overholt.css",
        #                        debug=False)

        # #: consolidated css bundle
        # css_all = Bundle("css/bootstrap.min.css", css_overholt,
        #                  "css/bootstrap-responsive.min.css",
        #                  "css/base.css",
        #                  #filters="cssmin", 
        #                  output="css/overholt.min.css")
        css_all = Bundle("css/base.css",
                         output="css/berrynet.min.css")

        # #: vendor js bundle
        # js_vendor = Bundle("js/vendor/jquery-1.10.1.min.js",
        #                    "js/vendor/bootstrap-2.3.3.min.js",
        #                    "js/vendor/underscore-1.4.4.min.js",
        #                    "js/vendor/backbone-1.0.0.min.js",
        #                    #filters="jsmin", 
        #                    output="js/vendor.min.js")

        # #: application js bundle
        # js_main = Bundle("coffee/*.coffee", 
        #                  #filters="coffeescript", 
        #                  output="js/main.js")

        assets.register('css_all', css_all)
        #assets.register('js_vendor', js_vendor)
        #assets.register('js_main', js_main)
        assets.manifest = 'cache' if not self.__app__.debug else False
        assets.cache = not self.__app__.debug
        assets.debug = self.__app__.debug
