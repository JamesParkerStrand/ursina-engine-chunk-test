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
        self.activelength += 1
        if self.activelength <= self.length:
            self.activeBlocks.append( Entity(model="cube",position=self.blockValues[self.activelength - 1][0] ))
        else:
            self.activelength = self.length

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

def get_visible_chunks(pos):
    ChunkPositions = set()
    for signIteration in range(5):

        coordinate = signchanges[signIteration]
        coordinate2 = signchanges[8-signIteration]

        playerXchunked = pos[0]
        playerZchunked = pos[1]

        chunkExists = chunks.get((playerXchunked + coordinate[0], playerZchunked + coordinate[1]))
        chunkExistsOtherSide = chunks.get((playerXchunked + coordinate2[0], playerZchunked + coordinate2[1])) != None

        if signIteration == 4:
            if chunkExists:
                ChunkPositions.update( {(playerXchunked + coordinate[0], playerZchunked + coordinate[1] )} )
            break

        if chunkExists:
            ChunkPositions.update( {(playerXchunked + coordinate[0], playerZchunked + coordinate[1])} )

        if chunkExistsOtherSide:
            ChunkPositions.update( {(playerXchunked + coordinate2[0], playerZchunked + coordinate2[1])} )


    return ChunkPositions

throwAwayChunks = set()

#find whether or not a certain item can be found, if not, throw it into the pile of chunks to degenerate, if item found as the other one, do not throw it away, generate with it
def ChunksToDeGenerate(prevChunkRecord, NewChunkRecord):
    global throwAwayChunks

    for i in prevChunkRecord:
        if i not in NewChunkRecord:
            throwAwayChunks.update({(i[0],i[1])})



def update():
    global playerZchunked, playerXchunked, lastplayerXchunked, lastplayerZchunked
    playerXchunked = int((player.x / 8))
    playerZchunked = int((player.z / 8))

    chunkNow = get_visible_chunks((playerXchunked,playerZchunked))
    for i in chunkNow:
        chunks[( i[0],i[1] )].makeBlockActive()
        if i in throwAwayChunks:
            throwAwayChunks.remove(i)
    chunkPrev = get_visible_chunks((lastplayerXchunked, lastplayerZchunked))

    ChunksToDeGenerate(chunkPrev, chunkNow)


    ChunkToDelete = []
    for i in throwAwayChunks:
        chunks[(i[0], i[1])].makeBlockInActive()
        if chunks[(i[0], i[1])].activelength == 0:
            ChunkToDelete.append(i)

    for i in ChunkToDelete:
        throwAwayChunks.remove(i)

    lastplayerZchunked = playerZchunked
    lastplayerXchunked = playerXchunked

    print("chunkPrev: ",chunkPrev)
    print("chunkNow: ",chunkNow)
    print("throwaway: ",throwAwayChunks)

def input(event):
    global playerZChunked, playerXChunked
    if event == "b":
        if chunks.get( (playerXchunked,playerZchunked) ) != None:
            chunks[ (playerXchunked,playerZchunked) ].appendBlock( position=(player.x,0.0,player.z),blockNumber=0 )


app.run()