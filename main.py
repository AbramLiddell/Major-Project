import os
import pygame as pg
import sys
import time
from pygame.locals import *
from pygame.compat import geterror
import random
from multiprocessing import Process
from PIL import Image

main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir, "Assets")
sounds_dir = os.path.join(assets_dir, "Sounds")
images_dir = os.path.join(assets_dir, "Images")
sprites_dir = os.path.join(images_dir, "Sprites")
test_dir = os.path.join(images_dir, "pathGenTesting")

print("\nConcentrate: A Game By Abram Liddell")
print("\nDIRECTORIES:")
print("     " + main_dir)
print("     " + assets_dir)
print("     " + sounds_dir)
print("     " + images_dir)
print("     " + sprites_dir)
print("     " + test_dir + "\n")


global gameStarted
global borderSpeed
borderSpeed = 1
gameStarted = False
oldY = 0


# Colour Pallette:
# Pink - #fa448c
# Yellow - #fec859
# Aqua/Green - #43b5a0
# Dark Purple - #491d88
# Light Black/Red - #331a38

# Standardised Fuctions For Loading In Images and Sprites
def load_image(name, colorkey=None):
    fullname = os.path.join(images_dir, name)
    try:
        image = pg.image.load(fullname)
        print("STATUS: Image loaded.")
    except pg.error:
        print("ERROR: Cannot load image:", fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image

    # Standardised Fuction For Loading In Sprites
def load_sprite(name, colorkey=None):
    fullname = os.path.join(sprites_dir, name)
    print("Sprite Name: " + fullname)
    try:
        image = pg.image.load(fullname)
        print(fullname)
        print("STATUS: Image loaded.")
    except pg.error:
        print("ERROR: Cannot load image:", fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image

# Standardised Fuction For Loading In Sounds
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

# Class Controlling The Player
class Player(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # Call Sprite intializer
        print("Loading Sprite")
        self.image = pg.transform.scale(load_sprite("square.png", -1), (50, 50))
        self.rect = self.image.get_rect()
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
    def update(self, move):

        # Border Detection
        if self.rect.x + move[0] >= 1280 or self.rect.x + move[0] <= 0:
            pass
        else:
            self.rect.x += move[0]

        if self.rect.y + move[1] <= 0 or self.rect.y + move[1] >= 720:
            pass
        else:
            self.rect.y += move[1]

# Class Controlling the Borders
class Border(pg.sprite.Sprite):
    global borderSpeed
    #global borderRequired
    global oldY

    borderSpeed = 2
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = load_sprite("border.png", None)
        self.rect = self.image.get_rect()
        self.rect.topleft = 1280, -720
        self.rect.x = 1280
        self.rect.y = 0
        self.y = 340
        self.width = 40
        self.borderRequired = False
        # self.passageGroup.add(self.passage)
        self.pathwayImage = pg.transform.scale(load_sprite("border-passageway.png", None), (50, self.width))
        self.pathRect = self.pathwayImage.get_rect()
        self.pathRect.x = 1280
        self.pathRect.y = 0

        print(self.rect)

    def update(self, screen):

        # Note: This comment is resource heavy.
        #print("STATUS: Borders Updating.")

        oldY = self.y


        self.width = self.generateWidth()
        self.rect.x = self.rect.x - borderSpeed
        self.y =+ self.generateY()
        self.pathRect.x = self.rect.x
        self.pathRect.y = self.y

        # Add the passageway somewhere here


        #print(self.rect.x)
        #print(borderRequired)

        if self.borderRequired == False:
            if self.rect.x < 1000:
                self.borderRequired = True
            else:
                self.borderRequired = False
        elif self.borderRequired == True:
            self.borderRequired = False

        
    def generateY(self):
        
        # y = oldY
        # print(y)
        # print(oldY)
        # if y + oldY >= 720:
        #     y = int(720-oldY-self.width)
        # else:
        #     y = int(oldY + random.randint(-1*oldY, oldY))
        #     print(y)
        return 300
        
    def generateWidth(self):
        # return (720/random.randint(70, 140))
        return 200
    # def drawLine(self, surface):
    #     pg.draw.line(surface, (0, 0, 0), (0, 660), (1280, 660))
    #     pg.draw.line(surface, (0, 0, 0), (0, 780), (1280, 780))
class Path(pg.sprite.Sprite):
    def __init__(self, borderY, pathGradient, pathWidth, pathImage):
        pg.sprite.Sprite.__init__(self)
        self.y = self.getY(borderY, pathGradient, pathWidth, pathImage)
        self.width = 40

    def getY(self, borderY, pathGradient, pathWidth, pathImage):
        generateImageProcess = Process(target=genImgProcess, args=(borderY, pathGradient, pathWidth, pathImage))
        generateImageProcess.start()

def genImgProcess(q, w, e, r):

    with Image.open(sprites_dir + r"\basePath.png") as im:
        im.rotate(45).show()
        im.save(test_dir + r"\generated45.png", format="PNG")
    print("Process Finished: "+ str(q), str(w), str(e), str(r))

# Class Controlling the Sounds
class Sounds():
    def __init__(self):
        self.loadSounds()

    def loadSounds(self):
        self.deathSound = load_sound("death_sound.wav")
        self.timerSound = load_sound("timer_sound.wav")
        self.startSound = load_sound("start_sound.wav")
        self.buttonSound = load_sound("button_sound.wav")
        self.gameMusicSound = load_sound("gameMusic_sound.wav")
        self.menuMusicSound = load_sound("menuMusic_sound.wav")

# Loads Images With Transparency
def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pg.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)

# Main Sub Which Controls All Other Game Functions
def main():

    global gameStarted
    borderRequired = True

    # Initialize Everything Required For Game Operation
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

    # Create The Instruction Menu Surface
    instructionMenuSurface = pg.Surface(screen.get_size())
    instructionMenuSurface = instructionMenuSurface.convert()
    instructionMenuSurface.fill((250, 250, 250))

    # Create The Game Surface
    gameSurface = pg.Surface(screen.get_size())
    gameSurface = gameSurface.convert()
    gameSurface.fill((250, 250, 250))

    # Call The Various Menus
    while not gameStarted:
        mainMenu(mainMenuSurface, screen, clock, instructionMenuSurface)
    configMenu(configMenuSurface, screen, clock)

    print("\nGAME STATUS: Running.\n")
    drawGame(gameSurface, screen, clock)
    
    #sounds = Sounds()
    player = Player()
    border = Border()
    path = Path(borderY=border.y, pathGradient=0, pathWidth=0, pathImage=0)

    allSprites = pg.sprite.RenderPlain((player))
    borderGroup = pg.sprite.Group()
    pathGroup = pg.sprite.Group()

    borderGroup.add(border)
    allSprites.add(player)
    pathGroup.add(path)
    screen.blit(gameSurface, (0, 0))
    pg.display.flip()

    playerMoveX = 0
    playerMoveY = 0
    speed = 3
    fps_count = 0

    # Main Loop
    while True:
        fps_count += 1
        # Keyboard detection
        for event in pg.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    playerMoveY -= speed
                if event.key == K_s:
                    playerMoveY += speed
                if event.key == K_a:
                    playerMoveX -= speed
                if event.key == K_d:
                    playerMoveX += speed
            elif event.type == KEYUP:
                if event.key == K_a:
                    playerMoveX += speed
                elif event.key == K_d:
                    playerMoveX -= speed
                elif event.key == K_w:
                    playerMoveY += speed
                elif event.key == K_s:
                    playerMoveY -= speed

        # Update player the position of each object
        player.update((playerMoveX, playerMoveY))  
        
        # Border collision detection and update passageway
        for border in borderGroup:
            if player.rect.colliderect(border):
                if player.rect.y < border.y or player.rect.y > (border.y + border.width):
                    print("STATUS: Border Collision.")

        borderGroup.update(screen)
        pathGroup.update(screen)

        # Create a new border if it is required, and remove old ones.
        if border.borderRequired == True:
            path = Path(borderY=border.y, pathGradient=0, pathWidth=0, pathImage=0)
            border = Border()

            borderGroup.add(border)
            pathGroup.add(path)
            print("STATUS: Border Added.")

            # Remove borders once they're past the edge of the screen
            # to prevent excess RAM usage and lag.
            for border in borderGroup:
                if border.rect.x < 100:
                    borderGroup.remove(border)
                    print("STATUS: Border Removed.")
            
            
            for path in pathGroup:
                if path.rect.x < 100:
                    pathGroup.remove(path)
                    print("STATUS: Path Removed.")

        

        # Display all changes
        screen.blit(gameSurface, (0, 0))
        borderGroup.draw(screen)

        # Reenable this line once the auto-image generation is created.
        #pathGroup.draw(screen)

        allSprites.draw(screen)
        pg.display.flip()
        pg.time.Clock().tick(220)
    
# Gets the time - for scoring purposes later.
def getPerfTime():
    return time.perf_counter()

# Main Menu Function
def mainMenu(mainMenuSurface, screen, clock, instructionMenuSurface):
    global gameStarted

    # Fill white to stop bolding - clear screen
    mainMenuSurface.fill((250, 250, 250))

    # Title Text
    font = pg.font.Font(None, 55)
    text = font.render("Concentrate", 1, (10, 10, 10))
    textpos = text.get_rect(centerx=round(mainMenuSurface.get_width() / 2), centery=round(mainMenuSurface.get_height()/3))
    mainMenuSurface.blit(text, textpos)

    # Start Game Text
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
                    gameStarted = True
                    print("CONTROL: Start Game")
                elif mousePos[0] >= instructionpos.topleft[0] and mousePos[0] <= instructionpos.bottomright[0] and mousePos[1] <= instructionpos.bottomright[1] and mousePos[1] >= instructionpos.topleft[1]:
                    print("CONTROL: Instructions")
                    instructionMenu(instructionMenuSurface, screen, clock)
                    menuGoing = False

# Configuration Menu Function
def configMenu(configMenuSurface, screen, clock):
    
    # Fill white to stop bolding - clear screen
    configMenuSurface.fill((250, 250, 250))

    # Background
    configBackgroundImage = load_image("Config-Menu.png")
    configRect = configBackgroundImage.get_rect()
    blit_alpha(configMenuSurface, configBackgroundImage, configRect, 255)

    # Start Game Text
    font = pg.font.Font(None, 40)
    text = font.render("Start", 1, (250, 250, 250))
    startpos = text.get_rect(centerx=round(configMenuSurface.get_width() / 2), centery=670)
    configMenuSurface.blit(text, startpos)

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
                    print("CONTROL: Config Start")

# Instruction Menu Function
def instructionMenu(instructionMenuSurface, screen, clock):

    # Fill white to stop bolding - clear screen
    instructionMenuSurface.fill((250, 250, 250))

    # Title Text
    font = pg.font.Font(None, 40)
    TitleText = font.render("Instructions", 1, (10, 10, 10))
    startpos = TitleText.get_rect(centerx=round(instructionMenuSurface.get_width() / 2), centery=round(instructionMenuSurface.get_height()/3 - 100))

    # Back Button Text
    font = pg.font.Font(None, 30)
    BackText = font.render("Back", 1, (10, 10, 10))
    backpos = BackText.get_rect(centerx=round(instructionMenuSurface.get_width() / 6 - 100), centery=round(instructionMenuSurface.get_height()/6 - 50))
    
    # Blit Text to Screen
    instructionMenuSurface.blit(TitleText, startpos)
    instructionMenuSurface.blit(BackText, backpos)

    # Display The Surface
    screen.blit(instructionMenuSurface, (0, 0))
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
                if mousePos[0] >= backpos.topleft[0] and mousePos[0] <= backpos.bottomright[0] and mousePos[1] <= backpos.bottomright[1] and mousePos[1] >= backpos.topleft[1]:
                    menuGoing = False
                    print("CONTROL: Back")

# This sub draws the game initially
def drawGame(gameSurface, screen, clock):
    
    # Fill white to stop bolding - clear screen
    gameSurface.fill((250, 250, 250))
    screen.blit(gameSurface, (0, 0))
    pg.display.flip()

# Startup Function to Ensure Modules Are Loaded
def startupChecks():
    if not pg.font:
        print("WARNING: Fonts disabled.")
    if not pg.mixer:
        print("WARNING: Sounds disabled.")
if __name__ == "__main__":
    pg.init()
    startupChecks()
    
    main()
