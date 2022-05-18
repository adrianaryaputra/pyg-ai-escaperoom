import pygame, easygui, pickle

from .player import Player
from .obstacle import BouncingObstacle, RotatingObstacle
from .map import Map



class Level:
    def __init__(self, screen):
        self.screen = screen
        
        self.map = Map(screen, (10, 110), (26, 16), 30)
        self.player = Player(self.map, (400, 300), 20, 5) 
        self.obstacles = pygame.sprite.Group()


    def dataSave(self):
        # use easygui to get save filepath
        path = easygui.filesavebox(msg="Escape Room", title="Save your hard worked level", default="levelX_Y.map", filetypes=["*.map"])
        save = {
            "map": self.map.dataSave(),
            "player": self.player.dataSave(),
            "obstacles": [obstacle.dataSave() for obstacle in self.obstacles]
        }
        with open (path, "wb") as file:
            pickle.dump(save, file)


    def dataLoad(self):
        # use easygui to get filepath
        path = easygui.fileopenbox(msg="Escape Room", title="Load your hard worked level", default="levelX_Y.map", filetypes=["*.map"])
        with open (path, "rb") as file:
            save = pickle.load(file)
        self.map.dataLoad(save["map"])
        self.player.dataLoad(save["player"])
        for obstacle in save["obstacles"]:
            if obstacle["type"] == "BouncingObstacle":
                self.obstacles.add(BouncingObstacle(self.map, obstacle["position"], obstacle["size"], obstacle["speed"], obstacle["direction"]))
            elif obstacle["type"] == "RotatingObstacle":
                self.obstacles.add(RotatingObstacle(self.map, obstacle["position"], obstacle["size"], obstacle["speed"], obstacle["direction"]))


    def createVObstacle(self):
        self.obstacles.add(BouncingObstacle(self.map, self.player.rect.center, 20, 5, 1))

    
    def createHObstacle(self):
        self.obstacles.add(BouncingObstacle(self.map, self.player.rect.center, 20, 5, 0))


    def createCWObstacle(self):
        self.obstacles.add(RotatingObstacle(self.map, self.player.rect.center, 20, 2, -1))


    def createCCWObstacle(self):
        self.obstacles.add(RotatingObstacle(self.map, self.player.rect.center, 20, 2, 1))


    def playObstacles(self):
        for obstacle in self.obstacles:
            obstacle.play()


    def stopObstacles(self):
        for obstacle in self.obstacles:
            obstacle.stop()