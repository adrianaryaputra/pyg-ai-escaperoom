import pygame, easygui, pickle

from src.game.map import Map
from src.game.player import Player
from src.game.obstacle import BouncingObstacle
from src.game.button import Button
from src.game.colorscheme import COLOR



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
            self.obstacles.add(BouncingObstacle(self.map, obstacle["position"], obstacle["size"], obstacle["speed"]))
        




def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Map Maker")
    FPS = 60
    clock = pygame.time.Clock()

    level = Level(screen)

    obs = BouncingObstacle(level.map, (300,300), 20, 5, 1)
    obs.play()

    obs2 = BouncingObstacle(level.map, (200, 300), 40, 5, 0)
    obs2.play

    buttons = pygame.sprite.Group()
    buttons.add(Button(screen, (10, 10), (150, 40), "Load Map", level.dataLoad))
    buttons.add(Button(screen, (10, 60), (150, 40), "Save Map", level.dataSave))

    # Add Surrounding Wall
    for i in range(16):
        level.map.blocks[i].onMouseDown()
        level.map.blocks[-i-1].onMouseDown()
    for i in range(1, 25):
        level.map.blocks[i*16].onMouseDown()
        level.map.blocks[(i+1)*16-1].onMouseDown()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            level.map.handleEvent(event)
            level.player.handleEvent(event)
            # obs.handleEvent(event)
            for button in buttons:
                button.handleEvent(event)

        screen.fill(COLOR.BG)

        level.map.draw()
        level.map.update()

        level.player.draw()
        is_collide = level.player.update([obs, obs2])
        if is_collide:
            break  # GAME OVER!!!

        obs.draw()
        obs.update()
        obs2.draw()
        obs2.update()

        buttons.draw(screen)
        buttons.update()

        pygame.display.update()
        clock.tick(FPS)



if __name__ == '__main__':
    main()