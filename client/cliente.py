from tkinter import *
from socket import AF_INET, socket, SOCK_DGRAM, gethostname
import socket, json, pickle, sys, emoji

class Interface(Frame):
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.master['bg'] = 'gray25'
    self.master.attributes('-fullscreen', True)
    self.addMovieScreenExists = FALSE
    self.movieScreenExists = FALSE

    self.host = gethostname()
    self.port = 8080
    self.buffer = 65535
    self.address = (self.host, self.port)
    self.clienteSckt = socket.socket(AF_INET, SOCK_DGRAM)
    

    def AddMovieScreen(self):
      self.HomeFrame.pack_forget()
      movie = {}
      movie['name'] = ''
      movie['rating'] = ''
      movie['actors'] = ['']
      movie['directors'] = ['']
      actorsEntries = {}
      actorsSpaces = {}
      directorsEntries = {}
      directorsSpaces = {}

      self.AddMovieFrame = Frame(None, pady = 20)
      self.AddMovieFrame["bg"] = "gray25"
      self.AddMovieFrame.pack()
      self.addMovieScreenExists = TRUE

      title = Label(self.AddMovieFrame, width=100,text="Adicionar filme", bg='gray25', fg='white smoke', font=("Calibri", "30"), pady=30) 
      title.pack()

      self.movieName = Entry(self.AddMovieFrame, font = ("Calibri", "15"), width = 50, textvariable = movie['name'])
      self.movieName.insert(0, ' Nome do filme')
      self.movieName.bind("<FocusIn>",lambda args: self.movieName.delete('0', 'end'))
      self.movieName.pack()

      spacing0 = Label(self.AddMovieFrame, text = " ", bg = "gray25")
      spacing0.pack()

      self.movieRating = Entry(self.AddMovieFrame, font = ("Calibri", "15"), width = 50, textvariable = movie['rating'])
      self.movieRating.insert(0, ' Qual a nota do filme? 0 - 5')
      self.movieRating.bind("<FocusIn>",lambda args: self.movieRating.delete('0', 'end'))
      self.movieRating.pack()

      spacing1 = Label(self.AddMovieFrame, text = " ", bg = "gray25")
      spacing1.pack()

      actorsFrame = Frame(self.AddMovieFrame, bg = 'gray25')
      actorsFrame.pack()

      self.actorName = Entry(actorsFrame, font = ("Calibri", "15"), width = 50, textvariable = movie['actors'][0])
      self.actorName.insert(0, " Nome do 1° ator/atriz")
      self.actorName.bind("<FocusIn>",lambda args: self.actorName.delete('0', 'end'))
      self.actorName.pack()

      spacing2 = Label(actorsFrame, text = " ", bg = "gray25")
      spacing2.pack()

      newActorBtn = Button(actorsFrame, text = " Adicionar ator/atriz", bg = 'brown1', fg = 'white smoke', relief='flat', width = 50, font = ("Calibri", "15"), command = lambda : newActor(actorsFrame, len(movie['actors']), actorsEntries, movie['actors'], actorsSpaces))

      newActorBtn.pack(side = BOTTOM)

      spacing3 = Label(self.AddMovieFrame, text = " ", bg = "gray25")
      spacing3.pack()

      directorsFrame = Frame(self.AddMovieFrame, bg = 'gray25')
      directorsFrame.pack()
      
      self.directorName = Entry(directorsFrame, font = ("Calibri", "15"), width = 50, textvariable = movie['directors'][0])
      self.directorName.insert(0, " Nome do 1° diretor")
      self.directorName.bind("<FocusIn>",lambda args: self.directorName.delete('0', 'end'))
      self.directorName.pack()

      spacing4 = Label(directorsFrame, text = " ", bg = "gray25")
      spacing4.pack()

      newDirectorBtn = Button(directorsFrame, text = "Adicionar diretor(a)", bg = 'brown1', fg = 'white smoke', relief='flat', width = 50, font = ("Calibri", "15"), command = lambda : newDirector(directorsFrame, len(movie['directors']), directorsEntries, movie['directors'], directorsSpaces))
      newDirectorBtn.pack(side = BOTTOM)

      spacing5 = Label(self.AddMovieFrame, text = " ", pady = 30, bg = "gray25")
      spacing5.pack()

      buttonsFrame = Frame(self.AddMovieFrame, width=50, bg = "gray25")
      buttonsFrame.pack()

      homeBtn = Button(buttonsFrame, text = "Voltar", width = 20, font = ("Calibri", "15"), command = lambda : HomeScreen(self))
      homeBtn.pack(side = LEFT)

      spacing6 = Label(buttonsFrame, text = " ", bg = "gray25", width = 11)
      spacing6.pack(side = LEFT)

      saveBtn = Button(buttonsFrame, text = "Salvar", bg = 'brown1', fg = 'white smoke', relief='flat', width = 20, font = ("Calibri", "15"), command = lambda : postMovie(movie, self, actorsEntries, directorsEntries))
      saveBtn.pack(side = RIGHT)

    def HomeScreen(self):
      self.movies = getMovies()
      if self.addMovieScreenExists:
        self.AddMovieFrame.pack_forget()

      if self.movieScreenExists:
        self.MovieFrame.pack_forget()

      self.HomeFrame = Frame(master, bg = "gray25")
      self.HomeFrame.pack()

      topContainer = Frame(self.HomeFrame, bg = "gray25", pady = 10, padx = 40)
      topContainer.pack()

      title = Label(topContainer, width=100,text="Lista de Filmes", bg='gray25', fg='white smoke', font=("Calibri", "30"), pady=15, anchor='nw') 
      title.pack()

      searchBar = Entry(topContainer, font = ("Calibri", "17"), width = 80)
      searchBar.insert(0, 'Pesquisar filme pelo titulo')
      searchBar.bind("<FocusIn>",lambda args: searchBar.delete('0', 'end'))
      searchBar.bind("<Return>",lambda x: filterMovies(self, searchBar.get()))
      searchBar.pack(side=LEFT)

      space = Label(topContainer, text = " ", bg = "gray25", width = 1)
      space.pack(side=LEFT)

      newFilmBtn = Button(topContainer, text = "Cadastrar filme", width = 20, bg = 'brown1', padx = 5, fg = 'snow', relief='flat', font = ("Calibri", "14"), command = lambda : AddMovieScreen(self))
      newFilmBtn.pack(side=RIGHT)

      tableData = Frame(self.HomeFrame, bg = "gray25")
      tableData.pack()

      self.moviesContainer = Frame(self.HomeFrame, bg = "gray25", pady = 20, padx = 40)
      self.moviesContainer.pack()

      movieName = Label(tableData, text = "Nome", fg = "white smoke", bg = "gray25", font = ("Calibri", "25"))
      movieName.pack(side = LEFT)
      
      space2 = Label(tableData, text = " ", bg = "gray25", width = 62)
      space2.pack(side=LEFT)

      movieRating = Label(tableData, text = "Avaliação", fg = "white smoke", bg = "gray25", font = ("Calibri", "25"))
      movieRating.pack(side = LEFT)
      
      space3 = Label(tableData, text = " ", bg = "gray25", width = 63)
      space3.pack(side=LEFT)

      movieActions = Label(tableData, text = "Opções", fg = "white smoke", bg = "gray25", font = ("Calibri", "25"))
      movieActions.pack(side = LEFT)

      movies = self.movies
      moviesRows = {}
      movieIndex = 1

      for movie in movies:
        name = movie["name"]
        rating = movie["rating"]
        star = emoji.emojize(':star:', use_aliases=True)
        
        movieName = f"{str(movieIndex)}  - {name}"
        movieRating = star*rating

        moviesRows[f"Row{movieIndex}"] = Frame(self.moviesContainer, width = 105, bg = 'gray25')
        moviesRows[f"Row{movieIndex}"].pack()

        moviesRows[movie['name']] = Label(moviesRows[f"Row{movieIndex}"], text = movieName, width = 41,
        bg='gray25', fg = 'white smoke', font=("Calibri", "18"), pady=13, anchor = 'nw') 
        moviesRows[movie['name']].pack(side = LEFT)

        moviesRows[f"{movie['name']} - space1"] = Label(moviesRows[f"Row{movieIndex}"], text = '', bg = 'gray25')
        moviesRows[f"{movie['name']} - space1"].pack(side = LEFT)

        moviesRows[movie['rating']] = Label(moviesRows[f"Row{movieIndex}"], text = movieRating, width = 15, bg = 'gray25', fg = 'gold', font=("Calibri", "18"))
        moviesRows[movie['rating']].pack(side = LEFT)

        moviesRows[f"{movie['name']} - space2"] = Label(moviesRows[f"Row{movieIndex}"], text = '', width = 60, bg = 'gray25')
        moviesRows[f"{movie['name']} - space2"].pack(side = LEFT)

        moviesRows[movieIndex] = Label(moviesRows[f"Row{movieIndex}"], text = 'Opções', width = 10, bg = 'gray25', fg = 'white smoke', font=("Calibri", "18"))
        moviesRows[movieIndex].pack(side = RIGHT)

        moviesRows[f"deleteBtn-{movieIndex}"] = Button(moviesRows[movieIndex], text = 'Excluir', bg = 'brown1', relief = 'flat', fg = 'snow', command = lambda id = movie["id"] : deleteMovie(id, self))
        moviesRows[f"deleteBtn-{movieIndex}"].pack(side = LEFT)

        moviesRows[f"btn{movieIndex}-space"] = Label(moviesRows[movieIndex], text = '', bg = 'gray25', fg = 'gray25')
        moviesRows[f"btn{movieIndex}-space"].pack(side = LEFT)

        moviesRows[f"openBtn-{movieIndex}"] = Button(moviesRows[movieIndex], text = ' Abrir ', fg = 'gray25', command = lambda id = movie["id"] : getMovie(id, self))
        moviesRows[f"openBtn-{movieIndex}"].pack(side = LEFT)

        movieIndex += 1

    def MovieScreen(movie, self):
      self.HomeFrame.pack_forget()

      self.MovieFrame = Frame(None, pady = 20, bg = 'gray25')
      self.MovieFrame.pack()
      
      self.movieScreenExists = TRUE

      title = Label(self.MovieFrame, width=100,text="Ver detalhes de um filme", bg='gray25', fg='white smoke', font=("Calibri", "35"), pady=30) 
      title.pack()

      movieName = Label(self.MovieFrame, width=100,text = f"Filme: {movie['name']}", bg='gray25', fg='white smoke', font=("Calibri", "25")) 
      movieName.pack()

      spacing0 = Label(self.MovieFrame, text = " ", bg = "gray25")
      spacing0.pack()

      movieRating = Label(self.MovieFrame, text = f"Avaliação: {movie['rating']}.0", font = ("Calibri", "25"),width = 50, bg = 'gray25', fg = 'white smoke')
      movieRating.pack()

      spacing1 = Label(self.MovieFrame, text = " ", bg = "gray25")
      spacing1.pack()

      actorsFrame = Frame(self.MovieFrame, bg = 'gray25')
      actorsFrame.pack()

      actorsTitle = Label(actorsFrame, width=100,text='Atores', bg='gray25', fg='white smoke', font=("Calibri", "25"), pady = 10) 
      actorsTitle.pack()

      actorsList = ", ".join(movie['actors'])

      actors = Label(actorsFrame, font = ("Calibri", "20"), width = 50, text = actorsList, bg = 'gray25', fg = 'white smoke')
      actors.pack()

      actorsSpace = Label(actorsFrame, text = " ", bg = "gray25")
      actorsSpace.pack()

      directorsFrame = Frame(self.MovieFrame, bg = 'gray25')
      directorsFrame.pack()

      directorsTitle = Label(directorsFrame, width=100, text = 'Diretores', bg='gray25', fg='white smoke', font=("Calibri", "25"), pady = 10) 
      directorsTitle.pack()

      directorsList = ", ".join(movie['directors'])

      directors = Label(directorsFrame, font = ("Calibri", "20"), width = 50, text = directorsList, bg = 'gray25', fg = 'white smoke')
      directors.pack()

      directorsSpace = Label(directorsFrame, text = " ", bg = "gray25")
      directorsSpace.pack()

      returnBtn = Button(self.MovieFrame, text = " Voltar", bg = 'brown1', fg = 'white smoke', relief='flat', width = 50, font = ("Calibri", "15"), command = lambda : HomeScreen(self))
      returnBtn.pack()

    def getMovies():
      req = {}
      req['method'] = "GET"
      req['id'] = FALSE
      
      self.clienteSckt.sendto(json.dumps(req).encode(), self.address)

      res, address = self.clienteSckt.recvfrom(self.buffer)
      moviesList = json.loads(res)
      return moviesList

    def postMovie(movie, self, actors, directors):
      movie['name'] = self.movieName.get()
      movie['rating'] = int(self.movieRating.get())
      movie['actors'][0] = self.actorName.get()
      movie['directors'][0] = self.directorName.get()

      for i in actors:
        movie['actors'][i] = actors[i].get()

      for j in directors:
        movie['directors'][j] = directors[j].get()

      req = {}
      req['method'] = "POST"
      req['movie'] = movie
      print(movie)
      self.clienteSckt.sendto(json.dumps(req).encode(), self.address)

      res, address = self.clienteSckt.recvfrom(self.buffer)
      if res.decode() == 'ok':
        HomeScreen(self)

    def filterMovies(self, name):
      movies = getMovies()

      if name == '':
        self.HomeFrame.destroy()
        return HomeScreen(self)

      matches = []
      for movie in movies:
        if name.lower() in movie['name'].lower():
          matches.append(movie)

      self.moviesContainer.pack_forget()
      moviesSearchContainer = Frame(self.HomeFrame, bg = "gray25", pady = 20, padx = 40)
      moviesSearchContainer.pack()
      moviesRowsF = {}
      movieIndex = 1
      
      for m in matches:
        name = m["name"]
        rating = m["rating"]
        star = emoji.emojize(':star:', use_aliases=True)
        
        movieName = f"{str(movieIndex)}  - {name}"
        movieRating = star*rating

        moviesRowsF[f"Row{movieIndex}"] = Frame(moviesSearchContainer, width = 105, bg = 'gray25')
        moviesRowsF[f"Row{movieIndex}"].pack()

        moviesRowsF[m['name']] = Label(moviesRowsF[f"Row{movieIndex}"], text = movieName, width = 41,
        bg='gray25', fg = 'white smoke', font=("Calibri", "18"), pady=13, anchor = 'nw') 
        moviesRowsF[m['name']].pack(side = LEFT)

        moviesRowsF[f"{m['name']} - space1"] = Label(moviesRowsF[f"Row{movieIndex}"], text = '', bg = 'gray25')
        moviesRowsF[f"{m['name']} - space1"].pack(side = LEFT)

        moviesRowsF[m['rating']] = Label(moviesRowsF[f"Row{movieIndex}"], text = movieRating, width = 15, bg = 'gray25',
        fg = 'gold', font=("Calibri", "18"))
        moviesRowsF[m['rating']].pack(side = LEFT)

        moviesRowsF[f"{m['name']} - space2"] = Label(moviesRowsF[f"Row{movieIndex}"], text = '', width = 60, bg = 'gray25')
        moviesRowsF[f"{m['name']} - space2"].pack(side = LEFT)

        # Frame para os botões de opções
        moviesRowsF[movieIndex] = Label(moviesRowsF[f"Row{movieIndex}"], text = 'Opções', width = 10, bg = 'gray25', fg = 'white smoke', font=("Calibri", "18"))
        moviesRowsF[movieIndex].pack(side = RIGHT)

        moviesRowsF[f"deleteBtn-{movieIndex}"] = Button(moviesRowsF[movieIndex], text = 'Excluir', bg = 'brown1', relief = 'flat', fg = 'snow', command = lambda  : deleteMovie(m, self))
        moviesRowsF[f"deleteBtn-{movieIndex}"].pack(side = LEFT)

        moviesRowsF[f"btn{movieIndex}-space"] = Label(moviesRowsF[movieIndex], text = '', bg = 'gray25')
        moviesRowsF[f"btn{movieIndex}-space"].pack(side = LEFT)

        moviesRowsF[f"btn-{movieIndex}-2"] = Button(moviesRowsF[movieIndex], text = ' Abrir ', fg = 'gray25')
        moviesRowsF[f"btn-{movieIndex}-2"].pack(side = LEFT)

        movieIndex += 1

    def newActor(frame, indice, entry, actors, spaces):
      actors.append('')
      entry[indice] = Entry(frame, font = ("Calibri", "15"), width = 50, textvariable = actors[indice])
      entry[indice].insert(0, "Nome do {}° ator/atriz".format(indice+1))
      entry[indice].bind("<FocusIn>",lambda args: entry[indice].delete('0', 'end'))
      entry[indice].pack(side = TOP)

      spaces[f"spacing{indice}"] = Label(frame, text = " ", bg = "gray25")
      spaces[f"spacing{indice}"].pack()

    def newDirector(frame, indice, entry, directors, spaces):
      directors.append('')
      entry[indice] = Entry(frame, font = ("Calibri", "15"), width = 50, textvariable = directors[indice])
      entry[indice].insert(0, "Nome do {}° diretor(a)".format(indice+1))
      entry[indice].bind("<FocusIn>",lambda args: entry[indice].delete('0', 'end'))
      entry[indice].pack(side = TOP)

      spaces[f"spacing{indice}"] = Label(frame, text = " ", bg = "gray25")
      spaces[f"spacing{indice}"].pack()

    def deleteMovie(id, self):
      req = {}
      req['method'] = "DELETE"
      req['id'] = id

      self.clienteSckt.sendto(json.dumps(req).encode(), self.address)

      res, address = self.clienteSckt.recvfrom(self.buffer)
      if res.decode() == 'ok':
        self.HomeFrame.destroy()
        HomeScreen(self)

    def getMovie(id, self):
      req = {}
      req['method'] = "GET"
      req['id'] = id

      self.clienteSckt.sendto(json.dumps(req).encode(), self.address)

      res, address = self.clienteSckt.recvfrom(self.buffer)
      movie = json.loads(res)

      if movie:
        MovieScreen(movie, self)

    HomeScreen(self)

root = Interface()
# root.state('zoomed')
root.master.title("MoviesFlix")
mainloop()