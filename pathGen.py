from PIL import Image

dest = r"c:\Users\abram\Documents\IT\Major Project\Assets\Images\pathGenTesting"
dir = r"c:\Users\abram\Documents\IT\Major Project\Assets\Images\Sprites"
angle = 30

flip = False
if angle < 0:
    flip = True
    angle = angle * -1

with Image.open(dir + r"\basePath.png") as im:
        im = im.rotate(angle, expand=True)
        print('Image Rotated')


imageWidth = im.width
imageHeight = im.height
pathWidth = 80
i = 0
height = -2

rgb_im = im.convert('RGBa')
print('Image Converted to RGBa')

print('Finding black pixels on last line...')
print('Pixels found:')

# This one removes the edge on the bottom line
for x in range(imageWidth):
    r, g, b, a = rgb_im.getpixel((x, imageHeight-1))
    if a > 20:
        i = i + 1
        print(str(i) + ": " + str(r), str(g), str(b), str(a), str(x))
        left = x
        x = imageWidth


im = im.crop([left, 0, pathWidth, 0])

i = 0
# This one removes the right column
for y in range(imageHeight):
        r, g, b, a = rgb_im.getpixel((1, y))
        if a > 20:
            i = i + 1
            print(str(i) + ": " + str(r), str(g), str(b), str(a), str(y))
            print(r, g, b, a, y)
            height = y
        if (height == (y-1)):
            y = imageHeight


height = imageHeight
if flip == True:
    print('Transposing and cropping for negative gradient...')

    im = im.transpose(Image.FLIP_TOP_BOTTOM)

    rgb_im = im.convert('RGBa')
    for y in range(imageHeight):
        r, g, b, a = rgb_im.getpixel((pathWidth, y))
        if a > 20:
            print('Right black pixel found.')
            print(r, g, b, a, y)
            height = y
            

im = im.crop([left, 0, pathWidth, height])
im.show()
im.save(dest + r"\generated45cropped.png")

