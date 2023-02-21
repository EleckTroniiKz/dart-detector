#Autor: Can Cetin, 12/3

class Game:

    players = []
    playerPoints = []
    actPlayer = 1
    game = True
    dartCount = 0

    startingEntity = []

    masterIn = False
    doubleIn = False

    straightOut = False
    doubleOut = False
    tripleOut = False

    gameContinue = False

    pointsBackUp = 0

    s = [0] * 20
    d = [0] * 20
    t = [0] * 20

    scoreboard = [["Spieler  ", "Wurf 1", "Wurf 2", "Wurf 3", "Punkte"]]
    playersThrows = [0, 0, 0]
    playersEntity = ["empty", "empty", "empty"]
    playersWon = []

    nameSet = False

    def __init__(self):
        # Python Konstruktor
        self.welcome()
        self.askrulesettings()
        self.createplayers()
        self.choosemode()
        self.fillPointsLists()
        self.process()
    # END of __init__

    def process(self):
        # Spielverlauf vom Dart Spiel
        while self.game:

            if self.gameContinue:
                if self.game == False:
                    break

            for a in range(3):
                print("Punkte von Spieler " + str(self.actPlayer) + ": " + str(self.playerPoints[self.actPlayer - 1]))
                e = input("ENTITY (Single, Double, Triple)?  ")
                p = input("PUNKTE?  ")
                p = int(p)
                self.playersThrows[a] = p
                self.playersEntity[a] = e
                self.throwdart(p, e)
                self.checkrules(self.playersThrows[0], self.playersEntity[0], self.playersThrows[1],
                                self.playersEntity[1], self.playersThrows[2], self.playersEntity[2])

        self.showscoreboard()
    # End of process

    def fillPointsLists(self):
        # Füllt die 3 leeren Listen s, d und t mit den Single, Double und Triple Werten der Segmente
        for a in range(20):
            self.s[a] = 1 * a + 1
            self.d[a] = 2 * a + 2
            self.t[a] = 3 * a + 3
    # End of fillPointsLists

    def createplayers(self):
        # Fragt die Anzahl der Spieler ab und kreiert die benötigten Listen für die Punkte, die Spieler-ID's/Spielernamen
        playernumber = int(input("Wie viele Leute spielen mit?"))

        self.players = [0] * playernumber
        self.playerPoints = [0] * playernumber
        self.startingEntity = [0] * playernumber

        askforname = input("Want to set your Name for the Players?")
        # Bei Bedarf kann man hier die Spieler benennen
        if self.checkuserdecision(askforname):
            self.nameSet = True
            for a in range(len(self.players)):
                name = input("Name von Spieler " + str(a + 1) + "?")
                self.players[a] = name
        elif not self.checkuserdecision(askforname):
            for i in range(len(self.players)):
                self.players[i] = "Spieler " + str(1 + i)
                print(str(self.players[i]))
    # End of createplayers

    def choosemode(self):
        # Spielmodus-Wahl: 301, 501, 601
        choosenMode = int(input("Welchen Spielemodus möchten Sie spielen?\n (301/501/601) ?"))
        if choosenMode == 301 or choosenMode == 501 or choosenMode == 601:
            for i in range(len(self.players)):
                self.playerPoints[i] = choosenMode
        else:
            print("Bitte wählen Sie nur einen von diesen Modi aus: 301, 501 oder 601!")
            self.choosemode()
    # End of choosenMode

    def throwdart(self, n, e):
        # Rechnung für den Dartwurf
        t = self.checkdart(n, e)

        self.playerPoints[self.actPlayer - 1] = self.playerPoints[self.actPlayer - 1] - float(t)
        print("Punkte von " + self.players[self.actPlayer - 1] + " nach Wurf Nummer " + str(self.dartCount + 1) + "!")

        print(str(self.playerPoints[self.actPlayer - 1]))
    # END of throwdart

    def checkdart(self, t, e):
        # Wert der angegebenen Entität und des Segmentes wird hier kontrolliert
        if t == 25 and e == "Bull":
            return 25
        elif t == 50 and e == "Bullseye":
            return 50
        elif t == 0 and e == "empty":
            return 0
        elif isinstance(t, int) == False:
            return 0
        else:
            if t >= 21 or t < 0:
                return 0
            elif t >= 1 and t <= 20:
                if e == "Single":
                    if self.startingEntity[self.actPlayer - 1] == 0 and self.doubleIn:
                        return 0

                    elif self.startingEntity[self.actPlayer - 1] == 0 and self.masterIn:
                        return 0

                    elif self.startingEntity[self.actPlayer - 1] == 1:
                        return self.s[t - 1]

                    elif not self.masterIn and not self.doubleIn:
                        return self.s[t - 1]

                elif e == "Double":
                    if self.startingEntity[self.actPlayer - 1] == 0 and self.doubleIn:
                        self.startingEntity[self.actPlayer - 1] = 1
                        return self.d[t - 1]

                    elif self.startingEntity[self.actPlayer - 1] == 0 and self.masterIn:
                        return 0

                    elif self.startingEntity[self.actPlayer - 1] == 1:
                        return self.d[t - 1]

                    elif not self.masterIn and not self.doubleIn:
                        return self.d[t - 1]

                elif e == "Triple":
                    if self.startingEntity[self.actPlayer - 1] == 0 and self.doubleIn:
                        return 0

                    elif self.startingEntity[self.actPlayer - 1] == 0 and self.masterIn:
                        self.startingEntity[self.actPlayer - 1] = 1
                        return self.t[t - 1]

                    elif self.startingEntity[self.actPlayer - 1] == 1:
                        return self.t[t - 1]

                    elif not self.masterIn and not self.doubleIn:
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
        elif phrase == "No" or phrase == "no" or phrase == "Nein" or phrase == "nein" or phrase == "N" or phrase == "n"\
                or phrase == "Nope" or phrase == "nope" or phrase == "Nee" or phrase == "nee":
            return False
        else:
            return False
    # END of checkuserdecision

    def checkrules(self, n1, e1, n2, e2, n3, e3):
        # Kontrolliert, ob alle Regeln eingehalten werden, die am Anfang vom Spiel eingestellt wurden
        lastThrow = ""
        if self.straightOut:
            lastThrow = e1
            points1 = self.checkdart(n1, e1)

            if n2 != 0 and e2 != "empty":
                points2 = self.checkdart(n2, e2)
                lastThrow = e2
            else:
                points2 = 0

            if n3 != 0 and e3 != "empty":
                points3 = self.checkdart(n3, e3)

                lastThrow = e3
            else:
                points3 = 0

            self.pointsBackUp = points1 + points2 + points3
            print("Points BackUp:   " + str(self.pointsBackUp))

            if self.playerPoints[self.actPlayer - 1] < 0:
                if self.doubleOut or self.tripleOut:
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
                    if lastThrow == "Double" or lastThrow == "double" or lastThrow.startswith("d"):
                        print("Herzlichen Glückwunsch Spieler " + str(self.actPlayer) + ". Sie haben gewonnen!")
                        self.checkcontinuegame()
                    elif lastThrow == "Bullseye":
                        print("Herzlichen Glückwunsch Spieler " + str(self.actPlayer) + ". Sie haben gewonnen!")
                        self.checkcontinuegame()
                    else:
                        print("Sie müssen genau auf 0 kommen und dies mit einem Double Wurf")
                        self.playerPoints[self.actPlayer - 1] = self.playerPoints[
                                                                    self.actPlayer - 1] + self.pointsBackUp
                        print("Neue Punktzahl =" + str(self.playerPoints[self.actPlayer - 1]))
                        self.changedartcount(True)
                elif self.tripleOut:
                    if lastThrow == "Triple" or lastThrow == "triple" or lastThrow.startswith("t"):
                        print("Herzlichen Glückwunsch Spieler " + str(self.actPlayer) + ". Sie haben gewonnen!")
                        self.checkcontinuegame()
                    else:
                        print("Sie müssen genau auf 0 kommen und dies mit einem Triple Wurf")
                        self.playerPoints[self.actPlayer - 1] = self.playerPoints[
                                                                    self.actPlayer - 1] + self.pointsBackUp
                        print("Neue Punktzahl =" + str(self.playerPoints[self.actPlayer - 1]))
                        self.changedartcount(True)
                elif not self.doubleOut and not self.tripleOut:
                    print("Herzlichen Glückwunsch Spieler " + str(self.actPlayer) + ". Sie haben gewonnen!")
                    self.checkcontinuegame()
            else:
                self.changedartcount(False)

        elif not self.straightOut:
            if self.playerPoints[self.actPlayer - 1] <= 0:
                print("Herzlichen Glückwunsch Spieler " + str(self.actPlayer) + ". Sie haben gewonnen!")
                self.fillscoreboard()
                self.checkcontinuegame()
                self.showscoreboard()

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
                self.showscoreboard()
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
        lastThrow = ""
    # End of changeplayer

    def checkcontinuegame(self):
        # Userabfrage, ob Sie weiterspielen möchten. Wird aufgrerufen nachdem ein Spieler 0 erreicht hat.

        self.playersWon.append(self.actPlayer)
        self.checkoneplayerleft()

        askplayers = input("Do the other Players want to continue?")
        self.gameContinue = self.checkuserdecision(askplayers)
        if self.gameContinue:
            self.game = True
            self.changedartcount(True)
            self.process()
        elif not self.gameContinue:
            self.game = False
            print("Game Ended")
            exit()
    # END of checkcontinuegame

    def askrulesettings(self):
        # Fragt die User nach den Regeln, mit denen Sie spielen wollen

        masterInAsk = input("Master-In: Ja/Nein?")
        self.masterIn = self.checkuserdecision(masterInAsk)
        if not self.masterIn:
            doubleInAsk = input("Double-In: Ja/Nein")
            self.doubleIn = self.checkuserdecision(doubleInAsk)

        tripleOutAsk = input("Triple Out: Ja/Nein?")
        self.tripleOut = self.checkuserdecision(tripleOutAsk)
        if self.tripleOut:
            self.straightOut = True
        elif not self.tripleOut:
            doubleOutAsk = input("Double Out : Ja/Nein?")
            self.doubleOut = self.checkuserdecision(doubleOutAsk)
            if self.doubleOut:
                self.straightOut = True
            elif not self.doubleOut:
                straightOutAsk = input("Straight Out : Ja/Nein?")
                self.straightOut = self.checkuserdecision(straightOutAsk)
    # END of askrulesettings

    def checkstopgame(self, phrase):
        # Kontrolliert ob als Entity End oder ähnliches eingegeben wurde. Wenn ja, wird das Spiel direkt beendet
        if phrase == "Ende":
            self.game = False
            print("Game Ended")
            return True
        elif phrase == "Restart":
            self.restartgame()
        else:
            return False
    # END of checkstopgame

    def showscoreboard(self):
        # Gibt das Scoreboard aus
        if self.game:
            for a in range(len(self.scoreboard)):
                print(self.scoreboard[a])

        elif not self.game and len(self.playersWon) > 1:
            print("")
            lastPlayer = 0

            for i in range(len(self.playersWon)):
                print("Platz " + str(i + 1) + ": " + str(self.players[i]))

            for i in range(len(self.players)):
                if self.players[i] not in self.playersWon:
                    lastPlayer = self.players[i]

            if len(self.players) - 1 != len(self.playersWon):
                return
            else:
                print("Letzter Platz: " + str(lastPlayer))
    # End of showscoreboard

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
            self.scoreboard[0] = ["Players" + " " * 13, "Throw1", "Throw2", "Throw3", "Score"]
        self.scoreboard.append([str(self.players[self.actPlayer - 1]) + " " * z, a[0], a[1], a[2], d])
    # End of fillscoreboard

    def pausescoreboard(self):
        # Gibt eine Trennlinie aus, um so das lesen des Scoreboards zu erleichtern
        # m = Anzahl der "_"
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
            self.showscoreboard()
            s = input("Do you want to play again?")

            if self.checkuserdecision(s):
                self.restartgame()

            elif not self.checkuserdecision(s):
                print("Game has been ended")
                exit()
    # End of checkoneplayerleft

    def welcome(self):
        # Dies hier sind die Prints für den Start des Programms
        # Hier wird dem User kurz erklärt was gleich passiert etc.
        # Sollte später jedoch in der GUI in anderer Form dargestellt werden.
        print("Willkommen! :D /")
        print("Regeln: ")
        print("Jeder Spieler bekommt 3 Darts. \n   Das Ziel ist es, von einer gleich gewählten "
              "Startpunktzahl (301/501/601) auf 0 zu kommen.")
        print("Gleich darfst du auswählen mit welchen Regelungen du spielst. Dies sind die individuellen Regeln:")
        print("Straight Out:  Du musst genau auf Null kommen. "
              "Ohne diese Regel kannst du werfen wie du willst. "
              "Du musst zum gewinnen einfach 0 oder weniger Punkte erreichen.")
        print("Straight Out:  Du musst GENAU auf NULL kommen.")
        print("Double Out:  Der Wurf mit dem du genau auf Null kommst muss ein Double-Wurf sein.")
        print("Master Out:  Der Wurf mit dem du genau auf Null kommst muss ein Triple-Wurf sein.")
        print("Double In:  Der Wurf mit dem du in das Spiel einsteigst muss ein Double-Wurf sein.")
        print("Triple In:  Der Wurf mit dem du in das Spiel einsteigst muss ein Double-Wurf sein.")
        print("")
        print("")
        print("Wenn du ein Bull oder Bullseye wirfst, dann bitte als Entity Bull und bei Punkte 25/ als Entity Bullseye und bei Punkte 50 eingeben")

        print("")
        print("")

        abfrage = input("Wenn du nun anfangen willst zu spielen, drücke die ENTER-Taste")
        print("________        _     ________   __________")
        print("`MMMMMMMb.     dM.    `MMMMMMMb. MMMMMMMMMM")
        print(" MM    `Mb    ,MMb     MM    `Mb /   MM   \ ")
        print(" MM     MM    d'YM.    MM     MM     MM     ")
        print(" MM     MM   ,P `Mb    MM     MM     MM     ")
        print(" MM     MM   d'  YM.   MM    .M9     MM     ")
        print(" MM     MM  ,P   `Mb   MMMMMMM9'     MM     ")
        print(" MM     MM  d'    YM.  MM  \M\       MM     ")
        print(" MM     MM ,MMMMMMMMb  MM   \M\      MM     ")
        print(" MM    .M9 d'      YM. MM    \M\     MM     ")
        print("_MMMMMMM9_dM_     _dMM_MM_    \M\_  _MM_  ")

        print("")
        print("")
    # End of welcome

    def restartgame(self):
        # Falls das Spiel Neu gestartet wird, werden hier alle Werte auf die Standard-Anfangswerte zurückgesetzt
        self.dartCount = 0
        self.actPlayer = 1
        self.game = True

        self.straightOut = False
        self.doubleOut = False

        self.masterIn = False
        self.doubleIn = False
        self.gameContinue = False

        self.startingEntity = []

        self.pointsBackUp = 0
        lastThrow = ""
        self.scoreboard = [["Players", "Throw1", "Throw2", "Throw3", "Score"]]
        self.playersWon = []
        self.playersThrows = [0, 0, 0]
        self.playersEntity = ["empty", "empty", "empty"]
        self.nameSet = False

        print("GAME HAS BEEN RESETTED!")
        self.__init__()
    # End of restartgame


g = Game()