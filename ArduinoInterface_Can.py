#Autor: Can Cetin, 12/3
import serial
import time
import math

class ArduinoInterface:

    port = '/dev/serial/by-path/platform-3f980000.usb-usb-0:1.3:1.0'  # Port Oben Rechts!!
    s = serial.Serial(port, 9600)
    x2 = 507.2
    y3 = 507.2

    def __init__(self):
    # Python Konstruktor
        self.s.close()

    def getData(self):
    #Empfängt die Daten vom Arduino

        self.s.open()
        time.sleep(5)

        self.s.write("Start".encode())
        micData = 0
        try:
            print("Waiting for Response...")
            micData = self.s.readline()
            micData = str(micData)
            self.s.close()

        except KeyboardInterrupt:
            self.s.close()

        micData = micData.replace("b\'", "")
        micData = micData.replace("\\r\\n\'", "")
        d1, d2, d3 = micData.split()
        x0, y0 = self.dataProcessing(d1, d2, d3)
        return x0, y0

    def dataProcessing(self, d1, d2, d3):
    # Die Gleichung, die die Koordinaten des Dartpfeils berechnet
        d0 = -1 / 2 * (
                (d1 ** 3 - d1 ** 2 * d3 - d1 * d3 ** 2 + d3 ** 3) * self.x2 ** 2 + (
                d1 ** 3 - d1 ** 2 * d2 - d1 * d2 ** 2 + d2 ** 3 - (
                d2 + d3) * self.x2 ** 2) * self.y3 ** 2 + math.sqrt(
            -d1 ** 4 * d2 ** 2 + 2 * d1 ** 3 * d2 ** 3 - d1 ** 2 * d2 ** 4 - (
                    d1 ** 2 - 2 * d1 * d2 + d2 ** 2) * d3 ** 4 - (
                    d1 ** 2 - 2 * d1 * d3 + d3 ** 2) * self.x2 ** 4 - (
                    d1 ** 2 - 2 * d1 * d2 + d2 ** 2 - self.x2 ** 2) * self.y3 ** 4 + 2 * (
                    d1 ** 3 - d1 ** 2 * d2 - d1 * d2 ** 2 + d2 ** 3) * d3 ** 3 - (
                    d1 ** 4 + 2 * d1 ** 3 * d2 - 6 * d1 ** 2 * d2 ** 2 + 2 * d1 * d2 ** 3 + d2 ** 4) * d3 ** 2 + (
                    d1 ** 4 - 2 * d1 ** 3 * d2 + 2 * d1 ** 2 * d2 ** 2 - 2 * (
                    d1 + d2) * d3 ** 3 + d3 ** 4 + 2 * (
                            d1 ** 2 + d1 * d2 + d2 ** 2) * d3 ** 2 - 2 * (
                            d1 ** 3 - d1 ** 2 * d2 + 2 * d1 * d2 ** 2) * d3) * self.x2 ** 2 + (
                    d1 ** 4 - 2 * d1 ** 3 * d2 + 2 * d1 ** 2 * d2 ** 2 - 2 * d1 * d2 ** 3 + d2 ** 4 + self.x2 ** 4 + 2 * (
                    d1 ** 2 - 2 * d1 * d2 + d2 ** 2) * d3 ** 2 - 2 * (
                            d1 ** 2 - d1 * d2 + d2 ** 2 - (
                            d1 + d2) * d3 + d3 ** 2) * self.x2 ** 2 - 2 * (
                            d1 ** 3 - d1 ** 2 * d2 - d1 * d2 ** 2 + d2 ** 3) * d3) * self.y3 ** 2 + 2 * (
                    d1 ** 4 * d2 - d1 ** 3 * d2 ** 2 - d1 ** 2 * d2 ** 3 + d1 * d2 ** 4) * d3) * self.x2 * self.y3) / (
                     (d1 ** 2 - 2 * d1 * d3 + d3 ** 2) * self.x2 ** 2 + (
                     d1 ** 2 - 2 * d1 * d2 + d2 ** 2 - self.x2 ** 2) * self.y3 ** 2)

        x0 = (self.x2 ** 2 + (d0 + d1) ** 2 - (d0 + d2) ** 2) / (2 * self.x2)

        y0 = math.sqrt((d0 + d1) ** 2 - x0 ** 2)

        return x0, y0



