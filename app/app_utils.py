"""
Created on 03/01/2021

file:           app_utils.py
description:

@author: Almoutaz
"""

# Load configuration at program initialization
def load_settings(app, where_running='document_scanner'):
    settings_path = "settings/"
    app.config.from_pyfile(settings_path + "default.cfg")

    if where_running == 'localhost':
        app.config.from_pyfile(settings_path + "localhost.cfg")
    elif where_running == 'style_transfer':
        app.config.from_pyfile(settings_path + "document_scanner.cfg")
    else:
        return "Error - load_settings(): cannot load settings"
    return ""

