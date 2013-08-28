#Jeff Haak
#Traveling Salesman Problem
import copy, random, numpypy, numpy
from operator import itemgetter

popId = 0 

#This function creates the initial population set
def initializePop(popSize, chromoSize):
     pop = []
     global popId

     count = 0
     
     #creates blank people for the program
     while count < popSize:
          pop.append([popId, [0] * chromoSize, 9999999])
          popId += 1
          count += 1

     return pop

#randomizes every person's chromosome in the population
def randomizePop(thePop):
     
     #max number of options 
     choiceMax = len(thePop[0][1])
     choices = []

     #Populates the list of options from 0 to the max choice     
     for i in range(0, choiceMax):
         choices.append(i)
     
     #This loop copies the options and shuffles them up and uses that as the 
     #    chromosome
     for citizen in thePop:
          availible = copy.deepcopy(choices)
          random.shuffle(availible)
          citizen[1] = availible         
           
     return thePop 

#This function ranks the citezens from best to worst by how long their path is
def fitness(thePop, cityInfo):
     chromoSize = len(thePop[0][1])
     cities = cityInfo[0]
     distances = cityInfo[1]
     cityOrder = []
     
     #figures out the order of the destinations and the total distance traveled
     for citizen in thePop:
          #create an empty array for the order of the cities to visit
          cityOrder = [0] * chromoSize
          
          #create a shortcut to the useful info
          chromo = citizen[1]

          #array containing all of the distances to the cities in the order 
          #    specified by the chromosome
          thisDist = [-1.0] * (chromoSize - 1)
          
          #determine what the order of cities is by finding out where they 
          #    are in the array
          for i in range(chromoSize):
               cityOrder[i] = chromo.index(i)
          
          #go through the list created above and find look up the distance 
          #    between each specified city
          for i in range(len(cityOrder)):
               if not i == len(cityOrder) - 1:
                    thisCity = cityOrder[i]
                    nextCity = cityOrder[i+1]

                    thisDist[i] = distances[thisCity][nextCity]
          #Sum the distance array to get the total distance traveled
          citizen[2] = sum(thisDist)
     
     #Sort the population by the total distance traveled
     thePop = sorted(thePop, key=itemgetter(2))
     
     return thePop

#this funtion identitifies potential mates and then mates them
def mate(thePop):
     global popId
     
     #create a result array and fill it with -1
     result = [-1] * int(round(len(thePop) * .25))
     
     #create an array of the top quarter of the population 
     elites = [-1] * int(round(len(thePop) * .25)) 

     #create an array for the top 55% and this becomes our mating pool
     candidates = [-1] * int(round(len(thePop) * .555555))
     
     #Put the elites in their array and into the result array
     count = 0
     while count < len(elites):
         elites[count] = thePop[count]
         result[count] = elites[count]
         count += 1 
     
     #Fill up the candidates array    
     count = 0
     while count < len(candidates):
         candidates[count] = thePop[count]
         count += 1
     
     #Mate the best citizen with all other citizens.  If the result does 
     #    not have enough people in it mate the second best with everyone 
     #    except the best ect.
     empty = int(round(len(thePop) * .25)) 
     for i in range(len(candidates)):
          for j in range(len(candidates)):
               if i < j:
                    if empty < len(thePop):
                        result.extend(crossOver(candidates[i], candidates[j]))
                    empty += 2
                              
     #If the result has too many citizens, kill one off and reduce the popId
     while len(result) > len(thePop):
          result.pop()
          popId -= 1 

     return result

def crossOver(par1, par2):
     global popId
     child1 = [popId, [], 9999999]
     child2 = [popId + 1, [], 9999999]
     
     popId += 2

     crossover = (len(par1[1]) % (random.randrange(25, 75, 1)/10) + 1) 
     
     count = 0
     while count < crossover:
          child1[1].append(par1[1][count])     
          child2[1].append(par2[1][count])     
          count += 1

     count = 0
     while count < len(par1[1]):
          if len(child1[1]) < len(par1[1]):
               try:
                    child1[1].index(par2[1][count])
               except:
                    child1[1].append(par2[1][count])

          if len(child2[1]) < len(par2[1]):
               try:
                    child2[1].index(par1[1][count])
               except:
                    child2[1].append(par1[1][count])

          count += 1
     
     mutate(child1[1])
     mutate(child2[1])
     
     return [child1, child2]

def mutate(chromo):
     thresh = 17
     
     for i in range(0, len(chromo)):
         chance = random.randrange(1, 100) 
         
         if chance <= thresh:
             old = chromo[i]
             ind = (i + 1) * -1
             new = chromo[ind]
             
             chromo[i] = new
             chromo[ind] = old

def createDataStructs(theCities):
     cityOrder = {}
     sdistances = []
     distances = []
     count = 0

     for city in theCities:
          cityOrder[count] = city[0]
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

def runGA(num = -1, close = 1):
     cities = readCities("./cities.csv")
     structs = createDataStructs(cities)
     
     for city in structs[1]:
         print city
      
     pop = initializePop(100, len(structs[1]))
     pop = randomizePop(pop)
     pop = fitness(pop, structs)
     
     topDiff = 9999999
     
     print "Gen: ", 0
     for i in range(len(pop)//10):
         print pop[i]


     if num == -1:
         count = 0
         while topDiff > close:
             newPop = mate(pop)
             pop = fitness(newPop, structs)
            
             cutoff = ((len(pop)//8) * 3) * -1
             topDiff = pop[cutoff][2] - pop[0][2]
             count += 1

             print "Gen: ", count
             for i in range(len(pop)//10):
                 print pop[i]

     else:
         count = 0
         while count < num:
             newPop = mate(pop)
             pop = fitness(newPop, structs)
             
             count += 1

             print "Gen: ", count
             for i in range(len(pop)//10):
                 print pop[i]
     
     printSolution(pop[0], structs[0])

                
def printSolution(best, cities):
     order = best[1]
     dist = best[2]
     
     final = ""

     for i in range(len(order)):
         city = order.index(i)

         final += cities[city] 
         
         if  i != len(order) - 1:
             final += " -> "
     
     print "\n"
     print final
     print "\n" 

if __name__ == "__main__":
     random.seed(1)
     
     runGA(-1)
