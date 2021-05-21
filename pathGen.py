from PIL import Image

'''
This code is for generating the path
from a base file with a rectangle in it. It
runs in a separate process on a separate core 
in the CPU in order to negate lag
and/or FPS drop. It is also more efficient than making 
68,400 images on piskel one at a time and saving them
all to the project file and crashing the user's computer.

"I'm proud of what we've accomplished here." - Abram Liddell, 2021.
'''

print('----    PATH GENERATOR    ----\n')
dest = r"c:\Users\abram\Documents\IT\Major Project\Assets\Images\pathGenTesting"
dir = r"c:\Users\abram\Documents\IT\Major Project\Assets\Images\Sprites"
name = r"\generated45cropped.png"
angle = 23

flip = False
if angle < 0:
    print('Path angle inverted.')
    flip = True
    angle = angle * -1

with Image.open(dir + r"\basePath.png") as im:
        im = im.rotate(angle, expand=True)
        print('\nImage Rotated.')


imageWidth = im.width
imageHeight = im.height
pathWidth = 80
i = 0
height = -2

rgb_im = im.convert('RGBa')
print('Image Converted to RGBa.')

print('\nFinding black pixels on last line...')
print('Pixels found:')

# This one removes the edge on the bottom line
for x in range(imageWidth):
    r, g, b, a = rgb_im.getpixel((x, imageHeight-2))
    if a > 20:
        i = i + 1
        print(str(i) + ": " + str(r), str(g), str(b), str(a), str(x))
        left = x
        break

# This crop is to remove the left side of the image.
im = im.crop([left, 0, pathWidth + left, imageHeight])
rgb_im = im.convert('RGBa')
newWidth = im.width
i = 0


# Increment this counter every time you edit this function.
# Time wasted on this for loop: 4hr 15min
# This one removes the right column

print('\nFinding pixels on right column...')
print('Pixels found:')
for y in range(imageHeight):
    r, g, b, a = rgb_im.getpixel((newWidth - 1, y))
    if a > 20:
        i = i + 1
        print(str(i) + ": " + str(r), str(g), str(b), str(a), str(y))
        height = y
        break

print('\nCropping...')
im = im.crop([0, height, newWidth, imageHeight])

if flip == True:
    height = imageHeight
    print('\nTransposing for negative gradient...')

    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    
im.show()
print('Saving image to: ' + dest + name + "...\n\nFinished.\n")
im.save(dest + name)

