from gl import Renderer, color, V3, V2
import random

width = 960
height = 540

rend = Renderer(width, height)

# StarField
for x in range(width):
    for y in range(height):
        if random.random() > 0.999:
            size = random.randrange(0, 4)
            brightness = random.random() / 2 + 0.5
            starColor = color(brightness, brightness, brightness)

            if size == 0:
                rend.glPoint(x, y, starColor)
            if size == 1:
                rend.glPoint(x, y, starColor)
                rend.glPoint(x+1, y, starColor)
                rend.glPoint(x+1, y+1, starColor)
                rend.glPoint(x, y+1, starColor)
            if size == 2:
                rend.glPoint(x, y, starColor)
                rend.glPoint(x, y+1, starColor)
                rend.glPoint(x, y-1, starColor)
                rend.glPoint(x+1, y, starColor)
                rend.glPoint(x-1, y, starColor)

            if size == 3:
                rend.glPoint(x, y, starColor)
                rend.glPoint(x+1, y, starColor)
                rend.glPoint(x, y+1, starColor)
                rend.glPoint(x+1, y+1, starColor)
                rend.glPoint(x+2, y, starColor)
                rend.glPoint(x+2, y+1, starColor)
                rend.glPoint(x, y+2, starColor)
                rend.glPoint(x+1, y+2, starColor)
                rend.glPoint(x+2, y+2, starColor)
                rend.glPoint(x-1, y+1, starColor)
                rend.glPoint(x+3, y+1, starColor)
                rend.glPoint(x+1, y-1, starColor)
                rend.glPoint(x+1, y+3, starColor)
                rend.glPoint(x-2, y+1, starColor)
                rend.glPoint(x+4, y+1, starColor)
                rend.glPoint(x+1, y-2, starColor)
                rend.glPoint(x+1, y+4, starColor)
            if size == 4:
                rend.glPoint(x, y, starColor)
                rend.glPoint(x+1, y, starColor)
                rend.glPoint(x, y+1, starColor)
                rend.glPoint(x+1, y+1, starColor)
                rend.glPoint(x+2, y, starColor)
                rend.glPoint(x+2, y+1, starColor)
                rend.glPoint(x, y+2, starColor)
                rend.glPoint(x+1, y+2, starColor)
                rend.glPoint(x+2, y+2, starColor)
                rend.glPoint(x-1, y+1, starColor)
                rend.glPoint(x+3, y+1, starColor)
                rend.glPoint(x+1, y-1, starColor)
                rend.glPoint(x+1, y+3, starColor)
                rend.glPoint(x-2, y+1, starColor)
                rend.glPoint(x+4, y+1, starColor)
                rend.glPoint(x+1, y-2, starColor)
                rend.glPoint(x+1, y+4, starColor)
                rend.glPoint(x-3, y+1, starColor)
                rend.glPoint(x+5, y+1, starColor)
                rend.glPoint(x+1, y-3, starColor)
                rend.glPoint(x+1, y+5, starColor)

# Floor

pol1 = [V2(0, 0), V2(width, 0), V2(width, height/4), V2(0, height/4)]
rend.glFill(pol1, color(0.65, 0.36, 0.03))

rend.glLoadModel("catmodel.obj",
                 translate=V3(width/2, height/5, 0),
                 scale=V3(10, 10, 10))

rend.glFinish("output.bmp")
