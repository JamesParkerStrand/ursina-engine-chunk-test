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

window.vsync = False

player = FirstPersonController( position=(0,2,0), gravity=0 )

plane = Entity(model="plane", texture="grass", scale=(200,1,200))

rows = 10
cols = 10

for x in range(rows):
    for z in range(cols):
        Entity(model="cube", position=(x * 8,0,z * 8), color=color.red)

chunks = dict()

for x in range(rows):
    for z in range(cols):
        chunks.update({(x,z): Chunk()})

playerXchunked = int((player.x / 8))
playerZchunked = int((player.z / 8))

lastplayerXchunked = int((player.x / 8))
lastplayerZchunked = int((player.z / 8))

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

chunksToWorkOn = []

chunkNow, chunkPrev = get_visible_chunks((playerXchunked, playerZchunked), (lastplayerXchunked, lastplayerZchunked))

workingOnChunks = True

DoneWithChunks = True

def update():
    global playerZchunked, playerXchunked, lastplayerXchunked, lastplayerZchunked, workingOnChunks, chunkNow, chunkPrev

    playerXchunked = int((player.x / 8))
    playerZchunked = int((player.z / 8))

    if (playerXchunked,playerZchunked) != (lastplayerXchunked, lastplayerZchunked) and workingOnChunks == False:
        workingOnChunks = True
        chunkNow, chunkPrev = get_visible_chunks((playerXchunked, playerZchunked), (lastplayerXchunked, lastplayerZchunked))
        lastplayerXchunked = playerXchunked
        lastplayerZchunked = playerZchunked

    #print(chunkNow, chunkPrev)

    if chunks[ (playerXchunked,playerZchunked) ].length != chunks[ (playerXchunked,playerZchunked) ].activelength:
        print("-- Insert Logic to Prevent player from either moving into the chunk or just pause player movement --")

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

chunks[ (playerXchunked,playerZchunked) ].appendBlock( position=(player.x,0.0,player.z),blockNumber=0 )
chunks[ (playerXchunked,playerZchunked) ].appendBlock( position=(player.x,0.0,player.z),blockNumber=0 )

def input(event):
    global playerZChunked, playerXChunked, workingOnChunks, workingOnSingleChunk
    if event == "b":
        if chunks.get( (playerXchunked,playerZchunked) ) != None:
            chunks[ (playerXchunked,playerZchunked) ].appendBlock( position=(player.x,0.0,player.z),blockNumber=0 )
            chunks[(playerXchunked, playerZchunked)].makeBlockActive()


app.run()