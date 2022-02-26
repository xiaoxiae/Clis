# Tutorial
A short tutorial on how to do photogrammetry on various types of climbing holds. Most of this is my personal opinion, formed by experimentation and various blog posts / YouTube videos about photogrammetry, so take it with a grain of salt.

I will leave links to the resources that I used while figuring things out where appropriate.

## Software used
The software used is [Agisoft Metashape Pro](https://www.agisoft.com/) using its Python bindings (see `../02-processing/README.md`). The program is relatively intuitive and simple to use, so I won't go into any detail regarding its GUI (there are many good tutorials out there that you can use if you're interested).

## Setup
This approach covers **turntable-based photogrammetry**, meaning that the holds are on a turntable that is being captured by a stationary camera. This is essentially the same thing as turning the camera around the object (although arguably less convenient), since the background is uniform and the software has no way of telling the difference.

### Camera
I'm using the [Nikon Z 50](https://en.wikipedia.org/wiki/Nikon_Z_50) mirrorless camera to take the pictures and would suggest you use a camera too -- while mobile phones produce fine photos, nothing can beat a good camera. Besides the quality of the images, it is also extremely important for the cameras to contain metadata about how the photo was taken (focal length, shutter speed, ISO, f/s), which is very useful to the photogrammetry process.

You should generally strive for lower ISO (duh) and higher f/s, because you want the depth of field to be as large as possible -- this makes it easier for the software to recognize key features to match between the photos. Luckily, since (most) of the holds don't move, slower shutter speeds are quite acceptable to achive both low ISO and high f/s.

### Background
I'm using black background with a green turntable. The colors themselves aren't all that important, but should be decently contrasting to the object being scanned -- green holds on a green background could give the software some trouble.

### Markers
Besides the background, I use 3 markers to automatically adjust the object into its proper scale and location. This can be done quite trivially in the `Markers/` Metashape menu, where you can both generate a set of markers of desired size and also detect them in the images.

### Lighting
It is absolutely vital for the holds to be decently lit by **soft light**, ideally from multiple directions. This can be achieved by some less powerful LED lights (at most 20W) and appropriate mounting equipment. When bought right, this can be relatively cheap, but improve the quality of the scans by a large margin.

If the lights still produce light that is too hard, I'd suggest you put baking paper (or any other not-easily-flammable material) around them to better diffuse the light. This is miles cheaper than any diffuse filter you find on the market but yields similar results.

## On scanning various holds

### Dual-texture holds
When scanning dual-texture holds (and glassy holds in general), the software will have trouble finding enough features to produce a good model in the glossy area. To prevent this, I'd suggest you apply small amount of chalk on the glossy parts.

### Large volumes
TODO: anything to say here?
