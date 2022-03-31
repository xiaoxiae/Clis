# Scanning climbing walls
A short tutorial on how to do photogrammetry on various types of climbing walls. Most of this is my personal opinion, formed by experimentation and various blog posts / YouTube videos about photogrammetry, so take it with a grain of salt.

I will leave links to the resources that I used while figuring things out where appropriate.

## Overview
The basic idea is the following:
1. take photos of the wall
2. create a point cloud using some photogrammetry software (like [Meshroom](https://github.com/alicevision/meshroom))
3. create the model using the point cloud from the previous step and some 3D modelling software (like Blender)

Using this method, I managed to create a very detailed 3D model of the [Smíchoff climbing wall](https://www.lezeckecentrum.cz/cs/) in about 10 hours of work, which I'd say is pretty decent. The model, in various formats, can be found in the `smichoff/` folder, if you're interested.

## Taking photos
Taking photos is the most crucial part of the entire process, since their quality will largely determine how accurate the model will be.

Use any device you can, but obviously the higher quality the better (I used my Nikon Z50 DLSR). When doing so, there are a few things to keep in mind:
- use different overlapping angles of each area you're capturing so the photogrammetry software has an easier time figuring everything out
- **do not change the area** that you're capturing by having people around or moving things about, else the reconstruction will most likely fail (or will exclude a lot of images, making the model inaccurate)
- the settings (ISO, shutter speed) and even the devices can differ between individual shots, but the photos should be as clear as possible and *should include the metadata** (namely the focal length), since the photogrammetry software uses this information to calculate the points

## Create a point cloud
Since I've only ever used Meshroom, I can't say much about other photogrammetry softwares. However, using Meshroom is free and easy, so I'd suggest you do the same.

To produce the pointcould, import the photos to Meshroom, press Start and you're basically done. Now you only need to wait for the `StructureFromMotion` step to complete, after which you should be able to find the `points3D.txt` file in the cache folder.

I wrote a small script `meshroom_points_to_ply.py` that converts this format to a regular `.ply` file which can then be used in step 3.

## Create the model
Again, since I've only ever used Blender, I can't say much about other 3D modelling software.

In blender, I used the [Point Cloud Visualizer plugin](https://github.com/uhlik/bpy) (an older, free version that is still very much usable can be found [here](https://raw.githubusercontent.com/uhlik/bpy/master/space_view3d_point_cloud_visualizer.py))
