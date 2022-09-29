from .Utilities import *

class MDL():

    def __init__(self) -> None:
        
        self.meshes = []

    class HEADER():

        def __init__(self) -> None:
            
            self.offsets = []

        def read(self, br):

            count = br.readUShort()
            br.readUShort()
            for i in range(count):
                self.offsets.append(br.readInt())

    class MESH():

        def __init__(self) -> None:

            self.dataLength = 0
            
            self.positions = []
            self.texCoords = []
            self.normals = []
            self.colors = []

            self.faces = []
            self.facesDir = []

        def read(self, br):

            test = 0

            self.dataLength = br.readUInt()
            self.dataLength = (self.dataLength & 0x7FFF) * 16 + 16 + br.tell() - 4 

            order = "positions"
            index = 0

            while(br.tell() < self.dataLength):
                
                IMMEDIATE = br.readUShort()
                NUM = br.readUByte()
                CMD = br.readUByte()

                if CMD == 1:
                    cl = IMMEDIATE & 0xFF
                    wl = (IMMEDIATE >> 8) & 0xFF
                    continue
                
                elif CMD == 17:
                    continue
                
                elif CMD & 0x60 == 0x60:

                    # unpack command
                    mask = ((CMD & 0x10) == 0x10)
                    vn = (CMD >> 2) & 3
                    vl = CMD & 3
                    addr = IMMEDIATE & 0x1ff
                    flag = (IMMEDIATE & 0x8000) == 0x8000
                    usn = (IMMEDIATE & 0x4000) == 0x4000

                    if CMD == 0x68:

                        for i in range(NUM):
                        
                            if order == "positions":
                                self.positions.append([br.readFloat(), br.readFloat(), br.readFloat()])
                                order = "normals"
                                
                            elif order == "normals":
                                self.normals.append([br.readFloat(), br.readFloat(), br.readFloat()])
                                if IMMEDIATE == 32770:
                                    order = "colors"
                                else:
                                    order = "uvs"
                            
                            elif order == "colors":
                                self.colors.append([br.readUInt(), br.readUInt(), br.readUInt()])
                                order = "uvs"

                            elif order == "uvs":
                                self.texCoords.append([br.readFloat(), br.readFloat(), br.readFloat()])
                                order = "positions"

                    elif CMD == 0x6C:
                        for i in range(NUM):
                            br.readBytes(16)

                    elif CMD == 0x70:

                        for i in range(NUM):
                            br.readBytes(4)

                    elif CMD == 0x72:

                        for i in range(NUM):

                            flag = br.readByte()                 

                            if int(bin(flag)[-1]) == 1:
                                self.faces.append(0xFFFF)
                                if flag != 33:
                                    self.facesDir.append(index)                            
                            self.faces.append(index)
                            index += 1

                        br.seek(((NUM + 3) & ~3) - NUM, 1)

                #print(br.tell())

            br.seek(self.dataLength, 0)

            print("END : " + str(br.tell()))

    def read(self, br):

        header = MDL.HEADER()
        header.read(br)

        for offset in header.offsets:

            if offset != -1:

                br.seek(offset, 0)
                
                mesh = MDL.MESH()
                mesh.read(br)

                self.meshes.append(mesh)



