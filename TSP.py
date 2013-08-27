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

def fitness(thePop, cityInfo):
     chromoSize = len(thePop[0][1])
     cities = cityInfo[0]
     distances = cityInfo[1]
     cityOrder = []

     for citizen in thePop:
          cityOrder = [0] * chromoSize
          chromo = citizen[1]
          thisDist = [-1.0] * (chromoSize - 1)
          
          for i in range(chromoSize):
               cityOrder[i] = chromo.index(i)
          
          for i in range(len(cityOrder)):
               if not i == len(cityOrder) - 1:
                    thisCity = cityOrder[i]
                    nextCity = cityOrder[i+1]

                    thisDist[i] = distances[thisCity][nextCity]


          citizen[2] = sum(thisDist)
     
     return thePop

def createDataStructs(theCities):
     cityOrder = {}
     sdistances = []
     distances = []
     count = 0

     for city in theCities:
          cityOrder[city[0]] = count
          distances.append(city[1:])
          
          for i in range(len(distances)):
               newCity = []
               for j in range(len(distances[i])):
                    newCity.append(float(distances[i][j]))
               distances[i] = newCity  
                               
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
     
     
      
     pop = fitness(pop, structs)

     for ele in pop:
         print ele








