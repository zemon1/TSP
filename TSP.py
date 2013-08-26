#Jeff Haak
#Traveling Salesman Problem
import copy, random

def initializePop(popSize, chromoSize):
     pop = []
     count = 0
     while count < popSize:
          pop.append([count, [0] * chromoSize, 9999999])
          count += 1

     return pop

def randomizePop(thePop):
     choiceMax = len(thePop[0][1])
     choices = []
     for i in range(0, choiceMax):
         choices.append(i)

     for citizen in thePop:
          availible = copy.deepcopy(choices)
          random.shuffle(availible)
          citizen[1] = availible         
           
     return thePop 




def createDataStructs(theCities):
     cityOrder = {}
     distances = []
     count = 0

     for city in theCities:
          cityOrder[city[0]] = count
          distances.append(city[1:])           
          count += 1

     return (cityOrder, distances)

def readCities(fileName):
     lines = []
     theFile = open(fileName)
     
     for line in theFile:
         line = line.strip().split(",")
         lines.append(line)
     
     return lines

if __name__ == "__main__":
     random.seed(1)
     cities = readCities("./cities.csv")
     structs = createDataStructs(cities)
     
     pop = initializePop(10, 7)
     pop = randomizePop(pop)
     
     for ele in pop:
         print ele








