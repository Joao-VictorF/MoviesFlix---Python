from socket import AF_INET, socket, SOCK_DGRAM, gethostname
import json, uuid

host = gethostname()
port = 8080
buffer = 65535
address = (host, port)

def getAllMovies():
  Database = open('DB.json', 'r')
  movies = json.load(Database)
  Database.close()
  return json.dumps(movies).encode()

def getMovie(id):
  Database = open('DB.json', 'r')
  movies = json.load(Database)
  Database.close()

  for movie in movies:
    if movie['id'] == id:
      response = movie
      return json.dumps(response).encode()

def createMovie(movie):
  Database = open('DB.json', 'r')
  movies = json.load(Database)

  movie['id'] = str(uuid.uuid4())
  movies.append(movie)

  Database = open('DB.json', 'w')
  json.dump(movies, Database)
  Database.close()

def deleteMovie(id):
  Database = open('DB.json', 'r')
  movies = json.load(Database)
  Database.close()
  for movie in movies:
    if movie['id'] == id:
      movies.remove(movie)
      moviesAfterDelete = movies
      Database = open('DB.json', 'w')
      json.dump(moviesAfterDelete, Database)
      Database.close()


server = socket(AF_INET, SOCK_DGRAM)
server.bind(address)
print ('\n\nServer running at {}' .format(gethostname()))

while True:
  reqData, address = server.recvfrom(buffer)
  reqData = reqData.decode()
  reqData = json.loads(reqData)
  
  if reqData["method"] == "GET":
    if reqData["id"]:
      server.sendto(getMovie(reqData["id"]), address) 
    else:
      server.sendto(getAllMovies(), address)

  elif reqData["method"] == "POST":
    createMovie(reqData["movie"])
    message = 'ok'
    server.sendto(message.encode(), address)

  elif reqData["method"] == "DELETE":
    print(reqData["id"])
    deleteMovie(reqData["id"])
    message = 'ok'
    server.sendto(message.encode(), address)
