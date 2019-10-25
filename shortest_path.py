import os
import time
from qgis.core import QgsVectorLayer, QgsRasterLayer
from qgis.gui import QgsMapCanvas
from qgis._gui import QgsMapToolEmitPoint
from qgis.utils import iface

#This function computes the shortest path between the clicked point
#and a fixed point (RMIT University) using QNEAT3 toolbox
def my_shortest_path(pointTool):
    try:
        #reading the coordinate of the points clicked
        #and writing in a string format to call shortest path algorithm
        
        startPoint = str(pointTool.x())+","+str(pointTool.y())+" [EPSG:4326-WGS84]"
        endPoint = "144.963403,-37.808179 [EPSG:4326-WGS84]" #coordinate of RMIT

        #path to the road network data (please change accordingly)
        roads_path = r"/Users/chhanda/Desktop/GIS_Programming/Major_project/Street_network_2018/shp/road.shp"
        #set outputfile directory
        outputfilepath = r"Users/chhanda/Desktop/GIS_Programming/Major_project/"

        #setting up the shortest path parameters
        shortestpathParam={'DEFAULT_DIRECTION': 2,'DEFAULT_SPEED':50,'DIRECTION_FIELD':None,'END_POINT':endPoint,'ENTRY_COST_CALCULATION_METHOD':0,'INPUT':roads_path,'OUTPUT':outputfilepath+"shortestpath_output",'SPEED_FIELD':None,'START_POINT':startPoint,'STRATEGY':0,'TOLERANCE':0,'VALUE_BACKWARD':'','VALUE_BOTH':'','VALUE_FORWARD':''}
        processing.run("qneat3:shortestpathpointtopoint", shortestpathParam)

        #loading the shortest path layer from the poutput of the previous processing run
        sp_file_path = outputfilepath+"shortestpath_output.gpkg"
        sp_layer = QgsVectorLayer(sp_file_path,"shortest_path", "ogr")
        if not sp_layer.isValid():
            print("Shortest Path Layer failed to load!")

        #loading road network layer
        road_layer = QgsVectorLayer(roads_path,"roads", "ogr")
        if not road_layer.isValid():
            print("road Layer failed to load!")

        #setting the url of the base layer from ESRI
        base_layer = QgsRasterLayer("http://server.arcgisonline.com/arcgis/rest/services/ESRI_Imagery_World_2D/MapServer?f=json&pretty=true","raster")

        #styling the shortest path layer (color and line width) 
        sp_layer.renderer().symbol().setWidth(0.6)
        sp_layer.renderer().symbol().setColor(QColor("red"))

        #creating a point layer to show the start point and the end point
        point_layer = QgsVectorLayer("Point", "temporary_points", "memory")
        pr = point_layer.dataProvider()
        #enter editing mode
        point_layer.startEditing()
        #add a field to display the labels
        pr.addAttributes([QgsField("name", QVariant.String)])
        point_layer.updateFields()
        #add features
        fet = QgsFeature()
        fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(pointTool.x(),pointTool.y())))
        pr.addFeatures( [ fet ] )
        point_layer.changeAttributeValue(1, 0, "Your Home")
        fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(144.963403,-37.808179)))
        pr.addFeatures( [ fet ] )
        point_layer.changeAttributeValue(2, 0, "RMIT UNIVERSITY")
        # Commit changes
        point_layer.commitChanges()
        
        #styling the point layer (size and color)
        point_layer.renderer().symbol().setSize(6)
        point_layer.renderer().symbol().setColor(QColor("red"))

        #styling the labels to make them appear with white background
        layer_settings  = QgsPalLayerSettings()
        text_format = QgsTextFormat()

        background_color = QgsTextBackgroundSettings()
        background_color.setFillColor(QColor('white'))
        background_color.setEnabled(True)

        text_format.setFont(QFont("Arial", 12))
        text_format.setSize(12)
        text_format.setBackground(background_color )

        buffer_settings = QgsTextBufferSettings()
        buffer_settings.setEnabled(True)
        buffer_settings.setSize(0.10)
        buffer_settings.setColor(QColor("black"))

        text_format.setBuffer(buffer_settings)
        layer_settings.setFormat(text_format)

        layer_settings.fieldName = "name"
        layer_settings.placement = 4

        layer_settings.enabled = True

        layer_settings = QgsVectorLayerSimpleLabeling(layer_settings)
        point_layer.setLabelsEnabled(True)
        point_layer.setLabeling(layer_settings)
        
        #initialising an output fgrame
        output_canvas = QgsMapCanvas()
        #chosing the layers to display
        output_canvas.setLayers([sp_layer, point_layer, base_layer])
        #getting the extent of the shortest path layer to zoom into the path
        ext = sp_layer.extent()
        xmin = ext.xMinimum()
        xmax = ext.xMaximum()
        ymin = ext.yMinimum()
        ymax = ext.yMaximum()
        #setting extent of the output to that of a box slightly larger than the shortest path layer
        #such that the labels don't get chopped
        output_canvas.setExtent(QgsRectangle(xmin-0.01,ymin-0.01,xmax+0.01,ymax+0.01))
        output_canvas.show()

        #the function raises an error because eiting without error causes the output window to disappear 
        raise
    
    except AttributeError:
        pass

#loading road network layer
roads_path = r"/Users/chhanda/Desktop/GIS_Programming/Major_project/Street_network_2018/shp/road.shp"
road_layer = QgsVectorLayer(roads_path,"roads", "ogr")
if not road_layer.isValid():
    print("Layer failed to load!")
#setting the url of the base layer
base_layer = QgsRasterLayer("http://server.arcgisonline.com/arcgis/rest/services/ESRI_Imagery_World_2D/MapServer?f=json&pretty=true","raster")

#creating a point layer to highlight RMIT
point_layer = QgsVectorLayer("Point", "temporary_points", "memory")
pr = point_layer.dataProvider()
#enter editing mode
point_layer.startEditing()
#add attribute for labels
pr.addAttributes([QgsField("name", QVariant.String)])
point_layer.updateFields()
# add a feature
fet = QgsFeature()
fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(144.963403,-37.808179)))
pr.addFeatures( [ fet ] )
point_layer.changeAttributeValue(1, 0, "RMIT UNIVERSITY\n(Click on your house location to\n obtain the shortest path to here)")
# Commit changes
point_layer.commitChanges()

#styling the point layer (size and color)
point_layer.renderer().symbol().setSize(6)
point_layer.renderer().symbol().setColor(QColor("red"))

layer_settings  = QgsPalLayerSettings()
text_format = QgsTextFormat()
background_color = QgsTextBackgroundSettings()

#styling the labels to make them appear with white background
background_color.setFillColor(QColor('white'))
background_color.setEnabled(True)

text_format.setFont(QFont("Arial", 12))
text_format.setSize(12)
text_format.setBackground(background_color )

buffer_settings = QgsTextBufferSettings()
buffer_settings.setEnabled(True)
buffer_settings.setSize(0.10)
buffer_settings.setColor(QColor("black"))

text_format.setBuffer(buffer_settings)
layer_settings.setFormat(text_format)

layer_settings.fieldName = "name"
layer_settings.placement = 4

layer_settings.enabled = True

layer_settings = QgsVectorLayerSimpleLabeling(layer_settings)
point_layer.setLabelsEnabled(True)
point_layer.setLabeling(layer_settings)

#creating a window to display the map of Melbourne and the RMIT location
canvas = QgsMapCanvas()
canvas.setLayers([point_layer, base_layer])
canvas.setExtent(road_layer.extent())
canvas.show()

#setup click trigger to capture the clicked location and then call the shortest path calculator function
pointTool = QgsMapToolEmitPoint(canvas)
pointTool.canvasClicked.connect(my_shortest_path)
canvas.setMapTool(pointTool)
