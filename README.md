# Clitoris Vulgaris

A Twitter bot that produces new species of clitoris by projecting botanical
illustrations onto a 3D model. The image is rendered with Blender and automated
with a Python script using the Blender API.

## Twitter bot

Every day the bot will publish an image with a name. The name is randomly
generated with Latin adjectives usually used for plants. The dataset was taken
from a [USDA plant list](http://plants.usda.gov/dl_all.html).

The textures were taken from two sources: [Bristish Library’s Flickr collection
of historic illustrations](https://www.flickr.com/photos/britishlibrary) and
[Wikimedia’s USDA Pomological Watercolors](https://commons.wikimedia.org/wiki/Category:USDA_Pomological_Watercolors).

## How to render an image

### Build the Docker image

```bash
cd clistoscope
docker build -t fhoehl/clitorisvulgaris .
```

The container has one volume called `/data` where there should be a `textures`
folder.

### Start a render

```bash
docker run --rm -v $DATA_FOLDER:/data/ fhoehl/clitorisvulgaris scene.blend --python scene.py -o /render/image -f 1
```

## Thanks

[Initial 3d model and inspiration](http://carrefour-numerique.cite-sciences.fr/fablab/wiki/doku.php?id=projets:clitoris)

[How to find a dominant color palette in an image with k-means](http://charlesleifer.com/blog/using-python-and-k-means-to-find-the-dominant-colors-in-images/)

[Blender](https://www.blender.org/)

[List of plants and their latin name](http://plants.usda.gov/dl_all.html)

[Flora from Mechanical Curator Collection](https://www.flickr.com/photos/britishlibrary/sets/72157641857515565)

[USDA Pomological Watercolors](https://commons.wikimedia.org/wiki/Category:USDA_Pomological_Watercolors)

---

[MIT license](LICENSE)
