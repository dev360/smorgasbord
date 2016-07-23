import os
from os.path import abspath, dirname, join as pjoin

import sys

from django.conf import settings
from django.conf.urls import include, url


TRAY_REGISTRY = []


class TrayApp(object):
    """
    Represents your collection of tray
    enabled apps.
    """
    @property
    def parent_dir(self):
        """
        Parent dir of app
        """
        dir_root = abspath(dirname(__file__))
        return pjoin(dir_root, '..')

    @property
    def registry(self):
        return TRAY_REGISTRY

    def register(self, app):
        """
        Registers a tray app so that its webpack assets can
        be built correctly
        """
        if app not in TRAY_REGISTRY:
            TRAY_REGISTRY.append(app)

    @property
    def apps(self):
        INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS')
        return [x for x in self.registry if x in INSTALLED_APPS]

    @property
    def app_dirs(self):
        """
        Returns all the app directories
        """
        app_dirs = []
        for app_name in self.apps:
            app_dir = os.path.join(self.parent_dir, 'tray-{}'.format(app_name), app_name)
            app_dirs.append(app_dir)
        return app_dirs

    def discover(self):
        """
        Tries to auto discover tray apps whose repos
        are sibling directories to the main tray app
        and then adds these into the sys path correctly.
        """
        INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS')

        paths = []
        app_names = []
        for path, dirs, files in list(os.walk(self.parent_dir)):

            for d in dirs:
                app_name = d.replace('tray-', '') if 'tray-' in d else None
                if app_name and app_name in INSTALLED_APPS:
                    dir_path = path + '/' + d
                    paths.append(dir_path)
                    app_names.append(app_name)

        for path in paths:
            sys.path.insert(0, path)

        # Import the modules to force them to load.
        map(__import__, app_names)

    @property
    def urls(self):
        """
        Returns app the app urls
        """
        urls = []

        for app_name in self.apps:
            app_url = url(r'^{}/'.format(app_name), include('{}.urls'.format(app_name)))
            urls.append(app_url)
        return urls

    @property
    def staticfiles_dirs(self):
        """
        Returns the static files directories
        """
        dirs = (
            os.path.join(self.parent_dir, 'tray', 'client'),
        )

        for app_dir in self.app_dirs:
            dirs += (app_dir + '/client',)
        return dirs

app = TrayApp()
