#Jeff Haak
#Traveling Salesman Problem










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
     cities = readCities("./cities.csv")
     structs = createDataStructs(cities)

     for ele in structs[1]:
         print ele








