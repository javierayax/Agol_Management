# Backup content from agol
# imports
from arcgis.gis import GIS
from initial_config import *

# variables
grid_id = "c5c5062765c54bc196631e6b01c2f55b"

# Connect to agol
gis = GIS(agol_url, agol_user, agol_password)

# Export item
grid_item = gis.content.get(grid_id)
result_export = grid_item.export("grilla_05_08_20", "File Geodatabase")

# Download item
result_download = result_export.download(r"C:\jescudero\Esri\AM\bk", "Grilla_05_08.zip")

print(result_download)

# End
