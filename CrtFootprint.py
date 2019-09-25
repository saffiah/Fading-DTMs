# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os, shutil
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr, gdal_array
import json
import time

#Netherlands (should it be clipped to the coastline?)
workdir=os.path.join('/cygdrive','f','Fading','Sweden')
smRast= os.path.join(workdir,'Merge_Sweden.tif')
binRas= 'SwedenBin.tif'
outPoly= 'SwedenExtent.shp'

#get all raster information
raster = gdal.Open(smRast)
ys=raster.RasterYSize #rows
xs=raster.RasterXSize #cols
print ys, xs, 'rows, cols'
band = raster.GetRasterBand(1)
ndv = band.GetNoDataValue()
tr = raster.GetGeoTransform()
pr = raster.GetProjection()
xOrigin = tr[0]
yOrigin = tr[3]
pixelWidth = tr[1]
pixelHeight = tr[5]
raster = None #closes the raster data set

#import raster as numpy ndarray
rasterArray = gdal_array.LoadFile(smRast)
rasterArray[rasterArray!=ndv] = int(1)
rasterArray[rasterArray==ndv] = int(0)
# print rasterArray.dtype #(float32 data type)
# rasterArray = rasterArray.astype(np.int)

#write new 1/0 array to a new raster
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# driver=gdal.GetDriverByName("GTiff")
outfile=os.path.join(workdir,binRas)
# outDs = driver.Create(outfile, xs, ys, 1, gdal.GDT_Byte)
# band=outDs.GetRasterBand(1)
# band.WriteArray(rasterArray)
# band.FlushCache()
# # band.SetNoDataValue()
# outDs.SetGeoTransform(tr) #same as input raster
# outDs.SetProjection(pr)
# outDs = None

# exit()
#polygonize the raster
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#read newly created raster
src_ds=gdal.Open(outfile)
srcband=src_ds.GetRasterBand(1)
srcSRS=osr.SpatialReference()
srcSRS.ImportFromEPSG(4326)
#create final 1/0 polygon
dst_layername=os.path.join(workdir,outPoly)
drv=ogr.GetDriverByName("ESRI Shapefile")
newField = ogr.FieldDefn('FID',ogr.OFTInteger)
dst_ds=drv.CreateDataSource(dst_layername)
dst_layer=dst_ds.CreateLayer(dst_layername,srs=srcSRS)
dst_layer.CreateField(newField)
gdal.Polygonize(srcband,None,dst_layer,0,[],callback=None) #-1 instead of 0 if not creating a field
dst_ds=None
src_ds=None


