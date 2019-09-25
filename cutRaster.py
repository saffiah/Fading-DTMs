# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os, shutil
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr, gdal_array
import json
import time

#Netherlands (should it be clipped to the coastline?)
original= os.path.join('/cygdrive','f','Fading','Netherlands','Filled','fade_in.tif')
original= os.path.join('/cygdrive','f','Fading','EUDEM','EU_DEM_EGMC.tif')

Tiles = os.path.join('/cygdrive','f','Fading','Tiles')
Tiles = os.path.join('/cygdrive','f','Fading','EUDEM','Tiles')

countryName = 'FadeIn_'
countryName = 'EUDEM_'

#read in raster, get the extent of the raster, and construct grid of tiles corresponding to 1x1 deg tiles that fall on whole integer corners that span the extent of the shape file.
raster = gdal.Open(original)
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

LLY=yOrigin+ys*pixelHeight
LLX=xOrigin
URY=yOrigin
URX=xOrigin+xs*pixelWidth

flrL=np.floor(LLY)
flrB=np.floor(LLX)
flrR=np.ceil(URY)
flrT=np.ceil(URX)

print LLY,LLX,URY,URX
print flrL, flrB, flrR, flrT

lons=range(int(flrB),int(flrT))
lats=range(int(flrL),int(flrR))
# lons=range(9,27)
# lats=range(55,70)

print "lons: "
print lons
print "lats:"
print lats

for degx in lons:
	for degy in lats:
		# print degx,degy
		if degx>= 0:
			ew= 'e'
		else:
			ew='w'
		if degy>=0:
			ns = 'n'
		else:
			ns = 's'
		tname = countryName+ns+str(abs(degy)).zfill(2)+ew+str(abs(degx)).zfill(3)+'.tif'
		# print tname
		tile=os.path.join(Tiles,tname)
		xmin = degx
		xmax = degx+1
		ymin = degy
		ymax = degy+1
		# gdalwarp -te 6 50 7 51 NewNethFO.tif NethTile_n50e006.tif
		cmd = 'gdalwarp -overwrite -co "COMPRESS=LZW" -te {0} {1} {2} {3} {4} {5}'.format(xmin,ymin,xmax,ymax,original,tile)
		print cmd
		os.system(cmd)




#then clip the raster to each of these tile geometries

