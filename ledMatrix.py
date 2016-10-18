import serial, json, time, traceback, pprint, array



class LedMatrix():

    # This is a simple one-color version LedMatrix handler class

    black = [0, 0, 0]
    red = [255, 0, 0]
    green = [0, 255, 0]
    blue = [0, 0, 255]


    count = 0 #debug

    def __init__(self, matrix_width=15, matrix_height=8):
        self.matrix_width = matrix_width
        self.matrix_height = matrix_height
        self.serial_port = None

        #initialize matrix
        self.initializeMatrix()



        # load letters matrices
        f = open("pismena.json")
        self.letters = json.load(f)
        f.close()



    def openPort(self, port_name="/dev/ttyUSB0", baudrate=115200):
        try:
            self.serial_port = serial.Serial(port_name, baudrate=baudrate)
            return True
        except:
            traceback.print_exc()
            return False


    def closePort(self):
        #print "closing port"
        self.serial_port.close()



    def initializeMatrix(self):
        self.matrix = [[0 for x in range(self.matrix_width)] for y in range(self.matrix_height)]



    def sendMatrixDataToPanel(self):
        dataToSend = []

        for line in self.matrix:
            line.reverse()
            dataToSend += line



        dataToSend += [10]   # ending byte


        bytesToSend = array.array('B', dataToSend)

        self.serial_port.write(bytesToSend)
        time.sleep(0.02)
        #print self.count
        self.count += 1



    def writeToMatrix(self, text, shift_x=1, shift_y=0):
        self.initializeMatrix() # clear matrix

        current_position_x = shift_x
        current_position_y = shift_y

        for letter in text:
            if not letter in self.letters:
                print "Cannot find letter %s in letter json file!" % (letter)
                continue

            for yplus, letter_line in enumerate(self.letters[letter]):
                letter_width = len(letter_line)

                for xplus, pixel in enumerate(letter_line):
                    position_x, position_y = current_position_x + xplus, current_position_y + yplus

                    #print position_x, position_y, pixel

                    if self.isPositionInMatrix(position_x, position_y):
                        self.matrix[position_y][position_x] = pixel



            current_position_x += letter_width + 1




    def isPositionInMatrix(self, position_x, position_y):
        # returns whether specified position is in bound of current matrix
        if position_x >= 0 and position_x < self.matrix_width and position_y >= 0 and position_y < self.matrix_height:
            return True
        return False





if __name__ == "__main__":
    ledMatrix = LedMatrix(matrix_width=15, matrix_height=8)






