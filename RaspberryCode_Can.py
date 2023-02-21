#Autor: Can Cetin, 12/3
import serial
import math
import time

class Game:
    players = []
    playerPoints = []
    actPlayer = 1
    game = True
    dartCount = 0

    startingEntity = []

    tripleIn = False
    doubleIn = False

    straightOut = False
    doubleOut = False
    masterOut = False

    gameContinue = False

    pointsBackUp = 0
    lastThrow = ""

    s = [0] * 20
    d = [0] * 20
    t = [0] * 20

    scoreboard = [["Players  ", "Throw1", "Throw2", "Throw3", "Score"]]
    playersThrows = [0, 0, 0]
    playersEntity = ["empty", "empty", "empty"]
    playersWon = []

    nameSet = False

    def __init__(self):
        #Python Konstruktor
        self.askrules()
        self.createplayers()
        self.choosemode()
        self.possiblepoints()
        self.process()
    #End of __init__

    def process(self):
        # Spielverlauf vom Dart Spiel
        arduino = ArduinoInterface()
        locate = Location()
        while self.game:

            if self.gameContinue:
                if self.game == False:
                    break

            for a in range(3):
                print("Punkte von Spieler " + str(self.actPlayer) + ": " + str(self.playerPoints[self.actPlayer - 1]))

                d1 = int(input("Geben Sie den d1-Wert an:  "))
                d2 = int(input("Geben Sie den d2-Wert an:  "))
                d3 = int(input("Geben Sie den d3-Wert an:  "))

                x0, y0 = arduino.dataProcessing(d1, d2, d3)
                e, p = locate.findQuadrant(x0, y0)

                self.playersThrows[a] = p
                self.playersEntity[a] = e
                self.throwdart(p, e)
                self.checkrules(self.playersThrows[0], self.playersEntity[0], self.playersThrows[1],
                                self.playersEntity[1], self.playersThrows[2], self.playersEntity[2])

    # End of process

    def possiblepoints(self):
        # Füllt die 3 leeren Listen s, d und t mit den Single, Double und Triple Werten der Segmente
        for a in range(20):
            self.s[a] = 1 * a + 1
            self.d[a] = 2 * a + 2
            self.t[a] = 3 * a + 3
    # End of possiblepoints

    def createplayers(self):
        # Fragt die Anzahl der Spieler ab und kreiert die benötigten Listen für Punkte, etc
        playernumber = int(input("Wie viele Leute spielen mit?"))

        self.players = [0] * playernumber
        self.playerPoints = [0] * playernumber
        self.startingEntity = [0] * playernumber

        askforname = input("Möchten Sie für jeden Spieler die Namen eintragen?")
        # Bei Bedarf kann man hier die Spieler benennen
        if self.checkuserdecision(askforname):
            self.nameSet = True
            for a in range(len(self.players)):
                name = input("Name von Spieler " + str(a + 1) + "?")
                self.players[a] = name
        elif not self.checkuserdecision(askforname):
            for i in range(len(self.players)):
                self.players[i] = "Spieler " + str(1 + i)
                #print(str(self.players[i]))
    # End of createplayers

    def choosemode(self):
        # Spielmodus-Wahl: 301, 501, 601
        choosenMode = int(input("Welchen Spielemodus möchten Sie spielen?\n (301/501/601) ?"))
        if choosenMode == 301 or choosenMode == 501 or choosenMode == 601:
            self.setplayerpoints(choosenMode)
        else:
            print("Bitte wählen Sie nur einen von diesen Modi aus: 301, 501 oder 601!")
            self.choosemode()
    # End of choosenMode

    def setplayerpoints(self, mode):
        # Spieler bekommen die Startpunktzahl zugewiesen
        for i in range(len(self.players)):
            self.playerPoints[i] = mode
    # END of setplayerpoints

    def throwdart(self, n, e):
        # Rechnung für den Dartwurf
        t = self.checkdart(n, e)
        print("Dartwert von Wurf "+ str(self.dartCount + 1) +": "+ str(t)) #Dient zur Kontrolle, ob die Funktion checkDart() funktioniert hat

        self.playerPoints[self.actPlayer - 1] = self.playerPoints[self.actPlayer - 1] - float(t)
        print("Punkte von " + self.players[self.actPlayer - 1] + " nach Wurf Nummer " + str(self.dartCount + 1) + "!")
        print(str(self.playerPoints[self.actPlayer - 1]))
        print("")
    # END of throwdart

    def checkdart(self, t, e):
        # Wert der angegebenen Entität und des Segmentes wird hier kontrolliert
        if t == 25 and e == "Bull":
            return 25.0
        elif t == 50 and e == "Bullseye":
            return 50.0
        elif t == 0 and e == "empty":
            return 0
        elif isinstance(t, int) == False:
            return 0
        else:
            if t >= 21 or t < 0:
                return 0
            elif t >= 1 and t <= 20:
                if e == "Single" or e == "single" or e.startswith("s") or e.startswith("S"):
                    if self.startingEntity[self.actPlayer - 1] == 0 and self.doubleIn:
                        return 0

                    elif self.startingEntity[self.actPlayer - 1] == 0 and self.tripleIn:
                        return 0

                    elif self.startingEntity[self.actPlayer - 1] == 1:
                        return self.s[t - 1]

                    elif not self.tripleIn and not self.doubleIn:
                        return self.s[t - 1]

                    return self.s[t - 1]

                elif e == "Double" or e == "double" or e.startswith("d") or e.startswith("D"):
                    if self.startingEntity[self.actPlayer - 1] == 0 and self.doubleIn:
                        self.startingEntity[self.actPlayer - 1] = 1
                        return self.d[t - 1]

                    elif self.startingEntity[self.actPlayer - 1] == 0 and self.tripleIn:
                        return 0

                    elif self.startingEntity[self.actPlayer - 1] == 1:
                        return self.d[t - 1]

                    elif not self.tripleIn and not self.doubleIn:
                        return self.d[t - 1]

                elif e == "Triple" or e == "triple" or e.startswith("t") or e.startswith("T"):
                    if self.startingEntity[self.actPlayer - 1] == 0 and self.doubleIn:
                        return 0

                    elif self.startingEntity[self.actPlayer - 1] == 0 and self.tripleIn:
                        self.startingEntity[self.actPlayer - 1] = 1
                        return self.t[t - 1]

                    elif self.startingEntity[self.actPlayer - 1] == 1:
                        return self.t[t - 1]

                    elif not self.tripleIn and not self.doubleIn:
                        return self.t[t - 1]

                else:
                    return 0
    # END of checkdart

    def checkuserdecision(self, phrase):
        # Stringeingaben Kontrolle
        if phrase == "Yes" or phrase == "yes" or phrase == "Y" or phrase == "y" or phrase == "Ja" or phrase == "ja" \
                or phrase == "J" or phrase == "j" or phrase == "yepp" or phrase == "Yepp" or phrase == "jope" \
                or phrase == "Jope":
            return True
        elif phrase == "No" or phrase == "no" or phrase == "Nein" or phrase == "nein" or phrase == "N" or phrase == "n" \
                or phrase == "Nope" or phrase == "nope" or phrase == "Nee" or phrase == "nee":
            return False
        else:
            print("Wir haben das nicht ganz Verstanden. Wir nehmen an Sie wollen nicht mit der Regelung spielen")
            return False
    # END of checkuserdecision

    def checkrules(self, n1, e1, n2, e2, n3, e3):
        # Kontrolliert, ob alle Regeln eingehalten werden, die am Anfang vom Spiel eingestellt wurden
        if self.straightOut:
            self.lastThrow = e1
            points1 = self.checkdart(n1, e1)

            if n2 != 0 and e2 != "empty":
                points2 = self.checkdart(n2, e2)
                self.lastThrow = e2
            else:
                points2 = 0

            if n3 != 0 and e3 != "empty":
                points3 = self.checkdart(n3, e3)

                self.lastThrow = e3
            else:
                points3 = 0

            self.pointsBackUp = points1 + points2 + points3
            #print("Points BackUp:   " + str(self.pointsBackUp))

            if self.playerPoints[self.actPlayer - 1] < 0:
                if self.doubleOut or self.masterOut:
                    print(
                        "Sie müssen genau auf 0 kommen, sodass Sie gewinnen. Die letzten Würfe werden nicht gezählt.\n")
                    self.playerPoints[self.actPlayer - 1] = self.playerPoints[self.actPlayer - 1] + self.pointsBackUp
                    print("Ihre aktuelle Punktzahl: " + str(self.playerPoints[self.actPlayer - 1]))
                    self.changedartcount(True)

                elif not self.doubleOut:
                    print("Sie müssen genau auf 0 kommen, sodass Sie gewinnen.\n"
                          + "Ihre letzten drei Würfe werden nicht gezählt.")
                    self.playerPoints[self.actPlayer - 1] = self.playerPoints[self.actPlayer - 1] + self.pointsBackUp
                    print("Ihre aktuelle Punktzahl: " + str(self.playerPoints[self.actPlayer - 1]))
                    self.changedartcount(True)

            elif self.playerPoints[self.actPlayer - 1] == 0:
                if self.doubleOut:
                    if self.lastThrow == "Double" or self.lastThrow == "double" or self.lastThrow.startswith("d"):
                        print("Herzlichen Glückwunsch Spieler " + str(self.actPlayer) + ". Sie haben gewonnen!")
                        self.checkcontinuegame()
                    elif self.lastThrow == "Bullseye":
                        print("Herzlichen Glückwunsch Spieler " + str(self.actPlayer) + ". Sie haben gewonnen!")
                        self.checkcontinuegame()
                    else:
                        print("Sie müssen genau auf 0 kommen und dies mit einem Double Wurf")
                        self.playerPoints[self.actPlayer - 1] = self.playerPoints[
                                                                    self.actPlayer - 1] + self.pointsBackUp
                        print("Neue Punktzahl =" + str(self.playerPoints[self.actPlayer - 1]))
                        self.changedartcount(True)
                elif self.masterOut:
                    if self.lastThrow == "Triple" or self.lastThrow == "triple" or self.lastThrow.startswith("t"):
                        print("Herzlichen Glückwunsch Spieler " + str(self.actPlayer) + ". Sie haben gewonnen!")
                        self.checkcontinuegame()
                    else:
                        print("Sie müssen genau auf 0 kommen und dies mit einem Triple Wurf")
                        self.playerPoints[self.actPlayer - 1] = self.playerPoints[
                                                                    self.actPlayer - 1] + self.pointsBackUp
                        print("Neue Punktzahl =" + str(self.playerPoints[self.actPlayer - 1]))
                        self.changedartcount(True)
                elif not self.doubleOut and not self.masterOut:
                    print("Herzlichen Glückwunsch Spieler " + str(self.actPlayer) + ". Sie haben gewonnen!")
                    self.checkcontinuegame()
            else:
                self.changedartcount(False)

        elif not self.straightOut:
            if self.playerPoints[self.actPlayer - 1] <= 0:
                print("Herzlichen Glückwunsch Spieler " + str(self.actPlayer) + ". Sie haben gewonnen!")
                self.fillscoreboard()
                self.checkcontinuegame()

                if self.gameContinue:
                    self.gameContinue = False
            self.changedartcount(False)
    # End of checkrules

    def changedartcount(self, bool):
        # Ändert die Dart Nummer (max.3)
        if not bool:
            self.dartCount += 1
            if self.dartCount == 3:
                self.dartCount = 0
                self.fillscoreboard()
                self.changeplayer()
        elif bool:
            self.dartCount = 0
            self.fillscoreboard()
            self.changeplayer()
    # End of changedartcount

    def changeplayer(self):
        # Ändert den Spieler
        self.actPlayer += 1

        if self.actPlayer > len(self.players):
            self.actPlayer = 1
            self.pausescoreboard()
            print("")
        print("")

        if self.playerPoints[self.actPlayer - 1] <= 0 and self.actPlayer in self.playersWon:
            print(self.players[self.actPlayer - 1] + " wird übersprungen. Er ist schon fertig.")
            self.changeplayer()
        else:
            print(self.players[self.actPlayer - 1] + " ist an der Reihe!")

        for a in range(3):
            self.playersThrows[a] = 0
            self.playersEntity[a] = "empty"
        self.pointsBackUp = 0
        self.lastThrow = ""
    # End of changeplayer

    def checkcontinuegame(self):
        # Userabfrage, ob Sie weiterspielen möchten. Dies wird abgefragt, nachdem ein Spieler null erreicht

        self.playersWon.append(self.actPlayer)
        self.checkoneplayerleft()

        askPlayers = input("Möchten die Spieler, die noch nicht auf 0 gekommen sind, weiterspielen??")
        self.gameContinue = self.checkuserdecision(askPlayers)
        if self.gameContinue:
            self.game = True
            self.changedartcount(True)
            self.process()
        elif not self.gameContinue:
            self.game = False
            print("Spiel beendet")
            exit()
    # END of checkcontinuegame

    def askrules(self):
        # Fragt die User nach den Regeln, mit denen Sie spielen wollen

        tripleInAsk = input("Triple In: Ja/Nein?")
        self.tripleIn = self.checkuserdecision(tripleInAsk)
        if not self.tripleIn:
            doubleInAsk = input("Double In: Ja/Nein")
            self.doubleIn = self.checkuserdecision(doubleInAsk)

        masterOutAsk = input("Master Out: Ja/Nein?")
        self.masterOut = self.checkuserdecision(masterOutAsk)
        if self.masterOut:
            self.straightOut = True
        elif not self.masterOut:
            doubleOutAsk = input("Double Out : Ja/Nein?")
            self.doubleOut = self.checkuserdecision(doubleOutAsk)
            if self.doubleOut:
                self.straightOut = True
            elif not self.doubleOut:
                straightOutAsk = input("Straight Out : Ja/Nein?")
                self.straightOut = self.checkuserdecision(straightOutAsk)
    # END of askrules

    def checkstopgame(self, phrase):
        # Kontrolliert ob als Entity End oder ähnliches eingegeben wurde. Wenn ja, wird das Spiel direkt beendet
        if phrase == "end" or phrase == "End" or phrase == "stop" or \
                phrase == "Stop" or phrase == "Ende" or phrase == "ende":
            self.game = False
            #("Spiel wurde beended")
            return True
        elif phrase == "restart":
            self.restartgame()
        else:
            return False
    # END of checkstopgame

    def checkInput(self, a):
        # Kontrolliert, ob die Zeichen in der Eingabe auch Zahlen sind. Falls nicht -> return 0
        if a.isalpha():
            return 0
        elif int(a) % 1 == 0:
            return a
        else:
            return 0
    # End of checkInput

    def fillscoreboard(self):
        # Füllt und aktualisiert das Scoreboard mit den Werten der Spieler
        d = " "

        t = [str(self.checkdart(self.playersThrows[0], self.playersEntity[0])),
             str(self.checkdart(self.playersThrows[1], self.playersEntity[1])),
             str(self.checkdart(self.playersThrows[2], self.playersEntity[2]))]
        a = [0, 0, 0]
        score = str(self.playerPoints[self.actPlayer - 1])

        for i in range(3):
            length = len(t[i])
            n = 6 - length
            a[i] = " " * n + t[i]

        length = len(score)
        n = 6 - length
        d = " " * n + score

        z = 0
        if self.nameSet:
            length = len(self.players[self.actPlayer - 1])
            z = 20 - length
            self.scoreboard[0] = ["Spieler" + " " * 12, "Wurf 1", "Wurf 2", "Wurf 4", "Punkte"]
        self.scoreboard.append([str(self.players[self.actPlayer - 1]) + " " * z, a[0], a[1], a[2], d])
    # End of fillscoreboard

    def pausescoreboard(self):
        # Gibt eine Trennlinie aus, um so das lesen des Scoreboards zu erleichtern
        m = 48
        if self.nameSet:
            m = 59
        self.scoreboard.append(["_" * m])
    # End of pausescoreboard

    def checkoneplayerleft(self):
        # Kontrolliert ob nur noch ein Spieler die 0 nicht erreicht hat. Falls Ja wird das Spiel beendet
        if len(self.playersWon) == (len(self.players) - 1):
            self.gameContinue = False
            self.game = False
            print("Das Spiel ist vorbei. Hier der Punktestand")
            s = input("Möchten Sie nochmal spielen?")
            if self.checkuserdecision(s):
                self.restartgame()
            elif not self.checkuserdecision(s):
                print("Spiel wurde beended")
                exit()
    # End of checkoneplayerleft

    def restartgame(self):
        # Falls das Spiel Neu gestartet wird, werden hier alle Werte auf die Standard-Anfangswerte zurückgesetzt
        self.dartCount = 0
        self.actPlayer = 1
        self.game = True

        self.straightOut = False
        self.doubleOut = False

        self.tripleIn = False
        self.doubleIn = False
        self.gameContinue = False

        self.startingEntity = []

        self.pointsBackUp = 0
        self.lastThrow = ""
        self.scoreboard = [["Spieler", "Wurf 1", "Wurf 2", "Wurf 3", "Punkte"]]
        self.playersWon = []
        self.playersThrows = [0, 0, 0]
        self.playersEntity = ["empty", "empty", "empty"]
        self.nameSet = False

        print("Spiel wurde zurück gesetzt!")
        self.__init__()
    # End of restartgame

class ArduinoInterface:
    #port = '/dev/serial/by-path/platform-3f980000.usb-usb-0:1.3:1.0'  # Port Oben Rechts!!
    #s = serial.Serial(port, 9600)
    x2 = 450  # x-Koordinate des Mikrofons auf der x-Achse
    y3 = 450  # y-Koordinate des Mikrofons auf der y-Achse


    #def __init__(self):
        #self.s.close()

    def getData(self):

        self.s.open()
        time.sleep(5)

        self.s.write("Start".encode())
        micData = 0
        try:
            print("Waiting for Response...")
            micData = self.s.readline()
            print(micData)
            micData = str(micData)
            self.s.close()

        except KeyboardInterrupt:
            self.s.close()

        micData = micData.replace("b\'", "")
        micData = micData.replace("\\r\\n\'", "")
        d1, d2, d3 = micData.split()
        d1 = float(d1)
        d2 = float(d2)
        d3 = float(d3)

        x0, y0 = self.dataProcessing(d1, d2, d3)
        return x0, y0

    def dataProcessing(self, d1, d2, d3):
        try:
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

        ##print("x0: " + str(x0))
        ##print("y0: " + str(y0))

            return x0, y0
        except:
            #print("FEHLER IN DER GLEICHUNG!")
            #print("Line 603 - 628")
            return 0, 0

class Location:  # Hier wird durch den Satz des Pythagoras und if-else berechnet, welche Punktzahl gerade geworfen wurde
    x0 = 225  # x-Koordinate des Mittelpunktes
    y0 = 225  # y-Kooridante des Mittelpunktes

    def findQuadrant(self, x, y):
        entity = ""
        segment = 0
        if x > self.x0 and y > self.y0:
            ##print("QUADRANT 1 ")
            entity, segment = self.quadrantOne(x, y)
        elif x < self.x0 and y > self.y0:
            ##print("QUADRANT 2 ")
            entity, segment = self.quadrantTwo(x, y)
        elif x < self.x0 and y < self.y0:
            ##print("QUADRANT 3 ")
            entity, segment = self.quadrantThree(x, y)
        elif x > self.x0 and y < self.y0:
            ##print("QUADRANT 4 ")
            entity, segment = self.quadrantFour(x, y)

        return entity, segment

    def quadrantOne(self, x, y):
        # Für den Fall, wenn sich der Dart im ersten Quadrant befindet (oberes rechtes Viertel der Dartscheibe)
        dx = x - self.x0
        dy = y - self.y0
        c = ((dx ** 2) + (dy ** 2)) ** 0.5
        tan = math.degrees(math.atan(dy / dx))
        ##print("Tan q1: " + str(tan))
        if c < 15.9:
            self.controlGeneral(c, tan)
        elif c > 170:
            return "empty", 0
        else:
            entity, segment = self.qOnePoints(tan, c)
            return entity, segment

    def quadrantTwo(self, x, y):
        # Für den Fall, wenn sich der Dart im zweiten Quadrant befindet (oberes linkes Viertel der Dartscheibe)
        dx = self.x0 - x
        dy = y - self.y0
        c = ((dx ** 2) + (dy ** 2)) ** 0.5
        tan = math.degrees(math.atan(dy / dx))
        ##print("Tan q2: " + str(tan))
        if c < 15.9:
            self.controlGeneral(c, tan)
        elif c > 170:
            return "empty", 0
        else:
            entity, segment = self.qTwoPoints(tan, c)
            return entity, segment

    def quadrantThree(self, x, y):
        # Für den Fall, wenn sich der Dart im dritten Quadrant befindet (unteres linkes Viertel der Dartscheibe)
        dx = self.x0 - x
        dy = self.y0 - y
        c = ((dx ** 2) + (dy ** 2)) ** 0.5
        tan = math.degrees(math.atan(dy / dx))
        #print("C          " + str(c))
        ##print("Tan q3: " + str(tan))
        if c < 15.9:
            entity, segment = self.controlGeneral(c)
            return entity, segment
        elif c > 170:
            return "empty", 0
        else:
            entity, segment = self.qThreePoints(tan, c)
            return entity, segment

    def quadrantFour(self, x, y):
        # Für den Fall, wenn sich der Dart im vierten Quadrant befindet (unteres rechtes Viertel der Dartscheibe)
        dx = x - self.x0
        dy = self.y0 - y
        c = ((dx ** 2) + (dy ** 2)) ** 0.5
        tan = math.degrees(math.atan(dy / dx))
        ##print("Tan q4: " + str(tan))
        if c < 15.9:
            self.controlGeneral(c, tan)
        elif c > 170:
            return "empty", 0
        else:
            entity, segment = self.qFourPoints(tan, c)
            return entity, segment

    def qOnePoints(self, degrees, c):
        # Segmentzuordnung mit Winkel und Entfernung zur Mitte im ersten Quadrant
        if degrees <= 90 and degrees >= 81:  # 20
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                entity = "Single"
                segment = 20
            elif c >= 162 and c <= 170:
                #print("Double 20")
                entity = "Double"
                segment = 20
            elif c >= 101 and c <= 109:
                #print("Triple 20")
                entity = "Triple"
                segment = 20
        elif degrees <= 81 and degrees >= 63:  # 1
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 1")
                entity = "Single"
                segment = 1
            elif c >= 162 and c <= 170:
                    #print("Double 1")
                    entity = "Double"
                    segment = 1
            elif c >= 101 and c <= 109:
                    #print("Triple 1")
                    entity = "Triple"
                    segment = 1
        elif degrees <= 45 and degrees >= 27:  # 4
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                    #print("Single 4")
                    entity = "Single"
                    segment = 4
            elif c >= 162 and c <= 170:
                    #print("Double 4")
                    entity = "Double"
                    segment = 4
            elif c >= 101 and c <= 109:
                    #print("Triple 4")
                    entity = "Triple"
                    segment = 4
        elif degrees <= 9 and degrees >= 0:  # 6
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                    #print("Single 6")
                    entity = "Single"
                    segment = 6
            elif c >= 162 and c <= 170:
                    #print("Double 6")
                    entity = "Double"
                    segment = 6
            elif c >= 101 and c <= 109:
                    #print("Triple 6")
                    entity = "Triple"
                    segment = 6
        elif degrees <= 27 and degrees >= 9:  # 13
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                    #print("Single 13")
                    entity = "Single"
                    segment = 13
            elif c >= 162 and c <= 170:
                    #print("Double 13")
                    entity = "Double"
                    segment = 13
            elif c >= 101 and c <= 109:
                    #print("Triple 13")
                    entity = "Triple"
                    segment = 13
        elif degrees <= 63 and degrees >= 45:  # 18
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                    #print("Single 18")
                    entity = "Single"
                    segment = 18
            elif c >= 162 and c <= 170:
                    #print("Double 18")
                    entity = "Double"
                    segment = 18
            elif c >= 101 and c <= 109:
                    #print("Triple 18")
                    entity = "Triple"
                    segment = 18

        return entity, segment

    def qTwoPoints(self, degrees, c):
        # Segmentzuordnung mit Winkel und Entfernung zur Mitte im zweiten Quadrant
        entity = "empty"
        segment = 0
            
        if degrees <= 81 and degrees >= 63:  # 5
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 5")
                entity = "Single"
                segment = 5
            elif c >= 162 and c <= 170:
                #print("Double 5")
                entity = "Double"
                segment = 5
            elif c >= 101 and c <= 109:
                #print("Triple 5")
                entity = "Triple"
                segment = 5
        elif degrees <= 45 and degrees >= 27:  # 9
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 9")
                entity = "Single"
                segment = 9
            elif c >= 162 and c <= 170:
                #print("Double 9")
                entity = "Double"
                segment = 9
            elif c >= 101 and c <= 109:
                #print("Triple 9")
                entity = "Triple"
                segment = 9
        elif degrees <= 9 and degrees >= 0:  # 11
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 11")
                entity = "Single"
                segment = 11
            elif c >= 162 and c <= 170:
                #print("Double 11")
                entity = "Double"
                segment = 11
            elif c >= 101 and c <= 109:
                #print("Triple 11")
                entity = "Triple"
                segment = 11
        elif degrees <= 63 and degrees >= 45:  # 12
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 12")
                entity = "Single"
                segment = 12
            elif c >= 162 and c <= 170:
                #print("Double 12")
                entity = "Double"
                segment = 12
            elif c >= 101 and c <= 109:
                #print("Triple 12")
                entity = "Triple"
                segment = 12
        elif degrees <= 27 and degrees >= 9:  # 14
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 14")
                entity = "Single"
                segment = 14
            elif c >= 162 and c <= 170:
                #print("Double 14")
                entity = "Double"
                segment = 14
            elif c >= 101 and c <= 109:
                #print("Triple 14")
                entity = "Triple"
                segment = 14
        elif degrees <= 90 and degrees >= 81:  # 20
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 20")
                entity = "Single"
                segment = 20
            elif c >= 162 and c <= 170:
                #print("Double 20")
                entity = "Double"
                segment = 20
            elif c >= 101 and c <= 109:
                #print("Triple 20")
                entity = "Triple"
                segment = 20

        return entity, segment

    def qThreePoints(self, degrees, c):
        # Segmentzuordnung mit Winkel und Entfernung zur Mitte im dritten Quadrant
        segment = 0
        entity = "Segment"

        if degrees <= 9 and degrees >= 0:  # 3
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 3")
                entity = "Single"
                segment = 3
                return entity, segment
            elif c >= 162 and c <= 170:
                #print("Double 3")
                entity = "Double"
                segment = 3
                return entity, segment
            elif c >= 101 and c <= 109:
                #print("Triple 3")
                entity = "Triple"
                segment = 3
                return entity, segment
        elif degrees <= 45 and degrees >= 27:  # 7
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 7")
                entity = "Single"
                segment = 7
                return entity, segment
            elif c >= 162 and c <= 170:
                #print("Double 7")
                entity = "Double"
                segment = 7
            elif c >= 101 and c <= 109:
                #print("Triple 7")
                entity = "Triple"
                segment = 7
        elif degrees <= 81 and degrees >= 63:  # 8
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 8")
                entity = "Single"
                segment = 8
                return entity, segment
            elif c >= 162 and c <= 170:
                #print("Double 8")
                entity = "Double"
                segment = 8
            elif c >= 101 and c <= 109:
                #print("Triple 8")
                entity = "Triple"
                segment = 8
        elif degrees <= 90 and degrees >= 81:  # 11
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 11")
                entity = "Single"
                segment = 11
            elif c >= 162 and c <= 170:
                #print("Double 11")
                entity = "Double"
                segment = 11
            elif c >= 101 and c <= 109:
                #print("Triple 11")
                entity = "Triple"
                segment = 11
        elif degrees <= 63 and degrees >= 45:  # 16
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 16")
                entity = "Single"
                segment = 16
            elif c >= 162 and c <= 170:
                #print("Double 16")
                entity = "Double"
                segment = 16
            elif c >= 101 and c <= 109:
                #print("Triple 16")
                entity = "Triple"
                segment = 16
        elif degrees <= 27 and degrees >= 9:  # 19
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 19")
                entity = "Single"
                segment = 19
            elif c >= 162 and c <= 170:
                #print("Double 19")
                entity = "Double"
                segment = 19
                return entity, segment
            elif c >= 101 and c <= 109:
                #print("Triple 19")
                entity = "Triple"
                segment = 19

        return entity, segment

    def qFourPoints(self, degrees, c):
        # Segmentzuordnung mit Winkel und Entfernung zur Mitte im vierten Quadrant
        entity = "empty"
        segment = 0
        if degrees <= 45 and degrees >= 27:  # 2
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 2")
                entity = "Single"
                segment = 2
            elif c >= 162 and c <= 170:
                #print("Double 2")
                entity = "Double"
                segment = 2
            elif c >= 101 and c <= 109:
                #print("Triple 2")
                entity = "Triple"
                segment = 2
        elif degrees <= 9 and degrees >= 0:  # 3
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 3")
                entity = "Single"
                segment = 3
            elif c >= 162 and c <= 170:
                #print("Double 3")
                entity = "Double"
                segment = 3
            elif c >= 101 and c <= 109:
                #print("Triple 3")
                entity = "Triple"
                segment = 3
        elif degrees <= 90 and degrees >= 81:  # 6
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 6")
                entity = "Single"
                segment = 6
            elif c >= 162 and c <= 170:
                #print("Double 6")
                entity = "Double"
                segment = 6
            elif c >= 101 and c <= 109:
                #print("Triple 6")
                entity = "Triple"
                segment = 6
        elif degrees <= 81 and degrees >= 63:  # 10
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 10")
                entity = "Single"
                segment = 10
            elif c >= 162 and c <= 170:
                #print("Double 10")
                entity = "Double"
                segment = 10
            elif c >= 101 and c <= 109:
                #print("Triple 10")
                entity = "Triple"
                segment = 10
        elif degrees <= 63 and degrees >= 45:  # 15
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 15")
                entity = "Single"
                segment = 15
            elif c >= 162 and c <= 170:
                #print("Double 15")
                entity = "Double"
                segment = 15
            elif c >= 101 and c <= 109:
                #print("Triple 15")
                entity = "Triple"
                segment = 15
        elif degrees <= 27 and degrees >= 9:  # 17
            if (c >= 15.9 and c <= 101) or (c >= 109 and c <= 162):
                #print("Single 17")
                entity = "Single"
                segment = 17
            elif c >= 162 and c <= 170:
                #print("Double 17")
                entity = "Double"
                segment = 17
            elif c >= 101 and c <= 109:
                #print("Triple 17")
                entity = "Triple"
                segment = 17

        return entity, segment

    def controlGeneral(self, c):
                                    # Der Fall, dass der Dart entweder ausserhalb der Dartscheibe oder innerhalb vom Bull landet
        entity = "empty"
        point = 0
        if c < 15.9 and c > 6.35:
            entity = "Bull"
            point = 25
        elif c < 6.35 and c >= 0:
            entity = "Bullseye"
            point = 50
        elif c > 170:
            entity = "empty"
            point = 0

        return entity, point

g = Game()
