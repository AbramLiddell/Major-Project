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
        self.dizzy = 0

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

    # Create The Backgound
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    clock = pg.time.Clock()
    mainMenu(background, screen, clock)

    # Prepare Game Objects
    
    #button_sound = load_sound("button_sound.wav")
    #barrier_sound = load_sound("barrier_sound.wav")
    #death_sound = load_sound("death_sound.wav")
    #player = Player()


def mainMenu(background, screen, clock):

    # Title On Background
    font = pg.font.Font(None, 55)
    text = font.render("Concentrate", 1, (10, 10, 10))
    textpos = text.get_rect(centerx=int(background.get_width() / 2), centery=int(background.get_height()/3))
    background.blit(text, textpos)

    # Start Game On Background
    font = pg.font.Font(None, 30)
    text = font.render("Start Game", 1, (10, 10, 10))
    startpos = text.get_rect(centerx=int(background.get_width() / 2), centery=int(background.get_height()/2))
    background.blit(text, startpos)

    # Instructions On Background
    text = font.render("Instructions", 1, (10, 10, 10))
    instructionpos = text.get_rect(centerx=int(background.get_width() / 2), centery=int(background.get_height()/2) + 1.5*(startpos.bottomright[1]-startpos.topleft[1]))
    background.blit(text, instructionpos)

    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()

    menuGoing = True
    while menuGoing == True:
        clock.tick(60)
        
        for event in pg.event.get():
            mousePos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if mousePos[0] >= startpos.topleft[0] and mousePos[0] <= startpos.bottomright[0] and mousePos[1] <= startpos.bottomright[1] and mousePos[1] >= startpos.topleft[1]:
                    menuGoing = False
                    print("Start Game")
                elif mousePos[0] >= instructionpos.topleft[0] and mousePos[0] <= instructionpos.bottomright[0] and mousePos[1] <= instructionpos.bottomright[1] and mousePos[1] >= instructionpos.topleft[1]:
                    print("Instructions")
        if event.type == pg.QUIT:
            exit(0)


def startupChecks():
    if not pg.font:
        print("WARNING: Fonts disabled.")
    if not pg.mixer:
        print("WARNING: Sounds disabled.")


if __name__ == "__main__":
    pg.init()
    startupChecks()
    main()
