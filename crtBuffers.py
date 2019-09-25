# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os, shutil
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr, gdal_array
import json
import time

#take footprint file and create series of buffer rasters
workdir=os.path.join('/cygdrive','f','Fading','Sweden','crtBuffer_gdal_prox')
if os.path.exists(workdir):
	print "output directory exists"
else:
	os.mkdir(workdir)

ftprint= os.path.join('/cygdrive','f','Fading','Sweden','SwedenBin2.tif')


py_cmd = '/usr/bin/python'
gd_cmd = '/usr/bin/gdal_proximity.py'
dist = float(1)/float(3600)

no_buffs = range(1,10)

for i in no_buffs:
	this_outfile = os.path.join(workdir,'SwedenBuf_{0}.tif'.format(i))
	this_dist=dist*float(i)
	print this_dist
	
	cmd='{0} {1} {2} {3} -ot Int16 -values 2 -maxdist {4} -distunits PIXEL -fixed-buf-val 4 -nodata 2'.format(py_cmd, gd_cmd,ftprint,this_outfile,str(i))
	print cmd
	os.system(cmd)

#add all the rasters together:
bufRas = os.listdir(workdir)
bufRas= [f for f in bufRas if f.endswith('.tif')]

sumRas = os.path.join('/cygdrive','f','Fading','Sweden','sumRas.tif')
os.chdir(workdir)
cmd = '{0} {1} -A {2} -B {3} -C {4} -D {5} -E {6} -F {7} -G {8} -H {9} -I {10} --outfile={11} --calc=\"A+B+C+D+E+F+G+H+I\"'.format(
	py_cmd,'/usr/bin/gdal_calc.py',bufRas[0], bufRas[1],bufRas[2],bufRas[3],bufRas[4],bufRas[5],bufRas[6],bufRas[7],
	bufRas[8],sumRas)
print cmd
os.system(cmd)

exit()
#reclassify the values 
#get all raster information
raster = gdal.Open(sumRas)
ys=raster.RasterYSize #rows
xs=raster.RasterXSize #cols
print ys, xs, 'rows, cols'
band = raster.GetRasterBand(1)
ndv = band.GetNoDataValue()
print 'no data value is ', ndv
tr = raster.GetGeoTransform()
pr = raster.GetProjection()
xOrigin = tr[0]
yOrigin = tr[3]
pixelWidth = tr[1]
pixelHeight = tr[5]
raster = None #closes the raster data set

#import raster as numpy ndarray
rasterArray = gdal_array.LoadFile(sumRas)
vals, inds = np.unique(rasterArray,return_index=True)
print vals
#create two rasters, one that fades into netherlands, and one that fades out of netherlands
#away from the 1-valued edge values should be 0
rasterArray1=rasterArray.astype(np.float32)
rasterArray1[rasterArray1==9.0] = 1.0
rasterArray1[rasterArray1==10.0] = 0.9
rasterArray1[rasterArray1==11.0] = 0.8
rasterArray1[rasterArray1==12.0] = 0.7
rasterArray1[rasterArray1==13.0] = 0.6
rasterArray1[rasterArray1==14.0] = 0.5
rasterArray1[rasterArray1==15.0] = 0.4
rasterArray1[rasterArray1==16.0] = 0.3
rasterArray1[rasterArray1==17.0] = 0.2
rasterArray1[rasterArray1==18.0] = 0.1
rasterArray1[rasterArray1==0.0] = 0.0

#Second raster
rasterArray2=rasterArray.astype(np.float32)
rasterArray2[rasterArray2==9.0] = 3.0
rasterArray2[rasterArray2==10.0] = 0.1
rasterArray2[rasterArray2==11.0] = 0.2
rasterArray2[rasterArray2==12.0] = 0.3
rasterArray2[rasterArray2==13.0] = 0.4
rasterArray2[rasterArray2==14.0] = 0.5
rasterArray2[rasterArray2==15.0] = 0.6
rasterArray2[rasterArray2==16.0] = 0.7
rasterArray2[rasterArray2==17.0] = 0.8
rasterArray2[rasterArray2==18.0] = 0.9
rasterArray2[rasterArray2==0.0] = 1.0
rasterArray2[rasterArray2==3.0] = 0.0

driver=gdal.GetDriverByName("GTiff")
outfile=os.path.join('/cygdrive','f','Fading','Sweden','fade1.tif')
outDs = driver.Create(outfile, xs, ys, 1, gdal.GDT_Float32)
band=outDs.GetRasterBand(1)
band.WriteArray(rasterArray1)
band.FlushCache()
# band.SetNoDataValue()
outDs.SetGeoTransform(tr) #same as input raster
outDs.SetProjection(pr)
outDs = None

driver=gdal.GetDriverByName("GTiff")
outfile=os.path.join('/cygdrive','f','Fading','Sweden','fade2.tif')
outDs = driver.Create(outfile, xs, ys, 1, gdal.GDT_Float32)
band=outDs.GetRasterBand(1)
band.WriteArray(rasterArray2)
band.FlushCache()
# band.SetNoDataValue()
outDs.SetGeoTransform(tr) #same as input raster
outDs.SetProjection(pr)
outDs = None


#multiply band raster (with weights) onto regular dtms





