import os
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from qgis.core import QgsRasterLayer, QgsProject, QgsCoordinateReferenceSystem
from qgis.utils import iface
import time


from qgis.PyQt.QtCore import QVariant
from qgis.core import (
    QgsProject,
    QgsGeometry,
    QgsFeatureRequest
)

plugin_dir = os.path.dirname(__file__)

class SelectNotValidPolygonsPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        # Create an action (i.e. a button) with Logo
        icon = os.path.join(os.path.join(plugin_dir, 'logo.png'))
        self.action = QAction(QIcon(icon), 'SelectNotValidPolygons', self.iface.mainWindow())
        # Add the action to the toolbar
        self.iface.addToolBarIcon(self.action)
        # Connect the run() method to the action
        self.action.triggered.connect(self.run)
      
    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        layer = iface.activeLayer()  # Oder ersetze mit QgsProject.instance().mapLayersByName("Layername")[0]
        valid_features = 0
        starttime = time.time()
        
        if not layer:
            print("Kein aktiver Layer gefunden.")
            self.iface.messageBar().pushMessage('Kein aktiver Layer gefunden. / No active layer found.',1,3)
        else:
            layer.removeSelection()
            invalid_ids = []

            for feature in layer.getFeatures():
                geom = feature.geometry()
                valid_features = valid_features + 1
                
                if not geom.isGeosValid():
                    invalid_ids.append(feature.id())
                    
            endtime = time.time()
            runtime = endtime - starttime

            if invalid_ids:
                layer.selectByIds(invalid_ids)
                print(f"{len(invalid_ids)} ungültige Polygone selektiert.")
                self.iface.messageBar().pushMessage('NotOK: ' + str(len(invalid_ids))+' from ' + str(valid_features) + ' polygons are not valid in layer "' + layer.name() + '" (runtime: ' + str(round(runtime,3)) + ' sec.).',1,5)
            else:
                print("Alle Geometrien sind gültig.")
                self.iface.messageBar().pushMessage('OK: All ' + str(valid_features) + ' polygons in layer "' + layer.name() + '" are valid (runtime: ' + str(round(runtime,3)) + ' sec.).',3,5)

