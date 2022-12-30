class Player():
    def __init__(self, heightScreen, widthScreen, role):
        self.position = {"x" : 0, "y" : 0}
        self.role = role
        self.heightScreen = heightScreen
        self.widthScreen = widthScreen
        self.abletoShot = True
        self.shooting = False
        self.shotPosition = {"x" : 1, "y" : 0}
        self.score = 0
        self.winner = False
        if self.role == 2:
          self.position["x"] = self.widthScreen - 1
          self.shotPosition["x"] = self.widthScreen - 2
    
    def moveUp(self, _):
        if self.position["y"] > 0:
             self.position["y"] -= 1
             if self.abletoShot:
                 self.shotPosition["y"] = self.position["y"]
    
    def moveDown(self, _):
        if self.position["y"] < self.heightScreen - 1:
             self.position["y"] += 1
             if self.abletoShot:
                 self.shotPosition["y"] = self.position["y"]
    
    def shot(self, _):
        if self.abletoShot:
            self.shooting = True
            self.abletoShot = False

    def bulletAgain(self, opponent):
          if self.role == 1:
              self.shotPosition["x"] += 1
              if opponent.position == self.shotPosition:
                  self.score += 1
                  print("Player 1 has shot Player 2")
                  print("########")
                  print("Score")
                  print("Player 1: ", self.score, " -- Player 2: ", opponent.score)
                  print("########")
              elif (opponent.shotPosition["x"] == self.shotPosition["x"] and opponent.shotPosition["y"] <= self.shotPosition["y"] and opponent.shooting) or (self.shotPosition["x"] > self.widthScreen - 1):
                     self.shotPosition = {"x" : 1, "y" :  self.position["y"]}
                     self.shooting = False
                     self.abletoShot = True     
          else:
              self.shotPosition["x"] -= 1
              if opponent.position == self.shotPosition:
                  self.score += 1
                  print("Player 2 has shot Player")
                  print("########")
                  print("Score")
                  print("Player 1: ",  opponent.score , " -- Player 2: ", self.score)
                  print("########")
              elif (opponent.shotPosition["x"] == self.shotPosition["x"] and opponent.shotPosition["y"] >= self.shotPosition["y"] and opponent.shooting) or (self.shotPosition["x"] < 0):
                     self.shotPosition = {"x" : self.widthScreen - 2, "y" :  self.position["y"]}
                     self.shooting = False
                     self.abletoShot = True
                     
    def resetState(self):
        self.position = {"x" : 0, "y" : 0}
        self.abletoShot = True
        self.shooting = False
        self.shotPosition = {"x" : 1, "y" : 0}
        self.score = 0
        self.winer = False
        if self.role == 2:
          self.position["x"] = self.widthScreen - 1
          self.shotPosition["x"] = self.widthScreen - 2
           