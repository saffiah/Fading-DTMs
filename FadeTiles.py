# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os, shutil
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr, gdal_array

#(1) go through each tile, grab the country tile (Netherlands), the background tile (SRTM) and the 
#two fading tiles.
#(2) multiply the country tile by the fadeOut and the background tile by fadeIn
#(3) add the results

bkgd = os.path.join('/cygdrive','f','Fading','SRTM_Neth')
country= os.path.join('/cygdrive','f','Fading','Tiles','Netherlands')
Fading = os.path.join('/cygdrive','f','Fading','Tiles','Fade')
outdir = os.path.join('/cygdrive','f','Fading','Fade_Merge','Netherlands')

rawTiles=os.listdir(bkgd)
rawTiles = [f for f in rawTiles if f.endswith('.tif')]

 #closes the raster data set

for bkgdTile in rawTiles:
	print bkgdTile
	ctTile = os.path.join(country,'Neth_'+bkgdTile)
	fadeIn = os.path.join(Fading,'FadeIn_'+bkgdTile)
	fadeOut = os.path.join(Fading,'FadeOut_'+bkgdTile)

	print ctTile,fadeIn,fadeOut
	fadeInArr = gdal_array.LoadFile(fadeIn)
	fadeOutArr = gdal_array.LoadFile(fadeOut)
	ctArr = gdal_array.LoadFile(ctTile)
	bkgdArr = gdal_array.LoadFile(os.path.join(bkgd,bkgdTile))

	#get all raster information from sample raster
	raster = gdal.Open(ctTile)
	ys=raster.RasterYSize #rows
	xs=raster.RasterXSize #cols
	band = raster.GetRasterBand(1)
	ndvC = band.GetNoDataValue()
	tr = raster.GetGeoTransform()
	pr = raster.GetProjection()
	xOrigin = tr[0]
	yOrigin = tr[3]
	pixelWidth = tr[1]
	pixelHeight = tr[5]
	raster = None

	numNaN=np.squeeze(np.asarray(np.where(ctArr==ndvC)))
	a,b= numNaN.shape
	print b
	# fadeIn should multiply the background tiles
	# if fadeIn has only 2 unique values of 1 and 0, then it spans a 1x1 deg cell that lies outside of the original neth extent
	#replace the 0 values with 1. or, whereever the country tile is no data, replace those index values in the fadeInArr to be 1
	vals, inds = np.unique(fadeInArr,return_index=True)
	print vals
	print fadeInArr.shape
	
	if b > 0:
		fadeInArr[ctArr == ndvC] = float(1)

	bkgd_fade= np.multiply(fadeInArr,bkgdArr)	

	# fadeOut should multiply the country tiles
	# NaN of country tile should be recast as 0. Then that 0 value can be added to background tile of raster
	if b > 0:
		ctArr[ctArr == ndvC] = float(0)

	ct_fade = np.multiply(fadeOutArr,ctArr)

	finalArr = ct_fade+bkgd_fade

	#write final array as a raster
	driver=gdal.GetDriverByName("GTiff")
	outfile=os.path.join(outdir, 'fin_'+bkgdTile)
	outDs = driver.Create(outfile, xs, ys, 1, gdal.GDT_Float32)
	band=outDs.GetRasterBand(1)
	band.WriteArray(finalArr)
	band.FlushCache()
	# band.SetNoDataValue()
	outDs.SetGeoTransform(tr) #same as input raster
	outDs.SetProjection(pr)
	outDs = None


	




# Filled=np.multiply(rasterArray,maskB_new) + zonalAvgArr


