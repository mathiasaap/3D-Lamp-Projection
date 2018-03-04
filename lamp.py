from PIL import Image
#im = Image.open("moon_small.jpeg")
im = Image.open("star.png")
width, height = im.size
print(width)

projected = Image.new('RGB', (width, height), (255, 0, 0))
projectedPixels = projected.load()

def getPictureCoordinates(pixel_coords, image_size, picture_size):
    x, y = pixel_coords[0], pixel_coords[1]
    w, h = image_size[0], image_size[1]

    return ((x/w) - 0.5) * picture_size, ((y/h) - 0.5) * picture_size

def getSpherePointForPictureCoordinate(x, y, z, r):
    k = r/((x**2 + y**2 + z**2))**0.5
    return k*x, k*y, k*z

def PILImageCoordsFromSphere(spherePoint, imageSize):
    x = 0.4* spherePoint[0] * imageSize[0] + 0.5 * imageSize[0]
    y = 0.4* spherePoint[1] * imageSize[1] + 0.5 * imageSize[1]
    return x,y


triangles = []
indices = []
coords2Index = {}
coords2IndexInner = {}

coords2IndexEdge = {}
coords2IndexInnerEdge = {}
currentIndex = 1

sphere_r = 1
#image_size = sphere_r * 15
#vertical_dist = sphere_r * 12

image_size = sphere_r * 5
vertical_dist = sphere_r * 3
COLOR_THRESHOLD = 200
THINNESS = 0.96
EDGE_LENGTH = 0.10

def checkAndAddTriangle(location):
    global currentIndex
    global coords2Index
    global coords2IndexInner
    global triangles

    if location not in coords2Index:
        x_1, y_1 = getPictureCoordinates(location, im.size, image_size)
        sx, sy, sz = getSpherePointForPictureCoordinate(x_1, y_1, vertical_dist, sphere_r)
        triangles.append((sx, sy, sz))
        coords2Index[location] = currentIndex
        currentIndex += 1

        sx, sy, sz = getSpherePointForPictureCoordinate(x_1, y_1, vertical_dist, sphere_r * THINNESS)
        triangles.append((sx, sy, sz))
        coords2IndexInner[location] = currentIndex
        currentIndex += 1

def checkAndAddTriangleEdge(location):
    global currentIndex
    global coords2IndexEdge
    global coords2IndexInnerEdge
    global triangles

    if location not in coords2IndexEdge:
        x_1, y_1 = getPictureCoordinates(location, im.size, image_size)
        sx, sy, sz = getSpherePointForPictureCoordinate(x_1, y_1, vertical_dist, sphere_r)
        triangles.append((sx, sy, sz - EDGE_LENGTH))
        coords2IndexEdge[location] = currentIndex
        currentIndex += 1

        sx, sy, sz = getSpherePointForPictureCoordinate(x_1, y_1, vertical_dist, sphere_r * THINNESS)
        triangles.append((sx, sy, sz - EDGE_LENGTH * THINNESS))
        coords2IndexInnerEdge[location] = currentIndex
        currentIndex += 1




for x in range(width):
    for y in range(height):
        if x>0 and y >0:
            pixel_origin = im.getpixel((x, y))
            pixel_up = im.getpixel((x, y-1))
            pixel_left = im.getpixel((x-1, y))
            pixel_leftup = im.getpixel((x-1, y-1))
            checkAndAddTriangle((x,y))
            checkAndAddTriangle((x,y-1))
            checkAndAddTriangle((x-1,y))
            checkAndAddTriangle((x-1,y-1))
            """
            if sum(pixel_origin) < COLOR_THRESHOLD and  sum(pixel_up) < COLOR_THRESHOLD and sum(pixel_left) < COLOR_THRESHOLD:
                indices.append((coords2Index[(x,y)], coords2Index[(x,y-1)], coords2Index[(x-1,y)]))
                indices.append((coords2IndexInner[(x,y)], coords2IndexInner[(x,y-1)], coords2IndexInner[(x-1,y)]))
            else:
                pass

                if sum(pixel_up) >= COLOR_THRESHOLD:
                    indices.append((coords2Index[(x,y)], coords2Index[(x,y-1)], coords2IndexInner[(x,y)]))
                    indices.append((coords2IndexInner[(x,y)], coords2IndexInner[(x,y-1)], coords2Index[(x,y-1)]))

                if sum(pixel_left) >= COLOR_THRESHOLD:
                    indices.append((coords2Index[(x,y)], coords2Index[(x-1,y)], coords2IndexInner[(x,y)]))
                    indices.append((coords2IndexInner[(x,y)], coords2IndexInner[(x-1,y)], coords2Index[(x-1,y)]))

            """
            if sum(pixel_origin) < COLOR_THRESHOLD :
                indices.append((coords2Index[(x,y)], coords2Index[(x,y-1)], coords2Index[(x-1,y)]))
                indices.append((coords2IndexInner[(x,y)], coords2IndexInner[(x,y-1)], coords2IndexInner[(x-1,y)]))

                if sum(pixel_up) >= COLOR_THRESHOLD:
                    indices.append((coords2Index[(x,y)], coords2Index[(x,y-1)], coords2IndexInner[(x,y)]))
                    indices.append((coords2IndexInner[(x,y)], coords2IndexInner[(x,y-1)], coords2Index[(x,y-1)]))

                if sum(pixel_left) >= COLOR_THRESHOLD:
                    indices.append((coords2Index[(x,y)], coords2Index[(x-1,y)], coords2IndexInner[(x,y)]))
                    indices.append((coords2IndexInner[(x,y)], coords2IndexInner[(x-1,y)], coords2Index[(x-1,y)]))





        else:
            if x <= 0 and y > 0:
                checkAndAddTriangle((x,y))
                checkAndAddTriangle((x,y-1))
                checkAndAddTriangleEdge((x,y))
                checkAndAddTriangleEdge((x,y-1))

                indices.append((coords2Index[(x,y)], coords2Index[(x,y-1)], coords2IndexEdge[(x,y)]))
                indices.append((coords2IndexEdge[(x,y)], coords2IndexEdge[(x,y-1)], coords2Index[(x,y-1)]))

                indices.append((coords2IndexInner[(x,y)], coords2IndexInner[(x,y-1)], coords2IndexInnerEdge[(x,y)]))
                indices.append((coords2IndexInnerEdge[(x,y)], coords2IndexInnerEdge[(x,y-1)], coords2IndexInner[(x,y-1)]))

                indices.append((coords2IndexEdge[(x,y)], coords2IndexEdge[(x,y-1)], coords2IndexInnerEdge[(x,y)]))
                indices.append((coords2IndexInnerEdge[(x,y)], coords2IndexInnerEdge[(x,y-1)], coords2IndexEdge[(x,y-1)]))


            if y <= 0 and x > 0:
                checkAndAddTriangle((x,y))
                checkAndAddTriangle((x-1,y))
                checkAndAddTriangleEdge((x,y))
                checkAndAddTriangleEdge((x-1,y))

                indices.append((coords2Index[(x,y)], coords2Index[(x-1,y)], coords2IndexEdge[(x,y)]))
                indices.append((coords2IndexEdge[(x,y)], coords2IndexEdge[(x-1,y)], coords2Index[(x-1,y)]))

                indices.append((coords2IndexInner[(x,y)], coords2IndexInner[(x-1,y)], coords2IndexInnerEdge[(x,y)]))
                indices.append((coords2IndexInnerEdge[(x,y)], coords2IndexInnerEdge[(x-1,y)], coords2IndexInner[(x-1,y)]))

                indices.append((coords2IndexEdge[(x,y)], coords2IndexEdge[(x-1,y)], coords2IndexInnerEdge[(x,y)]))
                indices.append((coords2IndexInnerEdge[(x,y)], coords2IndexInnerEdge[(x-1,y)], coords2IndexEdge[(x-1,y)]))





        if x < width -1 and y < height -1:
            pixel_origin = im.getpixel((x, y))
            pixel_down = im.getpixel((x, y+1))
            pixel_right = im.getpixel((x+1, y))
            pixel_rightdown = im.getpixel((x+1, y+1))
            checkAndAddTriangle((x,y))
            checkAndAddTriangle((x,y+1))
            checkAndAddTriangle((x+1,y))
            checkAndAddTriangle((x+1,y+1))



            if sum(pixel_origin) < COLOR_THRESHOLD :
                coords2Index[(x,y)]
                coords2Index[(x,y+1)]
                coords2Index[(x+1,y)]
                indices.append((coords2Index[(x,y)], coords2Index[(x,y+1)], coords2Index[(x+1,y)]))
                indices.append((coords2IndexInner[(x,y)], coords2IndexInner[(x,y+1)], coords2IndexInner[(x+1,y)]))

                if sum(pixel_down) >= COLOR_THRESHOLD:
                    indices.append((coords2Index[(x,y)], coords2Index[(x,y+1)], coords2IndexInner[(x,y)]))
                    indices.append((coords2IndexInner[(x,y)], coords2IndexInner[(x,y+1)], coords2Index[(x,y+1)]))

                if sum(pixel_right) >= COLOR_THRESHOLD:
                    indices.append((coords2Index[(x,y)], coords2Index[(x+1,y)], coords2IndexInner[(x,y)]))
                    indices.append((coords2IndexInner[(x,y)], coords2IndexInner[(x+1,y)], coords2Index[(x+1,y)]))


                """
            if sum(pixel_origin) < COLOR_THRESHOLD and sum(pixel_down) < COLOR_THRESHOLD and sum(pixel_right) < COLOR_THRESHOLD:
                indices.append((coords2Index[(x,y)], coords2Index[(x,y+1)], coords2Index[(x+1,y)]))
                indices.append((coords2IndexInner[(x,y)], coords2IndexInner[(x,y+1)], coords2IndexInner[(x+1,y)]))

            else:
                pass

                if sum(pixel_down) >= COLOR_THRESHOLD:
                    indices.append((coords2Index[(x,y)], coords2Index[(x,y+1)], coords2IndexInner[(x,y)]))
                    indices.append((coords2IndexInner[(x,y)], coords2IndexInner[(x,y+1)], coords2Index[(x,y+1)]))

                if sum(pixel_right) >= COLOR_THRESHOLD:
                    indices.append((coords2Index[(x,y)], coords2Index[(x+1,y)], coords2IndexInner[(x,y)]))
                    indices.append((coords2IndexInner[(x,y)], coords2IndexInner[(x+1,y)], coords2Index[(x+1,y)]))
                """

        else:
            if x >= width -1 and y < height -1:
                checkAndAddTriangle((x,y))
                checkAndAddTriangle((x,y+1))
                checkAndAddTriangleEdge((x,y))
                checkAndAddTriangleEdge((x,y+1))

                indices.append((coords2Index[(x,y)], coords2Index[(x,y+1)], coords2IndexEdge[(x,y)]))
                indices.append((coords2IndexEdge[(x,y)], coords2IndexEdge[(x,y+1)], coords2Index[(x,y+1)]))

                indices.append((coords2IndexInner[(x,y)], coords2IndexInner[(x,y+1)], coords2IndexInnerEdge[(x,y)]))
                indices.append((coords2IndexInnerEdge[(x,y)], coords2IndexInnerEdge[(x,y+1)], coords2IndexInner[(x,y+1)]))

                indices.append((coords2IndexEdge[(x,y)], coords2IndexEdge[(x,y+1)], coords2IndexInnerEdge[(x,y)]))
                indices.append((coords2IndexInnerEdge[(x,y)], coords2IndexInnerEdge[(x,y+1)], coords2IndexEdge[(x,y+1)]))

            if y >= height -1 and x < width -1:
                checkAndAddTriangle((x,y))
                checkAndAddTriangle((x+1,y))
                checkAndAddTriangleEdge((x,y))
                checkAndAddTriangleEdge((x+1,y))

                indices.append((coords2Index[(x,y)], coords2Index[(x+1,y)], coords2IndexEdge[(x,y)]))
                indices.append((coords2IndexEdge[(x,y)], coords2IndexEdge[(x+1,y)], coords2Index[(x+1,y)]))

                indices.append((coords2IndexInner[(x,y)], coords2IndexInner[(x+1,y)], coords2IndexInnerEdge[(x,y)]))
                indices.append((coords2IndexInnerEdge[(x,y)], coords2IndexInnerEdge[(x+1,y)], coords2IndexInner[(x+1,y)]))

                indices.append((coords2IndexEdge[(x,y)], coords2IndexEdge[(x+1,y)], coords2IndexInnerEdge[(x,y)]))
                indices.append((coords2IndexInnerEdge[(x,y)], coords2IndexInnerEdge[(x+1,y)], coords2IndexEdge[(x+1,y)]))



def createObj(triangles, indices):
    objectStr = "#Triangles\n\n"
    for triangle in triangles:
        objectStr += "v {:.6f} {:.6f} {:.6f}\n".format(triangle[0], triangle[1], triangle[2])
    objectStr += "\n\n#Indices\n\n"
    for index in indices:
        objectStr += "f {} {} {}\n".format(str(index[0]), str(index[1]), str(index[2]))

    return objectStr

objectData = createObj(triangles, indices)
with open("small_star.obj", 'w') as file:
    file.write(objectData)




        #outX_origin, outY_origin = PILImageCoordsFromSphere((sx, sy, sz), im.size)
        #print(outX, outY)
        #projectedPixels[outX, outY] = im.getpixel((x, y))

#projected.show()
