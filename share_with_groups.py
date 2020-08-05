# Share with groups
# Imports
from arcgis.gis import GIS
from initial_config import *

# Variables
grid_id = "c5c5062765c54bc196631e6b01c2f55b"

# Conect to GIS
gis = GIS(agol_url, agol_user, agol_password)

# Get Content
grid_item = gis.content.get(grid_id)

grid_item.share(groups=["904de0a3077b4e4789aa7c31f96b99ec", "e443167ae59040ec888d589b668e3e13"])

# End
