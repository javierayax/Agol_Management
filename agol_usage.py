# Calculate agol usage
# imports
from arcgis.gis import GIS
from initial_config import *

# Variables
usage_id = "c989c99c34a54915bb1ded804725e773"

# Connect to gis
gis = GIS(agol_url, agol_user, agol_password)

# Search content
mycontent = gis.content.search(query="owner:armando.castro", item_type="Dashboard", max_items=20)
adds = []
for item in mycontent:
    try:
        usage_df = item.usage(date_range='7D', as_df=True)
        for row in usage_df.itertuples():
            fecha = row[1]
            uso = row[2]
            add = {"attributes": {"nombre": item.name, "fecha": fecha, "uso": uso}}
            adds.append(add)
    except Exception as error:
        print("Un error ha ocurrido")
        print(error)

# Insert rows
usage_item = gis.content.get(usage_id)
table = usage_item.tables[0]
table.manager.truncate(asynchronous=True, wait=True)
result = table.edit_features(adds=adds)
print(result)
# End
