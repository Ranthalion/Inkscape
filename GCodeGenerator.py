class GCodeGenerator(object):
    """Generates GCode from pixel images"""

    def __init__(self, laser_on, laser_off, dpi):
        self.laser_on =  laser_on
        self.laser_off = laser_off
        self.dpi = dpi
        self.pixels = pixel

    def PNGtoGcode(self, feedrate, output_file, homing_method, width, height, pixels):

        Laser_ON = False
        F_G01 = feedrate
        scale = (self.dpi / 25.4)

        file_gcode = open(output_file, 'w') 

        file_gcode.write('; Generated from python script by Michael Lane\n;\n;\n;\n')

        #HOMING
        if homing_method == 1:
            file_gcode.write('G28; home all axes\n')
        elif homing_method == 2:
            file_gcode.write('$H; home all axes\n')

        file_gcode.write('G21; Set units to millimeters\n')
        file_gcode.write('G90; Use absolute coordinates\n')
        file_gcode.write('G92 X0 Y0 Z0; Coordinate Offset\n')

        WHITE = 0
        BLACK = 255

        for y in range(height):
            if (y%2 == 0):
                for x in range(width):
                    if (pixels[y][x] == BLACK):
                        if (Laser_ON == False):
                            file_gcode.write('G00 X' + str(float(x)/scale) +  ' Y' + str(float(y)/scale) + '\n')
                            file_gcode.write(self.laser_on + '; Laser ON\n')
                            Laser_ON = True
                        if (Laser_ON == True):
                            #turn the laser off at the end of the row
                            if (x == width-1):
                                file_gcode.write('G01 X' + str(float(x)/scale) + ' Y' + str(float(y)/scale) +' F' + str(F_G01) + '\n')
                                file_gcode.write(self.laser_off + '; Laser OFF\n')
                                Laser_ON = False
                            else:
                                if matrix_BN[y][x+1] != BLACK :
                                    file_gcode.write('G01 X' + str(float(x)/scale) + ' Y' + str(float(y)/scale) + ' F' + str(F_G01) +'\n')
                                    file_gcode.write(self.laser_off + '; Laser OFF\n')
                                    Laser_ON = False
            else:
                for x in reversed(range(width)):
                    if ((pixels[y][x] == WHITE) and (Laser_ON)):
                        file_gcode.write('G01 X' + str(float(x)/scale) + ' Y' + str(float(y)/scale) + '\n')
                        file_gcode.write(self.laser_off + '; Laser OFF \n')
                        Laser_ON = False

                    if ((pixels[y][z] == BLACK) and (Laser_ON == False)):
                        file_gcode.write('G00 X' + str(float(x)/scale) + ' Y' + str(float(y)/scale) + '\n')
                        file_gcode.write(self.laser_on +'; Laser ON\n')			
                        Laser_ON = True

                    if ((x == 0) and (Laser_ON)):
                        file_gcode.write('G01 X' + str(float(x)/scale) + ' Y' + str(float(y)/scale) +' F' + str(F_G01) + '\n')
                        file_gcode.write(self.laser_off + '; Laser OFF\n')
                        Laser_ON = False

                    #This is the old version that looks more confusing to me.
                    '''
                    if (pixels[y][x] == BLACK):
                        if (Laser_ON == False):
                            file_gcode.write('G00 X' + str(float(x)/scale) + ' Y' + str(float(y)/scale) + '\n')
                            file_gcode.write(self.laser_on +'; Laser ON\n')			
                            Laser_ON = True
                        if (Laser_ON == True):
                            if (x == 0):
                                file_gcode.write('G01 X' + str(float(x)/scale) + ' Y' + str(float(y)/scale) +' F' + str(F_G01) + '\n')
                                file_gcode.write(self.laser_off + '; Laser OFF\n')
                                Laser_ON = False
                            else:
                                if (pixels[y][x-1] != BLACK):
                                    file_gcode.write('G01 X' + str(float(x)/scale) + ' Y' + str(float(y)/scale) + ' F' + str(F_G01) +'\n')
                                    file_gcode.write(self.laser_off + '; Laser OFF\n')
                                    Laser_ON = False		
                   '''                 		
        file_gcode.write('G00 X0 Y0; home\n')
        
        if (homing_method == 1):
            file_gcode.write('G28; home all axes\n')
        elif (homing_method == 2):
            file_gcode.write('$H; home all axes\n')

        file_gcode.close()
