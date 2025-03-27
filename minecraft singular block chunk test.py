from ursina import *
import time

app = Ursina()

blocks = dict()

xRange = 35

yRange = 35

zRange = 35

#this is initialzing an array storing coordinates like to be able to index the blocks array by a y-axis, then all the x and z coordinates are then just scattered around
for x in range(xRange):
    for z in range(zRange):
        for y in range(yRange):
            blocks.update({(x,y,z) : 1})

# test to see if blocks modify correctly as it should.
#blocks.update({(0,0,0): 0})
#blocks.update({(0,1,0): 0})
#blocks.update({(0,2,0): 0})
#blocks.update({(1,2,0): 0})
#blocks.update({(0,4,0): 0})

def generateVertTOP(x, y, z):
    return [
        Vec3(x,1+y,z),
        Vec3(1+x,1+y,z),
        Vec3(1+x,1+y,1+z),
        Vec3(x,1+y,1+z)
    ]

def generateVertBOTTOM(x, y, z):
    return [
        Vec3(x, y, 1+z),
        Vec3(1+x, y, 1+z),
        Vec3(1+x,y,z),
        Vec3(x, y, z)
    ]

def generateVertBACK(x, y, z):
    return [
        Vec3(x, 1+y, 1+z),
        Vec3(1+x, 1+y, 1+z),
        Vec3(1+x,y,1+z),
        Vec3(x, y, 1+z)
    ]

def generateVertFRONT(x, y, z):
    return [
        Vec3(x,y,z),
        Vec3(1+x,y,z),
        Vec3(1+x,1+y,z),
        Vec3(x, 1+y, z),


    ]

def generateVertLEFT(x, y, z):
    return [
        Vec3(x, 1+y, 1+z),
        Vec3(x, y, 1+z),
        Vec3(x, y, z),
        Vec3(x, 1+y, z),
    ]

def generateVertRIGHT(x, y, z):
    return [
        Vec3(1+x, y, z),
        Vec3(1+x, y, 1+z),
        Vec3(1+x, 1+y, 1+z),
        Vec3(1+x, 1+y, z),
    ]

def generateUv():
    return [
        Vec2(0,0),
        Vec2(0,1),
        Vec2(1,1),
        Vec2(1,0)
    ]

#use it for looping in indexes
def generateConnection(indexedNumber):
    return [[0+indexedNumber*4,1+indexedNumber*4,2+indexedNumber*4],[3+indexedNumber*4,0+indexedNumber*4,2+indexedNumber*4]]


verts = []

uvs = []

connections = []

mesh = Mesh(vertices=verts, uvs=uvs, triangles=connections,mode='triangle')

quad_entity = Entity(
model = mesh,
texture = 'white_cube',
color = color.azure)

keyblocks = iter(blocks.keys())

def DictionaryLooper():
    global quad_entity, mesh
    destroy(quad_entity)
    verts = []

    uvs = []

    connections = []

    start_time = time.time()

    loopCounter = 0

    for i in blocks.keys():
        x = i[0]
        y = i[1]
        z = i[2]

        current = blocks.get((x, y, z))
        up = blocks.get((x, y + 1, z))
        down = blocks.get((x, y - 1, z))
        forward = blocks.get((x, y, z - 1))
        backward = blocks.get((x, y, z + 1))
        right = blocks.get((x + 1, y, z))
        left = blocks.get((x - 1, y, z))

        if current == 0:
            continue

        if down == 0 or down == None:
            verts.extend(generateVertBOTTOM(x, y, z))
            uvs.extend(generateUv())
            connections.extend(generateConnection(loopCounter))
            loopCounter += 1

        if up == 0 or up == None:
            verts.extend(generateVertTOP(x, y, z))
            uvs.extend(generateUv())
            connections.extend(generateConnection(loopCounter))
            loopCounter += 1

        if forward == 0 or forward == None:
            verts.extend(generateVertFRONT(x, y, z))
            uvs.extend(generateUv())
            connections.extend(generateConnection(loopCounter))
            loopCounter += 1

        if backward == 0 or backward == None:
            verts.extend(generateVertBACK(x, y, z))
            uvs.extend(generateUv())
            connections.extend(generateConnection(loopCounter))
            loopCounter += 1

        if right == 0 or right == None:
            verts.extend(generateVertRIGHT(x, y, z))
            uvs.extend(generateUv())
            connections.extend(generateConnection(loopCounter))
            loopCounter += 1

        if left == 0 or left == None:
            verts.extend(generateVertLEFT(x, y, z))
            uvs.extend(generateUv())
            connections.extend(generateConnection(loopCounter))
            loopCounter += 1



    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.6f} seconds")

    mesh = Mesh(vertices=verts, uvs=uvs, triangles=connections,mode='triangle')

    quad_entity = Entity(
    model = mesh,
    texture = 'white_cube',
    color = color.azure)

    print(len(mesh.vertices))

cube = Cube()

#TODO: you can experiment with the vertices to get the result of deleting blocks at a certain coordinate, right now it's a test.
def add():
    global mesh
    start_time = time.time()
    mesh.vertices.extend(cube.vertices)
    mesh.uvs.extend(cube.uvs)
    mesh.triangles.extend(cube.triangles)
    mesh.generate()
    print(len(mesh.vertices))
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.6f} seconds")

#test for quad generation for each side
'''
mesh2 = Mesh(vertices=generateVertFRONT(0,0,0), uvs=generateUv(), triangles=generateConnection(0),mode='triangle')

quad_entity = Entity(
model = mesh2,
texture = 'white_cube',
color = color.azure)
'''

processingVerts = False
loopCounter = 0
coordinateIterator = next(keyblocks, "end")

def update():
    global processingVerts, keyblocks, loopCounter, quad_entity, mesh, coordinateIterator
    #if processingVerts:
    #    x = next(keyblocks, "end")
    #    while x != "end":
    #        x = next(keyblocks, "end")
    #        print(x)
    #    processingVerts = False

    start_time = time.time()
    while coordinateIterator != "end":
        x = coordinateIterator[0]
        y = coordinateIterator[1]
        z = coordinateIterator[2]

        current = blocks.get((x, y, z))
        up = blocks.get((x, y + 1, z))
        down = blocks.get((x, y - 1, z))
        forward = blocks.get((x, y, z - 1))
        backward = blocks.get((x, y, z + 1))
        right = blocks.get((x + 1, y, z))
        left = blocks.get((x - 1, y, z))

        if current == 0:
            continue

        if down == 0 or down == None:
            verts.extend(generateVertBOTTOM(x, y, z))
            uvs.extend(generateUv())
            connections.extend(generateConnection(loopCounter))
            loopCounter += 1

        if up == 0 or up == None:
            verts.extend(generateVertTOP(x, y, z))
            uvs.extend(generateUv())
            connections.extend(generateConnection(loopCounter))
            loopCounter += 1

        if forward == 0 or forward == None:
            verts.extend(generateVertFRONT(x, y, z))
            uvs.extend(generateUv())
            connections.extend(generateConnection(loopCounter))
            loopCounter += 1

        if backward == 0 or backward == None:
            verts.extend(generateVertBACK(x, y, z))
            uvs.extend(generateUv())
            connections.extend(generateConnection(loopCounter))
            loopCounter += 1

        if right == 0 or right == None:
            verts.extend(generateVertRIGHT(x, y, z))
            uvs.extend(generateUv())
            connections.extend(generateConnection(loopCounter))
            loopCounter += 1

        if left == 0 or left == None:
            verts.extend(generateVertLEFT(x, y, z))
            uvs.extend(generateUv())
            connections.extend(generateConnection(loopCounter))
            loopCounter += 1
        coordinateIterator = next(keyblocks, "end")

        if coordinateIterator == "end":
            mesh.vertices = verts
            mesh.uvs = uvs
            mesh.triangles = connections
            mesh.generate()


        end_time = time.time()
        if end_time - start_time > 1/60:
            break


EditorCamera()

test = 0

def input(key):
    global keyblocks, processingVerts, loopCounter, coordinateIterator, verts, uvs, connections, test
    if key == "r":
        blocks.pop((test,0,0))
        test += 1

    if key == "g":
        DictionaryLooper()

    if key == "j":
        #destroy(quad_entity)
        verts = []

        uvs = []

        connections = []

        keyblocks = iter(blocks.keys())
        coordinateIterator = next(keyblocks, "end")
        processingVerts = True
        loopCounter = 0

app.run()