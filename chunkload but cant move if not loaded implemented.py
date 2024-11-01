from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class Chunk():
    def __init__(self):

        self.colors = {0:color.white}

        self.blockValues = []
        self.length = 0
        self.activelength = 0

        self.activeBlocks = []

        self.active = False

    def appendBlock(self, position, blockNumber):
        self.blockValues.append( (position, blockNumber) )
        self.length += 1

    def makeBlockActive(self):
        if self.activelength < self.length:
            self.activelength += 1
            self.activeBlocks.append( Entity(model="cube",position=self.blockValues[self.activelength - 1][0] ))

    def makeBlockInActive(self):
        if self.activelength > 0:
            destroy(self.activeBlocks[self.activelength - 1])
            del self.activeBlocks[self.activelength - 1]
            self.activelength -= 1

app = Ursina()

chunksize = 8

window.vsync = False

player = FirstPersonController( position=(0,2,0), gravity=0 )

plane = Entity(model="plane", texture="grass", scale=(200,1,200))

rows = 10
cols = 10

for x in range(rows):
    for z in range(cols):
        Entity(model="sphere", scale=0.3,position=(x * chunksize,0,z * chunksize), color=color.red)

chunks = dict()

for x in range(rows):
    for z in range(cols):
        chunks.update({(x,z): Chunk()})

playerXchunked = int((player.x / chunksize))
playerZchunked = int((player.z / chunksize))

lastplayerXchunked = int((player.x / chunksize))
lastplayerZchunked = int((player.z / chunksize))

signchanges = [ (0,0) , (0,1), (0,-1), (1,0), (1,1), (1,-1), (-1,0) , (-1,1), (-1,-1) ]

def get_visible_chunks(pos, pos2):
    ChunkPositions = set()
    prevChunkPositions = set()
    for signIteration in range(5):

        coordinate = signchanges[signIteration]
        coordinate2 = signchanges[8-signIteration]

        playerXchunked = pos[0]
        playerZchunked = pos[1]

        lastplayerXchunked = pos2[0]
        lastplayerZchunked = pos2[1]

        chunkExists = chunks.get((playerXchunked + coordinate[0], playerZchunked + coordinate[1]))
        chunkExistsOtherSide = chunks.get((playerXchunked + coordinate2[0], playerZchunked + coordinate2[1]))

        chunkExists2 = chunks.get((lastplayerXchunked + coordinate[0], lastplayerZchunked + coordinate[1]))
        chunkExistsOtherSide2 = chunks.get((lastplayerXchunked + coordinate2[0], lastplayerZchunked + coordinate2[1]))

        if signIteration == 4:

            if chunkExists:

                ChunkPositions.update( { (playerXchunked + coordinate[0], playerZchunked + coordinate[1] ) } )

            if chunkExists2:
                prevChunkPositions.update( { (lastplayerXchunked + coordinate[0], lastplayerZchunked + coordinate[1]) } )

            break

        if chunkExists:

            ChunkPositions.update( { (playerXchunked + coordinate[0], playerZchunked + coordinate[1]) } )

        if chunkExists2:

            prevChunkPositions.update( { (lastplayerXchunked + coordinate[0], lastplayerZchunked + coordinate[1]) } )

        if chunkExistsOtherSide:

            ChunkPositions.update( { (playerXchunked + coordinate2[0], playerZchunked + coordinate2[1]) } )

        if chunkExistsOtherSide2:

            prevChunkPositions.update( { (lastplayerXchunked + coordinate2[0], lastplayerZchunked + coordinate2[1]) } )



    return ChunkPositions, prevChunkPositions

chunkNow, chunkPrev = get_visible_chunks((playerXchunked, playerZchunked), (lastplayerXchunked, lastplayerZchunked))

workingOnChunks = True

lastplayerx = 2
lastplayerz = 6

player.x = 10
player.z = 10

#Entity(model="sphere", position=(lastplayerx,0,lastplayerz), color=color.yellow)
#Entity(model="sphere", position=(player.x,0,player.z), color=color.white)

def update():
    global playerZchunked, playerXchunked, lastplayerXchunked, lastplayerZchunked, workingOnChunks, chunkNow, chunkPrev, lastplayerx, lastplayerz

    playerXchunked = int((player.x / chunksize))
    playerZchunked = int((player.z / chunksize))

    if (playerXchunked,playerZchunked) != (lastplayerXchunked, lastplayerZchunked) and workingOnChunks == False:
        workingOnChunks = True
        chunkNow, chunkPrev = get_visible_chunks((playerXchunked, playerZchunked), (lastplayerXchunked, lastplayerZchunked))
        lastplayerXchunked = playerXchunked
        lastplayerZchunked = playerZchunked

    if chunks[ (playerXchunked,playerZchunked) ].length != chunks[ (playerXchunked,playerZchunked) ].activelength:
        print("-- Insert Logic to Prevent player from either moving into the chunk --")
        boxCollider = Entity(model="cube", position=(
        (playerXchunked * chunksize) + chunksize / 2, 0, (playerZchunked * chunksize) + chunksize / 2), scale=(chunksize + 0.2, 1, chunksize + 0.2),
                      color=color.blue, collider="box")

        differenceX = lastplayerx - player.x
        differenceZ = lastplayerz - player.z

        ray = raycast(origin=(player.x,0,player.z),direction= (differenceX,0,differenceZ),distance=100,debug=True )

        destroy(boxCollider)

        #Entity(model="sphere", position=ray.world_point)


        player.x = ray.world_point[0]
        player.z = ray.world_point[2]
        if chunks[(int((player.x / chunksize)), int((player.z / chunksize)))].length != chunks[(int((player.x / chunksize)), int((player.z / chunksize)))].activelength:
            boxCollider = Entity(model="cube", position=(( int((lastplayerx / chunksize)) * chunksize) + chunksize / 2, 0, (int((lastplayerz / chunksize)) * chunksize) + chunksize / 2),scale=(chunksize -0.2, 1, chunksize - 0.2),color=color.blue, collider="box")
            ray = raycast(origin=(player.x, 0, player.z), direction=(differenceX, 0, differenceZ), distance=100,
                          debug=True)
            destroy(boxCollider)

            player.x = ray.world_point[0]
            player.z = ray.world_point[2]

            #Entity(model="sphere", position=ray.world_point)


    lastplayerx = player.x
    lastplayerz = player.z

    if workingOnChunks:
        workingOnChunks = False
        for i in chunkNow:
            if i in chunkPrev:
                chunkPrev.remove(i)
            chunks[i].makeBlockActive()
            if chunks[i].activelength != chunks[i].length:
                workingOnChunks = True
        for j in chunkPrev:
            chunks[j].makeBlockInActive()
            if chunks[j].activelength != 0:
                workingOnChunks = True

chunks[ (1,1) ].appendBlock( position=(12,0.0,12),blockNumber=0 )
chunks[ (1,1) ].appendBlock( position=(12,0.0,12),blockNumber=0 )
chunks[ (1,1) ].appendBlock( position=(12,0.0,12),blockNumber=0 )
chunks[ (1,1) ].appendBlock( position=(12,0.0,12),blockNumber=0 )

def input(event):
    global playerZChunked, playerXChunked, workingOnChunks, workingOnSingleChunk
    if event == "b":
        if chunks.get( (playerXchunked,playerZchunked) ) != None:
            chunks[ (playerXchunked,playerZchunked) ].appendBlock( position=(player.x,0.0,player.z),blockNumber=0 )
            chunks[(playerXchunked, playerZchunked)].makeBlockActive()


app.run()