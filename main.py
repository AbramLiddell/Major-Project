import os
import pygame as pg
import sys
import time
from pygame.locals import *
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir, "Assets")
sounds_dir = os.path.join(assets_dir, "Sounds")
images_dir = os.path.join(assets_dir, "Images")
sprites_dir = os.path.join(images_dir, "Sprites")

print("\nConcentrate: A Game By Abram Liddell")
print("\nDIRECTORIES:")
print("     " + main_dir)
print("     " + assets_dir)
print("     " + sounds_dir)
print("     " + images_dir)
print("     " + sprites_dir + "\n")

global gameStarted
global bordernum
bordernum = 0
gameStarted = False
border = []

# Colour Pallette:
# Pink - #fa448c
# Yellow - #fec859
# Aqua/Green - #43b5a0
# Dark Purple - #491d88
# Light Black/Red - #331a38

# Standardised Fuction For Loading In Images
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
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        print("Loading Sprite")
        self.image = load_sprite("square.png", -1)
        self.rect = self.image.get_rect()
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
    def update(self, move):
        self.rect.x += move[0]
        self.rect.y += move[1]


        
    def move(self):
        # Move according to mouse position
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pg.transform.flip(self.image, 1, 0)
            self.rect = newpos
class Border():
    global bordernum
    def __init__(self):
        self.x = generateX()
        self.y = generateY()
        self.width = generateWidth()

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
    global bordernum

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
    startTime = getPerfTime()

    print("\nGAME STATUS: Running\n")
    print("Time Started At: " + str(startTime))
    drawGame(gameSurface, screen, clock)
    
    # Prepare Game Objects
    #button_sound = load_sound("button_sound.wav")
    #barrier_sound = load_sound("barrier_sound.wav")
    #death_sound = load_sound("death_sound.wav")
    
    player = Player()

    currentTimer = getPerfTime()
    gameTime = currentTimer - startTime

    print("Game Time: " + str(gameTime))
    #have game countdown here
    #while (gameTime <= 3):
    playerPosition = 600
    border.append(Border())
    allSprites = pg.sprite.RenderPlain((player))
    screen.blit(gameSurface, (0, 0))
    allSprites.draw(screen)
    pg.display.flip()



    allSprites.add(player)


    playerMoveX = 0
    playerMoveY = 0
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    playerMoveY -= 2
                if event.key == K_s:
                    playerMoveY += 2
                if event.key == K_a:
                    playerMoveX -= 2
                if event.key == K_d:
                    playerMoveX += 2
            elif event.type == KEYUP:
                if event.key == K_a:
                    playerMoveX += 2
                elif event.key == K_d:
                    playerMoveX -= 2
                elif event.key == K_w:
                    playerMoveY += 2
                elif event.key == K_s:
                    playerMoveY -= 2

        player.update((playerMoveX, playerMoveY))    
    
        bordernum += 1
        border.append(Border())
#        allSprites.update()
        screen.blit(gameSurface, (0, 0))
        allSprites.draw(screen)
        pg.display.flip()
        pg.time.Clock().tick(60)
    
    
    
    #print(border[0].x)
    #print(border[0].y)
    #print(border[0].width)
    #print(border[bordernum].x)
    #print(border[bordernum].y)
    #print(border[bordernum].width)

def getPerfTime():
    return time.perf_counter()

def generateX():
    global bordernum
    if bordernum == 0:
        #return borderwidth
        return 1000
    else:
        return border[bordernum-1].x - 100

def generateY():
    # randomboi
    return 100

def generateWidth():
    # randomboi 
    return 100

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

def drawGame(gameSurface, screen, clock):
    # Fill white to stop bolding - clear screen
    gameSurface.fill((250, 250, 250))

    # Background
    #gameBackgroundImage = load_image("Config-Menu.png")
    #gameRect = gameBackgroundImage.get_rect()
    #blit_alpha(gameSurface, gameBackgroundImage, gameRect, 255)

    
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
