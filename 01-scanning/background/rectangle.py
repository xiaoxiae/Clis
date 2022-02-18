from PIL import Image

image = Image.new("RGB", (1754, 1240))  # with default black color

pixels = image.load()

n = 50

for x in range(image.width):
    for y in range(image.height):
        pixels[(x, y)] = (0, 0, 0) if ((x // n) % 2 + (y // n) % 2) % 2 == 0 else (255, 255, 255)

image.save("rectangle.pdf")
