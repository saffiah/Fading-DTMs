# Fading-DTMs

The scripts in this repository were used to merge DTMs of differing resolution into each other so that a single grid tile in the model domain could capture data from multiple sources.

1. CrtFootprint.py: This script creates a binary raster (1's and 0's) of the DTM tile where there is data vs. no data then polygonizes.
2. crtBuffers.py: This script creates rings of buffers interior to the data/no data boundary. Each ring is 1 grid cell wide.
3. cutRaster.py: This script splits the raster into tiles along whole integer lat and lons
4. FadeTiles.py: This script performs the fading along the boundary between to different data sets. Each fading grid is multiplied by a data tile. The resulting rasters are summed.


