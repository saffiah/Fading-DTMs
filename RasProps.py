# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os, shutil
import numpy as np
from osgeo import gdal, ogr, osr, gdal_array

#directory of Sweden files:
workdir = os.path.join('/cygdrive','f','Fading','Sweden')

AllFiles = os.listdir(workdir)
SW_Tif_Tiles = [f for f in AllFiles if f.endswith('.tif') and f.startswith('nh')]

for f in SW_Tif_Tiles:
	#read in raster, get the extent of the raster, and construct grid of tiles corresponding to 1x1 deg tiles that fall on whole integer corners that span the extent of the shape file.
	raster = gdal.Open(f)
	ys=raster.RasterYSize #rows
	xs=raster.RasterXSize #cols
	# print ys, xs, 'rows, cols'
	band = raster.GetRasterBand(1)
	ndv = band.GetNoDataValue()
	print 'No data value is ',ndv, ' for file ', f
	raster = None #closes the raster data set
