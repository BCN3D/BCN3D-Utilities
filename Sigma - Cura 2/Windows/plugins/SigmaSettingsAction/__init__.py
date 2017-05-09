from . import SigmaSettingsAction

from UM.i18n import i18nCatalog
catalog = i18nCatalog("cura")

def getMetaData():
    return {
        "plugin": {
            "name": catalog.i18nc("@label", "Sigma Settings action"),
            "author": "BCN3DTechnologies",
            "version": "1.0",
            "description": catalog.i18nc("@info:whatsthis", "Provides a way to change Sigma settings"),
            "api": 3
        }
    }

def register(app):
    return { "machine_action": SigmaSettingsAction.SigmaSettingsAction() }
