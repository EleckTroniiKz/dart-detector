#Autor: Can Cetin, 12/3
import math

class Location:  # Hier wird durch den Satz des Pythagoras und if-else berechnet, welche Punktzahl gerade geworfen wurde
    x0 = 85
    y0 = 85

    def findQuadrant(self, x, y):
        #Schaut in welchem Quadrant von der Dartscheibe sich der Dartpfeil befindet
        entity = ""
        segment = 0
        if x > self.x0 and y > self.y0:
            entity, segment = self.quadrantOne(x, y)
        elif x < self.x0 and y > self.y0:
            entity, segment = self.quadrantTwo(x, y)
        elif x < self.x0 and y < self.y0:
            entity, segment = self.quadrantThree(x, y)
        elif x > self.x0 and y < self.y0:
            entity, segment = self.quadrantFour(x, y)

        return entity, segment

    def quadrantOne(self, x, y):
        # Für den Fall, wenn sich der Dart im ersten Quadrant befindet (oberes rechtes Viertel der Dartscheibe)
        dx = x - self.x0
        dy = y - self.y0
        c = ((dx ** 2) + (dy ** 2)) ** 0.5
        tan = math.degrees(math.atan(dy / dx))
        print("Tan q1: " + str(tan))
        if c < 15.9:
            self.checkGeneral(c, tan)
        else:
            entity, segment = self.qOnePoints(tan, c)
            return entity, segment

    def quadrantTwo(self, x, y):
        # Für den Fall, wenn sich der Dart im zweiten Quadrant befindet (oberes linkes Viertel der Dartscheibe)
        dx = self.x0 - x
        dy = y - self.y0
        c = ((dx ** 2) + (dy ** 2)) ** 0.5
        tan = math.degrees(math.atan(dy / dx))
        print("Tan q2: " + str(tan))
        if c < 15.9:
            self.checkGeneral(c, tan)
        else:
            entity, segment = self.qTwoPoints(tan, c)
            return entity, segment

    def quadrantThree(self, x, y):
        # Für den Fall, wenn sich der Dart im dritten Quadrant befindet (unteres linkes Viertel der Dartscheibe)
        dx = self.x0 - x
        dy = self.y0 - y
        c = ((dx ** 2) + (dy ** 2)) ** 0.5
        tan = math.degrees(math.atan(dy / dx))
        print("Tan q3: " + str(tan))
        if c < 15.9:
            self.checkGeneral(c)
        else:
            entity, segment = self.qThreePoints(tan, c)
            return entity, segment

    def quadrantFour(self, x, y):
        # Für den Fall, wenn sich der Dart im vierten Quadrant befindet (unteres rechtes Viertel der Dartscheibe)
        dx = x - self.x0
        dy = self.y0 - y
        c = ((dx ** 2) + (dy ** 2)) ** 0.5
        tan = math.degrees(math.atan(dy / dx))
        print("Tan q4: " + str(tan))
        if c < 15.9:
            self.checkGeneral(c, tan)
        else:
            entity, segment = self.qFourPoints(tan, c)
            return entity, segment

    def qOnePoints(self, degrees, c):
        # Segmentzuordnung mit Winkel und Entfernung zur Mitte im ersten Quadrant
        if degrees <= 90 and degrees >= 81:  # 20
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                entity = "Single"
                segment = 20
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 20")
                entity = "Double"
                segment = 20
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 20")
                entity = "Triple"
                segment = 20
                return entity, segment
        elif degrees <= 81 and degrees >= 63:  # 1
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 1")
                entity = "Single"
                segment = 1
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 1")
                entity = "Double"
                segment = 1
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 1")
                entity = "Triple"
                segment = 1
                return entity, segment
        elif degrees <= 45 and degrees >= 27:  # 4
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 4")
                entity = "Single"
                segment = 4
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 4")
                entity = "Double"
                segment = 4
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 4")
                entity = "Triple"
                segment = 4
                return entity, segment
        elif degrees <= 9 and degrees >= 0:  # 6
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 6")
                entity = "Single"
                segment = 6
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 6")
                entity = "Double"
                segment = 6
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 6")
                entity = "Triple"
                segment = 6
                return entity, segment
        elif degrees <= 27 and degrees >= 9:  # 13
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 13")
                entity = "Single"
                segment = 13
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 13")
                entity = "Double"
                segment = 13
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 13")
                entity = "Triple"
                segment = 13
                return entity, segment
        elif degrees <= 63 and degrees >= 45:  # 18
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 18")
                entity = "Single"
                segment = 18
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 18")
                entity = "Double"
                segment = 18
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 18")
                entity = "Triple"
                segment = 18
                return entity, segment
        else:
            print("Q1")
            print("FEHLER: Irgendwo muss es einen Fehler geben.")
            print("Schau nochm al in den Gleichungen oder du hast die IFs hier falsch eingeordnet oder sö")

    def qTwoPoints(self, degrees, c):
        # Segmentzuordnung mit Winkel und Entfernung zur Mitte im zweiten Quadrant
        if degrees <= 81 and degrees >= 63:  # 5
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 5")
                entity = "Single"
                segment = 5
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 5")
                entity = "Double"
                segment = 5
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 5")
                entity = "Triple"
                segment = 5
                return entity, segment
        elif degrees <= 45 and degrees >= 27:  # 9
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 9")
                entity = "Single"
                segment = 9
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 9")
                entity = "Double"
                segment = 9
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 9")
                entity = "Triple"
                segment = 9
                return entity, segment
        elif degrees <= 9 and degrees >= 0:  # 11
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 11")
                entity = "Single"
                segment = 11
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 11")
                entity = "Double"
                segment = 11
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 11")
                entity = "Triple"
                segment = 11
                return entity, segment
        elif degrees <= 63 and degrees >= 45:  # 12
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 12")
                entity = "Single"
                segment = 12
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 12")
                entity = "Double"
                segment = 12
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 12")
                entity = "Triple"
                segment = 12
                return entity, segment
        elif degrees <= 27 and degrees >= 9:  # 14
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 14")
                entity = "Single"
                segment = 14
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 14")
                entity = "Double"
                segment = 14
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 14")
                entity = "Triple"
                segment = 14
                return entity, segment
        elif degrees <= 90 and degrees >= 81:  # 20
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 20")
                entity = "Single"
                segment = 20
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 20")
                entity = "Double"
                segment = 20
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 20")
                entity = "Triple"
                segment = 20
                return entity, segment
        else:
            print("Q2")
            print("FEHLER: Irgendwo muss es einen Fehler geben.")
            print("Schau nochm al in den Gleichungen oder du hast die IFs hier falsch eingeordnet oder sö")

    def qThreePoints(self, degrees, c):
        # Segmentzuordnung mit Winkel und Entfernung zur Mitte im dritten Quadrant
        if degrees <= 9 and degrees >= 0:  # 3
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 3")
                entity = "Single"
                segment = 3
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 3")
                entity = "Double"
                segment = 3
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 3")
                entity = "Triple"
                segment = 3
                return entity, segment
        elif degrees <= 45 and degrees >= 27:  # 7
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 7")
                entity = "Single"
                segment = 7
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 7")
                entity = "Double"
                segment = 7
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 7")
                entity = "Triple"
                segment = 7
                return entity, segment
        elif degrees <= 81 and degrees >= 63:  # 8
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 8")
                entity = "Single"
                segment = 8
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 8")
                entity = "Double"
                segment = 8
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 8")
                entity = "Triple"
                segment = 8
                return entity, segment
        elif degrees <= 90 and degrees >= 81:  # 11
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 11")
                entity = "Single"
                segment = 11
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 11")
                entity = "Double"
                segment = 11
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 11")
                entity = "Triple"
                segment = 11
                return entity, segment
        elif degrees <= 63 and degrees >= 45:  # 16
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 16")
                entity = "Single"
                segment = 16
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 16")
                entity = "Double"
                segment = 16
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 16")
                entity = "Triple"
                segment = 16
                return entity, segment
        elif degrees <= 27 and degrees >= 9:  # 19
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 19")
                entity = "Single"
                segment = 19
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 19")
                entity = "Double"
                segment = 19
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 19")
                entity = "Triple"
                segment = 19
                return entity, segment
        else:
            print("Q3")
            print("FEHLER: Irgendwo muss es einen Fehler geben.")
            print("Schau nochm al in den Gleichungen oder du hast die IFs hier falsch eingeordnet oder sö")

    def qFourPoints(self, degrees, c):
        # Segmentzuordnung mit Winkel und Entfernung zur Mitte im vierten Quadrant
        if degrees <= 45 and degrees >= 27:  # 2
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 2")
                entity = "Single"
                segment = 2
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 2")
                entity = "Double"
                segment = 2
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 2")
                entity = "Triple"
                segment = 2
                return entity, segment
        elif degrees <= 9 and degrees >= 0:  # 3
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 3")
                entity = "Single"
                segment = 3
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 3")
                entity = "Double"
                segment = 3
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 3")
                entity = "Triple"
                segment = 3
                return entity, segment
        elif degrees <= 90 and degrees >= 81:  # 6
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 6")
                entity = "Single"
                segment = 6
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 6")
                entity = "Double"
                segment = 6
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 6")
                entity = "Triple"
                segment = 6
                return entity, segment
        elif degrees <= 81 and degrees >= 63:  # 10
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 10")
                entity = "Single"
                segment = 10
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 10")
                entity = "Double"
                segment = 10
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 10")
                entity = "Triple"
                segment = 10
                return entity, segment
        elif degrees <= 63 and degrees >= 45:  # 15
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 15")
                entity = "Single"
                segment = 15
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 15")
                entity = "Double"
                segment = 15
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 15")
                entity = "Triple"
                segment = 15
                return entity, segment
        elif degrees <= 27 and degrees >= 9:  # 17
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                print("Single 17")
                entity = "Single"
                segment = 17
                return entity, segment
            elif c >= 162 and c <= 170:
                print("Double 17")
                entity = "Double"
                segment = 17
                return entity, segment
            elif c >= 101 and c <= 109:
                print("Triple 17")
                entity = "Triple"
                segment = 17
                return entity, segment
        else:
            print("Q4")
            print("FEHLER: Irgendwo muss es einen Fehler geben.")
            print("Schau nochm al in den Gleichungen oder du hast die IFs hier falsch eingeordnet oder sö")

    def controlGeneral(self, c):
        # Der Fall, dass der Dart entweder ausserhalb der Dartscheibe oder innerhalb vom Bull landet
        if c < 15.9 and c > 6.35:
            entity = "Bull"
            point = 25
            return entity, point
        elif c < 6.35 and c > 0.1:
            entity = "Bullseye"
            point = 50
            return entity, point
        elif c > 170:
            entity = "empty"
            point = 0
            return entity, point
