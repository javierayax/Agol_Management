# Calculate field
# imports
from initial_config import *
from arcgis.gis import GIS
from arcgis.geometry import Point
from arcgis.geometry import SpatialReference
from arcgis.geometry import filters

# Variables
erradication_id = "9bc352654401432ca046825fd35f8fc1"
municipio_id = "43b88e5f2549404886f2b3725126d7c7"

# Connect to agol
gis = GIS(agol_url, agol_user, agol_password)

# Read data
erradicacion_item = gis.content.get(erradication_id)
erradicacion_lyr = erradicacion_item.layers[0]
erradicacion_fs = erradicacion_lyr.query()
erradicacion_df = erradicacion_fs.sdf
mpio_layer = gis.content.get(municipio_id).layers[0]

# Process data
errad_summarize = erradicacion_df.groupby(['nombremunicipio'])['hectareas'].sum()

updates = []
for row in erradicacion_lyr.query(where="nombremunicipio = '-'"):

    # get attributes
    oid = row.attributes['OBJECTID']
    x = row.geometry["x"]
    y = row.geometry["y"]

    # Create spatial filter
    point = Point({"x": x, "y": y})
    sr = SpatialReference({"wkid": 4326})
    geom_filter = filters.intersects(point, sr)

    # Query data using a point (Identify)
    mpio = mpio_layer.query(out_fields="coddane, nombremunicipio, nombredepartamento", geometry_filter=geom_filter, return_geometry=False)

    # Create update record
    nombre_mpio = mpio.features[0].attributes["nombremunicipio"]
    nombre_depto = mpio.features[0].attributes["nombredepartamento"]
    coddane = mpio.features[0].attributes["coddane"]
    update = {"attributes": {"objectid": oid, "NombreMunicipio": nombre_mpio, "NombreDepartamento": nombre_depto, "coddane": coddane}}

    updates.append(update)

# Update incidentes
erradicacion_lyr.edit_features(updates=updates)

# End
