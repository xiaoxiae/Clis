# Scanning climbing walls
A short tutorial on how to do photogrammetry on various types of climbing walls. Most of this is my personal opinion, formed by experimentation and various blog posts / YouTube videos about photogrammetry, so take it with a grain of salt.

I will leave links to the resources that I used while figuring things out where appropriate.

## Overview
The basic idea is the following:
1. take photos of the wall
2. create a model some photogrammetry software (like [Metashape](https://www.agisoft.com/))
3. clean up the model using some 3D modelling software (like Blender)

Using this method, I managed to create a very detailed 3D model of the [Smíchoff climbing wall](https://www.lezeckecentrum.cz/cs/) in about 10 hours of work.

## Taking photos
Taking photos is the most crucial part of the entire process, since their quality will largely determine how accurate the model will be.

Use any device you can, but obviously the higher quality the better (I used my Nikon z50). When doing so, there are a few things to keep in mind:
- use different overlapping angles of each area you're capturing so the photogrammetry software has an easier time figuring everything out
- **do not change the area** that you're capturing by having people around or moving things about, else the reconstruction will most likely fail (or will exclude a lot of images, making the model inaccurate)
- the settings (ISO, shutter speed) and even the devices can differ between individual shots, but the photos should be as clear as possible and *should include the metadata** (namely the focal length), since the photogrammetry software uses this information to calculate the features
