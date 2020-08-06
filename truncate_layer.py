# Truncate layer
# imports
from arcgis.gis import GIS
from initial_config import *

# Variables
truncate = False

# Connect to GIS
gis = GIS(agol_url, agol_user, agol_password)

# get content
erradicacion_id = "9bc352654401432ca046825fd35f8fc1"
item = gis.content.get(erradicacion_id)
layer = item.layers[0]
condition = "objectid > 358"

# Truncate
if truncate:
    resutl = layer.manager.truncate(asynchronous=True, wait=True)
else:
    result = layer.delete_features(where=condition)

print(result)
# End

