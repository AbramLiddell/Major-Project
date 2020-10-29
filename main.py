import os
import pygame as pg
import sys
from pygame.locals import *
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir, "assets")
sounds_dir = os.path.join(assets_dir, "sounds")
images_dir = os.path.join(assets_dir, "images")
sprites_dir = os.path.join(images_dir, "sprites")

print("\nDIRECTORIES:")
print("     " + main_dir)
print("     " + assets_dir)
print("     " + sounds_dir)
print("     " + images_dir)
print("     " + sprites_dir + "\n")

# Colour Pallette:
# Pink - #fa448c
# Yellow - #fec859
# Aqua/Green - #43b5a0
# Dark Purple - #491d88
# Light Black/Red - #331a38

def load_image(name, colorkey=None):
    fullname = os.path.join(images_dir, name)
    try:
        image = pg.image.load(fullname)
    except pg.error:
        print("ERROR: Cannot load image:", fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(sounds_dir, name)
    try:
        sound = pg.mixer.Sound(fullname)
    except pg.error:
        print("Cannot load sound: %s" % fullname)
        raise SystemExit(str(geterror()))
    return sound
    
class Player(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image("player.png", -1)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9

    def move(self):
        # Move according to mouse position
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pg.transform.flip(self.image, 1, 0)
            self.rect = newpos


def main():
    # Initialize Everything
    screen = pg.display.set_mode((1280, 720))
    pg.display.set_caption("Concentrate")
    pg.mouse.set_visible(1)
    clock = pg.time.Clock()

    # Create The Main Menu Surface
    mainMenuSurface = pg.Surface(screen.get_size())
    mainMenuSurface = mainMenuSurface.convert()
    mainMenuSurface.fill((250, 250, 250))

    # Create The Config Menu Surface
    configMenuSurface = pg.Surface(screen.get_size())
    configMenuSurface = configMenuSurface.convert()
    configMenuSurface.fill((250, 250, 250))

    # Call The Various Menus
    mainMenu(mainMenuSurface, screen, clock)
    configMenu(configMenuSurface, screen, clock)

    print("GAME STATUS: Running")
    # Prepare Game Objects
    
    #button_sound = load_sound("button_sound.wav")
    #barrier_sound = load_sound("barrier_sound.wav")
    #death_sound = load_sound("death_sound.wav")
    #player = Player()


def mainMenu(mainMenuSurface, screen, clock):

    # Title Text
    font = pg.font.Font(None, 55)
    text = font.render("Concentrate", 1, (10, 10, 10))
    textpos = text.get_rect(centerx=round(mainMenuSurface.get_width() / 2), centery=round(mainMenuSurface.get_height()/3))
    mainMenuSurface.blit(text, textpos)

    # Start Game TExt
    font = pg.font.Font(None, 30)
    text = font.render("Start Game", 1, (10, 10, 10))
    startpos = text.get_rect(centerx=round(mainMenuSurface.get_width() / 2), centery=round(mainMenuSurface.get_height()/2))
    mainMenuSurface.blit(text, startpos)

    # Instructions Text
    text = font.render("Instructions", 1, (10, 10, 10))
    instructionpos = text.get_rect(centerx=round(mainMenuSurface.get_width() / 2), centery=round(mainMenuSurface.get_height()/2) + round(1.5*(startpos.bottomright[1]-startpos.topleft[1])))
    mainMenuSurface.blit(text, instructionpos)

    # Display The Surface
    screen.blit(mainMenuSurface, (0, 0))
    pg.display.flip()

    # Loop For The Menu - Keeps Screen At 60FPS and Loops Until Otherwise Instructed
    menuGoing = True
    while menuGoing == True:
        clock.tick(60)
        
        for event in pg.event.get():
            mousePos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if mousePos[0] >= startpos.topleft[0] and mousePos[0] <= startpos.bottomright[0] and mousePos[1] <= startpos.bottomright[1] and mousePos[1] >= startpos.topleft[1]:
                    menuGoing = False
                    print("Start Game")
                elif mousePos[0] >= instructionpos.topleft[0] and mousePos[0] <= instructionpos.bottomright[0] and mousePos[1] <= instructionpos.bottomright[1] and mousePos[1] >= instructionpos.topleft[1]:
                    print("Instructions")
                

def configMenu(configMenuSurface, screen, clock):
    # Title Text
    font = pg.font.Font(None, 55)
    text = font.render("Game Configuration", 1, (10, 10, 10))
    textpos = text.get_rect(centerx=round(configMenuSurface.get_width() / 2), centery=round(configMenuSurface.get_height()/3))
    configMenuSurface.blit(text, textpos)

    # Start Game Text
    font = pg.font.Font(None, 30)
    text = font.render("Start Game", 1, (10, 10, 10))
    startpos = text.get_rect(centerx=round(configMenuSurface.get_width() / 2), centery=round(configMenuSurface.get_height()/2))
    configMenuSurface.blit(text, startpos)

    # Instructions Text
    text = font.render("Instructions", 1, (10, 10, 10))
    instructionpos = text.get_rect(centerx=round(configMenuSurface.get_width() / 2), centery=round(configMenuSurface.get_height()/2) + round(1.5*(startpos.bottomright[1]-startpos.topleft[1])))
    configMenuSurface.blit(text, instructionpos)

    # Display The Surface
    screen.blit(configMenuSurface, (0, 0))
    pg.display.flip()

    # Loop For The Config Menu - Does The Same As Main Menu Loop
    menuGoing = True
    while menuGoing == True:
        clock.tick(60)
        
        for event in pg.event.get():
            mousePos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if mousePos[0] >= startpos.topleft[0] and mousePos[0] <= startpos.bottomright[0] and mousePos[1] <= startpos.bottomright[1] and mousePos[1] >= startpos.topleft[1]:
                    menuGoing = False
    
def startupChecks():
    if not pg.font:
        print("WARNING: Fonts disabled.")
    if not pg.mixer:
        print("WARNING: Sounds disabled.")


if __name__ == "__main__":
    pg.init()
    startupChecks()
    main()
