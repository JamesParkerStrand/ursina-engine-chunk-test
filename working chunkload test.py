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
        Entity(model="cube", position=(x * 8,0,z * 8))

chunks = dict()
chunksToChange = set()

for x in range(rows):
    for z in range(cols):
        chunks.update({(x,z): Chunk()})

print(chunks)

playerXchunked = int((player.x / 8))
playerZchunked = int((player.z / 8))

changes = [ (0,0) , (0,1), (0,-1), (1,0), (1,1), (1,-1), (-1,0) , (-1,1), (-1,-1) ]

def update():
    global playerZchunked, playerXchunked, chunksToChange
    playerXchunked = int((player.x / 8))
    playerZchunked = int((player.z / 8))

    chunksToNoLongerChange = []
    #print(chunksToNoLongerChange)
    for change in chunksToChange:
        #print(chunks[ (i[0] , i[1] ) ])
        chunks[ (change[0] , change[1] ) ].active = False
        if chunks[ (change[0] , change[1] ) ].activelength == 0:
            chunksToNoLongerChange.append((change[0] , change[1] ))


    #if (playerXchunked >= 0 and playerXchunked <= rows) and (playerZchunked >= 0 and playerZchunked <= cols):
        #chunksToChange.update( {(playerXchunked,playerZchunked)} )
        #chunks[(playerXchunked, playerZchunked)].active = True

    #if chunks.get( (playerXchunked,playerZchunked) ) != None:
        #print(playerXchunked,playerZchunked)
        #chunks[(playerXchunked, playerZchunked)].makeBlockActive()
    #    chunksToChange.update( {(playerXchunked,playerZchunked)} )
    #    chunks[(playerXchunked, playerZchunked)].active = True

    for signIteration in range(5):
        print(signIteration, 8-signIteration)
        coordinate = changes[signIteration]
        coordinate2 = changes[8-signIteration]

        if signIteration == 4:
            if chunks.get((playerXchunked + coordinate[0], playerZchunked + coordinate[1])) != None:
                chunksToChange.update({(playerXchunked + coordinate[0], playerZchunked + coordinate[1] )})
                chunks[(playerXchunked + coordinate[0], playerZchunked + coordinate[1])].active = True
            break

        if chunks.get((playerXchunked + coordinate[0], playerZchunked + coordinate[1])) != None:
            chunksToChange.update({(playerXchunked + coordinate[0], playerZchunked + coordinate[1])})
            chunks[(playerXchunked + coordinate[0], playerZchunked + coordinate[1])].active = True

        if chunks.get((playerXchunked + coordinate2[0], playerZchunked + coordinate2[1])) != None:
            chunksToChange.update({(playerXchunked + coordinate2[0], playerZchunked + coordinate2[1])})
            chunks[(playerXchunked + coordinate2[0], playerZchunked + coordinate2[1])].active = True

    for removalSet in chunksToNoLongerChange:
        if chunks[ (removalSet[0],removalSet[1]) ].active == False:
            chunksToChange.remove( (removalSet[0],removalSet[1]) )

    for i in chunksToChange:
        if chunks[(i[0],i[1])].active == True:
            chunks[(i[0], i[1])].makeBlockActive()
        else:
            chunks[(i[0], i[1])].makeBlockInActive()





def input(event):
    global playerZChunked, playerXChunked
    if event == "b":
        if chunks.get( (playerXchunked,playerZchunked) ) != None:
            chunks[ (playerXchunked,playerZchunked) ].appendBlock( position=(player.x,0.0,player.z),blockNumber=0 )

app.run()