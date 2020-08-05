# publish services
# imports
import arcpy

# variables
folder = r"C:\jescudero\Esri\AM"
aprx_path = r"{0}\aprx\data_grid.aprx".format(folder)
sdd_path = r"{0}\aprx\Grilla.sddraft".format(folder)
sd_path = r"{0}\aprx\Grilla.sd".format(folder)

# environents
arcpy.env.overwriteOutput = 1

# Identify aprx
aprx = arcpy.mp.ArcGISProject(aprx_path)

# Create Service definition draft
maps = aprx.listMaps()
grid_map = maps[0]
ssd = grid_map.getWebLayerSharingDraft("HOSTING_SERVER", "FEATURE", "Grilla")
ssd.summary = "Grilla de coca"
ssd.description = u'Grilla de coca para el proceso de interpretación'
ssd.tags = u'Coca, Interpretación'
ssd.portalFolder = 'Datos'
ssd.overwriteExistingService = True

# Export service definition
ssd.exportToSDDraft(sdd_path)
arcpy.StageService_server(sdd_path, sd_path)

# Upload service definition
arcpy.UploadServiceDefinition_server(sd_path, "My Hosted Services")

# End

