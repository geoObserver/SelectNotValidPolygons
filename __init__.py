from .selectnotvalidpolygons import SelectNotValidPolygonsPlugin

def classFactory(iface):
    return SelectNotValidPolygonsPlugin(iface)