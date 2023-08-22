


class Dijkstra:

    def __init__(self, map={"A": {"B": 30, "C": 10},
                    "B": {"A": 30, "C": 5, "D": 40, "E": 20},
                    "C": {"A": 10, "B": 5, "D": 20},
                    "D": {"B": 40, "C": 20, "E": 10},
                    "E": {"B": 20, "D": 10}}, startPoint="A", endPoint="E"):
        self.map = map
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.dist = 0
        self.table = []
        self.blackList = []
        self.road = []

    def Dijkstra(self):
        startPoint = self.startPoint
        isSmalest = False

        #isSmalest est la variable qui dit si le point d'arriver est le plus petit
        while not isSmalest:
            currentIndex = 0
            minIndex = None
            isBL = False
            min = None
            dist = 0

            #on cherche actuellement la route la plus petite
            for i in self.table:
                if min is None or min > i[1]:
                    for bl in self.blackList:
                        if bl == i[2]:
                            isBL = True
                            break
                    if not isBL:
                        min = i[1]
                        minIndex = currentIndex

                isBL = False
                currentIndex += 1

            if len(self.table) > 0 and minIndex is not None:
                startPoint = self.table[minIndex][2]
                dist = self.table[minIndex][1]

                if startPoint == self.endPoint:
                    isSmalest = True

            #on ajoute tout les nouveaux point accessible à partir du startpoint
            if not isSmalest:
                for i in self.map.get(startPoint).keys():
                    for bl in self.blackList:
                        
                        if bl == i:
                            isBL = True
                            break

                    if not isBL and self.map.get(startPoint).get(i) is not None:
                        self.table.append((startPoint, dist + self.map.get(startPoint).get(i), i))
                    self.blackList.append(startPoint)

                    isBL = False

        self.road = [startPoint]

        while startPoint != self.startPoint:
            currentIndex = 0
            minIndex = None
            min = None

            for i in self.table:
                if i[2] == startPoint and (min is None or i[1] < min):
                    min = self.table[currentIndex][1]
                    minIndex = currentIndex

                currentIndex += 1

            startPoint = self.table[minIndex][0]
            self.dist += self.map.get(self.table[minIndex][0]).get(self.table[minIndex][2])
            self.road.insert(0, startPoint)

        print(self.road)
        print(self.dist)
