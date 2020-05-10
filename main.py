# sprite calsses
# Created by Angie Hollingworth
# HIT137 2019

# This is the main file to run the game
# This game is a side scolling platform game
# The object of the game is to collect musg=hrooms for points and lives
# Avoid zombies, or throw little mushrooms at them with yoru space bar
# you only have 3 mushrooms at a time so use them wisely

#game imports
import pygame
import random
#To Check for existance of text files without exceptions
import os

from settings import * # This is the settings file that is required to run the game
from sprites import * # This is the sprites file that is required to run the game

game_title = ('A walk in the park')

# Initiate High score, either open existing file or create new one
def high_score(): #Check for high score file, or create one
    '''Either read or create a high score file'''
    highscorefile = os.path.isfile("highscore.txt") # Check if high score file exists
    if highscorefile:
        highfile = open("highscore.txt").readline()# If it does read in the high score
        highscore = int(highfile)
        return highscore# return the high score to display in the game
    else:
        highscore = 0
        highfile = open("highscore.txt", "w")# otherwise create it
        highfile.write('0')
        highfile.close()
        return int(highscore)# return the high score to display in the game

def new_high_Score(score):
    '''Update the high score in the high score file'''
    highfile = open("highscore.txt", "w")
    score = str(score)
    highfile.write(score)# add new high score
    highfile.close()
    return score

score = 0 # Set your score for this gamt to 0

class Game:
    '''This is the game class to run the game'''
    def __init__(self):
        '''Setup and initialise game window & settings\
        Start timers, set up the background and reset any values to defaults.'''
        pygame.init()
        pygame.mixer.init() #to allow sounds
        self.window = pygame.display.set_mode((window_width, window_height))# set the game window
        pygame.display.set_caption(game_title)
        self.clock = pygame.time.Clock() #seet the clock
        self.running = True
        pygame.time.set_timer(pygame.USEREVENT+2, random.randrange(200, 1500))# This limits how often a platform will generate

        #Background scrolling images
        self.bg = pygame.image.load('images/bg.png').convert() #Background images
        self.bg = pygame.transform.scale(self.bg, (window_width,window_height))# scale to window size
        self.bgX = 0# set position of first
        self.bgX2 = window_width#set next to first image off screen for scrollling
        self.lastbottom = 0 # The x position of the last ground sprite
        self.speed = speed #set game speed
        self.livecount = 5 # player lives
        self.game_over = False
        self.highscore = high_score()


    def new(self):
        '''Start a new game.\
        Start the game music, load sprite groups & sprite sheets\
        Load the player and draw in the first lot of ground images'''
        pygame.mixer.music.load('sounds/soundtrack.mp3') #Load soundtrack for game
        pygame.mixer.music.play(-1) #Put the osng on a loop
        pygame.mixer.music.set_volume(1)
        # Load all Sprite groups
        self.game_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.grounds = pygame.sprite.Group()
        self.groundends = pygame.sprite.Group()
        self.waters = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.bonuses = pygame.sprite.Group()
        self.bonuslife = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.lives = pygame.sprite.Group()
        self.liveslost = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.enemy_level=1 # Level for how many enemy objects are added

        #Load Player sprites
        self.enemyspritesheet = Spritesheet('images/ewalk.png') #Load enemey walking picture
        self.spritesheetwalk = Spritesheet('images/walking.png') #Load player walking picture
        self.spritesheetjump = Spritesheet('images/jump.png') #Load player jumping picture
        self.spritesheetground = Spritesheet('images/ground.png') #Load ground pictures

        self.player = Player(self) #Set up player
        self.player_group.add(self.player)
        self.draw_lives() #Draw life mushroom on the screen

        # Load first ground items before scrolling starts
        pwx = self.lastbottom #Set platform water x variable to last ground x position
        for water in range(0,3):
            gw = GroundWater(pwx, window_height-57, 74,57, self) # Load a ground water object
            self.waters.add(gw) # Add to water sprite group
            self.game_sprites.add(gw) # Add to game spritea group
            pwx = gw.rect.x+74 # Add the size of one water brick to x position eofre loading next oiece
        gl = GroundLandLeft(165, window_height-74, 74,74, self) #Next is a left lnd piece
        groundwidth = len(self.grounds)+ len(self.waters) # Set whole ground width so far to include water and first left piece
        pGquantity = random.randint(3,12)# Select how many middles are being drawn
        pgx = gl.rect.x+74 # Set platform ground x variable to +74 for next image
        for plat in range(0,pGquantity):
            gm = GroundLandMiddle(pgx, gl.rect.y, 74,74, self) # Add a ground middle piece
            self.platforms.add(gm) # Add to sprite groups
            self.grounds.add(gm)
            self.game_sprites.add(gm)
            pgx = gm.rect.x+74 # Set platform ground x variable to +74 for next image
        gr = GroundLandRight(pgx, gm.rect.y, 74,74, self)# Add a ground right piece
        waterq = random.randint(1,3) # Set a random vlue of how many water pieces are drawn next
        pwx = gr.rect.x+74 # Set platform water x position to the last ground right position +74
        for water in range(waterq):
            gw = GroundWater(pwx, window_height-57, 74,57, self) # Add awaer object
            self.waters.add(gw) # add to sprite groups
            self.game_sprites.add(gw)
            pwx = gw.rect.x+74
        # Add remaining sprites to sprite groups
        self.lastbottom = pwx
        self.groundends.add(gr)
        self.game_sprites.add(gr)
        self.platforms.add(gr)
        self.groundends.add(gl)
        self.game_sprites.add(gl)
        self.platforms.add(gl)

        self.run() # Ru the game it is now set up

    def run(self):
        ''' The loop to run the game\
        Set timers and call other methods for game play'''
        pygame.time.set_timer(pygame.USEREVENT+1,1500) # Timer for adding extra enemy levels
        #set game variables
        self.game_over = False
        self.playing = True
        while self.playing: #the game loop, run game methods
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

            if self.livecount<1: # Out of lives, go to game over screen
                self.game_over = True
                self.playing = False
                self.game_over_screen()


    def update(self):
        '''Update sprites in game for each frame\
        randomly add ground pieces as long as shorter than window width\
        Check for player collisions and object collisions'''
        self.projectiles.update(self)
        self.liveslost.update(self)
        self.player_group.update(self)
        self.game_sprites.update()
        #set background image to scroll
        if self.bgX < window_width *-1:
            self.bgX = window_width
        if self.bgX2 < window_width * -1:
            self.bgX2 = window_width

        #Draw ground items
        groundwidth = len(self.grounds)+ len(self.waters) # Total distance of ground pieces
        groundmax = (window_width//55)+4 # Dive screen by ground image width and add 4 more to get mximum pieces
        lastground = groundwidth*55 # Sets the last known x position
        self.lastbottom +=speed # Move the last bottom ground x over by speed
        if groundwidth <groundmax: # room for more
            gl = GroundLandLeft(self.lastbottom, window_height-74, 57,74, self)# star with adding a left ground piece
            pGquantity = random.randint(3,8)# Select how many middles are being drawn
            pgx = gl.rect.x+55 # set platfor ground x variavble to last piece x pos plus 55 (width of a piece)
            for plat in range(0,pGquantity):
                gm = GroundLandMiddle(pgx, gl.rect.y, 74,74, self) #Draw middle pieces
                self.platforms.add(gm) # Add to sprite groups
                self.grounds.add(gm)
                self.game_sprites.add(gm)
                pgx = gm.rect.x+74 # Add 74 to last platform ground x pos
            gr = GroundLandRight(pgx, gm.rect.y, 74,74, self)# load one ground right piece
            waterq = random.randint(1,5)# Add random water pieces count
            pwx = gr.rect.x+74# Add 74 to last platform ground x pos
            for water in range(2,5):
                gw = GroundWater(pwx, window_height-57, 74,57, self)# Load water pieces
                self.waters.add(gw)# add to sprite groups
                self.game_sprites.add(gw)
                pwx = gw.rect.x+74 # Add 74 to last platform ground x pos
            self.lastbottom = pwx+speed# add speed to x pos to move it over
            self.groundends.add(gr) # add remaining pieces to sprite groups
            self.game_sprites.add(gr)
            self.platforms.add(gr)
            self.groundends.add(gl)
            self.game_sprites.add(gl)
            self.platforms.add(gl)


        # ** Game hits and collisions **
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False) #Check if the player has hit a platform
        if hits:
            if pygame.sprite.spritecollide(self.player, self.groundends, False, pygame.sprite.collide_mask): # check pixel perfect for ends
                self.player.pos.y = hits[0].rect.top #set player y to hit top of platform
                self.player.vel.y =0 # Set player velocity to 0 (not falling or jumping)
                self.player.onground = True # On the ground
                self.player.jumping = False# not jumping
                self.player.acc.y =0 # Stop y acceleration

            elif pygame.sprite.spritecollide(self.player, self.grounds, False): #If on the middle ground do not do pixel perfect collision
                self.player.pos.y = hits[0].rect.top #set player y to hit top
                self.player.vel.y =0 # Set player velocity to 0 (not falling or jumping)
                self.player.onground = True # On the ground
                self.player.jumping = False# not jumping
                self.player.acc.y =0 # Stop y acceleration

            else: #collision with a platform, do pixel perfect to check if you are touching actual platform
                hits = pygame.sprite.spritecollide(self.player, self.platforms, False, pygame.sprite.collide_mask)
                for platform in hits:
                    if self.player.rect.top> platform.rect.y: # Check if the top of the player is above the platform
                        self.player.acc.y =0.2 #Leave moving
                        self.onground = False
                    elif self.player.rect.top+40< platform.rect.y+20: #Player has passedthe threshold for landing on a platform
                        self.player.pos.y = hits[0].rect.top #set player y to hit top
                        self.player.vel.y =0 # Set player velocity to 0 (not falling or jumping)
                        self.player.onground = True # On the ground
                        self.player.jumping = False# not jumping
                        self.player.acc.y =0 # Stop y acceleration
                    else:
                        self.player.acc.y =0.2 #Leave moving
                        self.player.jumping = True #leave jumping
                        self.onground = False
        else:
            self.player.onground = False #Otherwise leave falling/ gravity
            self.player.acc.y =0.2

        global score #Load in the global score
        #ENEMY HITS
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False) #Check if player has ht an enemy
        if hits:
            if pygame.sprite.spritecollide(self.player, self.enemies, True, pygame.sprite.collide_mask):# check pixel perfect
                score -=10 #Lose score points
                self.livecount-=1# lose 1 life
                self.lives.update(self) # Update life mushrooms
                effect = pygame.mixer.Sound('sounds/hit.ogg') #load sound effect
                effect.play() # play sound effect
                self.lifelost = LivesLost(self.player.pos.x, self.player.pos.y,self) #Launch lost life mushroom to float up the screen
                self.liveslost.add(self.lifelost) # add lost life mushroom to sprite group
                pygame.display.update()

        hits = pygame.sprite.spritecollide(self.player, self.waters, False,pygame.sprite.collide_mask) #Check if player hits the water
        if hits:
            self.livecount-=1 #Lose a life
            self.lives.update(self) #Update life mushrooms
            effect = pygame.mixer.Sound('sounds/hit.ogg') #Load sound effect
            effect.play() #Play sound
            self.lifelost = LivesLost(self.player.pos.x, self.player.pos.y-120,self) #Draw a lost life mushroom just above player
            self.liveslost.add(self.lifelost) #add to lives lost
            self.lifelost.update(self)# add to lost lives group
            self.liveslost.draw(self.window)#draw to window
            pygame.display.update()#update display
            pygame.time.wait(1000)# pause the screen to show the loss of life
            self.lastbottom = 0 #Reset last ground bottom piece to 0 for game redraw
            self.new()# redraw game with player falling in again

        bonusscore = pygame.sprite.spritecollide(self.player, self.bonuses, False) #Checkif player hit bonus points
        if bonusscore:
            if pygame.sprite.spritecollide(self.player, self.bonuses, True, pygame.sprite.collide_mask):#check pixel perfect
                effect = pygame.mixer.Sound('sounds/bonus.wav') #Load sound
                effect.play() #Play sound
                score +=10 #score for bonus
                pygame.display.update()

        extralife = pygame.sprite.spritecollide(self.player, self.bonuslife, True) #Check if player hit extra life mushrooms
        if extralife:
            effect = pygame.mixer.Sound('sounds/bonus.wav') #Load sound
            effect.play() #Play sound
            if self.livecount<10: #Check if lifecount is at 10 already being the max
                self.livecount+=1 #If not add one life
                self.lives.update(self) # add one life to lifecount sprites
                self.draw_lives() # Draw lives top right hand corner
                pygame.display.update()

        hits = pygame.sprite.groupcollide(self.projectiles, self.enemies, True, True, pygame.sprite.collide_mask)# Check if a throwm mushroom hits a zombie
        if hits:
            effect = pygame.mixer.Sound('sounds/bonus.wav')# load a sound
            effect.play()# play the sound
            score +=5 #score for bonus
            pygame.display.update()


    def events(self):
        '''Check for eventsin the game loop\
        If the game is quit, check if the game was a high score\
        Player movement is controlled by changing player.dir\
        Throw mushroom projectiles\
        Load random platform every amount of time in the game\
        spawn enemies, bonus mushroom, and life mushrooms on platforms'''

        for event in pygame.event.get(): #Check events
            if event.type == pygame.QUIT:  # don't quit uness close is pressed
                if self.playing:
                    self.playing = False # finished playing game
                self.running = False
                # Check if this game bet the high score and amend if needed
                if score > self.highscore:
                    new_high_Score(score)# Load high score to file
                    self.highscore = score

            #Change player directions
            if event.type == pygame.KEYUP: #key released, allows sprite to turn around
              if event.key == pygame.K_LEFT: #Was left, now not so  must be right
                  self.player.dir = 1 #change direction to flip image
              if event.key == pygame.K_SPACE and len(self.projectiles)<3:# space was pressed, and you don't have 3 projectiles on screen
                  self.projectile = Projectile(self.player.pos.x, self.player.pos.y-80, self) #Load a projectile mushroom sprite
                  self.projectiles.add(self.projectile) #add to sprite group
                  effect = pygame.mixer.Sound('sounds/project.wav')# load sound effect
                  effect.play() #play sound when throwing mushroom

            if event.type== pygame.USEREVENT+1: #Time has passed to level up th enemy spawning
                self.enemy_level+=1

            #PLATFORM DRAWING
            if event.type == pygame.USEREVENT+2 and len(self.platforms)-len(self.grounds) < 30:# Ther are no more than 30 platform pieces
                width = random.randrange(50, 200) #Length of platform in 50 px pieces
                pl = Platform(window_width, random.randrange(80,(window_height-80)), 55,40, self) # Load left platform piece
                # Add a random number of middle pieces to a platform
                pMquantity = random.randint(1,5)# Select how many middles are being drawn
                pmx = pl.rect.x+55 #Set new platform middle x coordinate for next piece
                for plat in range(0,pMquantity):
                    pm = PlatformM(pmx, pl.rect.y, 55,40, self) #Draw a platform middle piece
                    self.platforms.add(pm) # Add to groups
                    self.game_sprites.add(pm)
                    pmx = pm.rect.x+55 #Set new x coordinate for next piece
                pr = PlatformR(pmx, pl.rect.y, 55,40,self) # Out of the loop, add right platform end piece

                # Add platform left & right pieces to sprite groups
                self.platforms.add(pl)
                self.platforms.add(pr)
                self.game_sprites.add(pl)
                self.game_sprites.add(pr)

                #Add random enemy/ mushroom/ life to right end piece of a platform
                enemyrandom = random.randint(0,20)
                bonusrandom = random.randint(0,20)
                livesrandom = random.randint(0,25)# Add a bonus life 2/ 25 times
                if enemyrandom>=18:
                    enemypath = pr.rect.right -pl.rect.left # Set enemy path to be platform rightx x pos minus left platform x pos to get the length
                    enemy = Enemy(pr.rect.x, pr.rect.y-pr.rect.height*2, enemypath, self) #Load enemy sprite with platform length
                    self.enemies.add(enemy) # add to groups
                    self.game_sprites.add(enemy)
                elif bonusrandom>12:
                    bonuspath = pr.rect.right -pl.rect.left# Set bonus path to be platform rightx x pos minus left platform x pos to get the length
                    bonus = Bonus(pr.rect.x, pr.rect.y-pr.rect.height, bonuspath, self)
                    self.bonuses.add(bonus)
                    self.game_sprites.add(bonus)
                elif livesrandom>22 and len(self.bonuslife)<10:
                    lifepath = pr.rect.right -pl.rect.left# Set Lives path to be platform rightx x pos minus left platform x pos to get the length
                    life = Extra_Life(pr.rect.x, pr.rect.y-20, lifepath, self) # Add life to platform
                    self.bonuslife.add(life)# add to sprite groups
                    self.game_sprites.add(life)
                else:
                    enemyrandom = int(self.enemy_level)*random.randint(0,4)# add enemies based on level
                    if enemyrandom>=int(self.enemy_level)*2: # Set enemy path to be platform rightx x pos minus left platform x pos to get the length
                        enemypath = pr.rect.right -pl.rect.left
                        enemy = Enemy(pr.rect.x, pr.rect.y-pr.rect.height*2, enemypath, self) #Load enemy sprite with platform length
                        self.enemies.add(enemy)# add to groups
                        self.game_sprites.add(enemy)


    def draw(self):
        ''' The grame draw method for drawing all sprites and text to the window\
        for every update of the screen'''
        self.lastbottom +=self.speed #reset last bottom piece x location
        #Draw background image
        self.bgX += self.speed #Set background images to new x positions
        self.bgX2 += self.speed
        self.window.blit(self.bg,(self.bgX,0)) #Draw background images
        self.window.blit(self.bg,(self.bgX2,0))
        #Draw sprite groups
        self.platforms.draw(self.window)
        self.grounds.draw(self.window)
        self.lives.draw(self.window)
        self.game_sprites.draw(self.window)
        self.bonuses.draw(self.window)
        self.enemies.draw(self.window)
        self.player_group.draw(self.window)
        self.projectiles.draw(self.window)
        self.liveslost.draw(self.window)
        #Add scoreboards
        font = pygame.font.SysFont('comicsans', 30, True)
        text = font.render('Score: '+ str(score),1 ,(0,0,0))
        self.window.blit(text, (window_width-150, 10))
        font = pygame.font.SysFont('arial', 20, True)
        text = font.render('High Score: '+ str(self.highscore),1 ,(0,0,0))
        self.window.blit(text, (window_width-180, 80))
        pygame.display.flip() #Update game screen

    def start_screen(self):
        '''Start screen for before the game starts'''
        # game splash/start screen
        pygame.mixer.music.load('sounds/intro.mp3') #Load music
        pygame.mixer.music.play(-1) #Play music on a loop
        pygame.mixer.music.set_volume(1)

        #Load background image for start screen
        self.bg = pygame.image.load('images/bg.png').convert()
        self.bg = pygame.transform.scale(self.bg, (window_width,window_height))
        self.window.blit(self.bg, (0,0) )

        #Text on start screen
        pygame.font.init()
        high_score() # Get high score
        textload (game_title, 2,3, 0,102,0,51,50, 'comicsans', self)
        textload ("Use arrows to move, up to Jump, space to launch projectile", 2,2,25 ,0,102,102,40, 'comicsans', self)
        textload ("Avoid zombies, bonus points for mushrooms", 2,2,60 ,0,102,102,40, 'comicsans', self)
        textload ("Press any key to start", 2,2,150 ,0,0,0,25, 'arial', self)
        textload ("A game by Angie Hollingworth", 2,2,190 ,0,0,0,15, 'arial', self)
        textload ("CURRENT HIGH SCORE {}! Can you beat it?".format(self.highscore), 2,2,220 ,0,102,102,25, 'arial', self)
        #Load window
        pygame.display.flip()
        self.key_press_wait("start") #Wait for user to press a key to start
        pygame.mixer.music.fadeout(500)# fade out music before main music starts

    def game_over_screen(self):
        '''Game over screen, shows message and gives you the option to play agian'''
        #Game over start_screen
        if self.game_over: #If game is over, run through
            self.game_over=False
            pygame.mixer.music.load('sounds/intro.mp3') #Load music
            pygame.mixer.music.play(-1) #Play music on a loop
            pygame.mixer.music.set_volume(1)

            #Load background image for start screen
            self.bg = pygame.image.load('images/bg.png').convert() #Load background image
            self.bg = pygame.transform.scale(self.bg, (window_width,window_height))
            self.window.blit(self.bg, (0,0) ) #Set to transperant

            #Text on game over screen
            pygame.font.init()
            textload (game_title, 2,3, 0,102,0,51,50, 'comicsans', self)
            textload ("GAME OVER!!", 2,2,25 ,0,102,102,40, 'comicsans', self)
            textload ("Press any key to start again", 2,2,150 ,0,0,0,25, 'comicsans', self)

            if score > self.highscore: #Check if your game beat the high score
                new_high_Score(score) #if so, update score & print message
                self.highscore = score
                textload ("CONGRATULATIONS, New High Score {}!!!".format(self.highscore), 2,3,50 ,0,102,102,40, 'arial', self)
            #Load window
            pygame.display.flip()
            self.key_press_wait("go") #Wait for user input quit/start again using method

    def draw_lives(self):
        '''Spawn lives (mushroom) class objects in top right hand corner as lives'''
        lifex = window_width-50 #Set staring position to be 50 leff than the screen width
        for life in range(0,self.livecount):
            self.life = Lives(lifex, 50, self)
            self.lives.add(self.life)
            lifex-=40
        pygame.display.update() # Display with lives loaded


    def key_press_wait(self,screen): #Used to pause the start screen
        '''Wait whiles the screen is paused on game over screen and start screen'''
        paused = True
        while paused:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #Quit Pygame, do not launch game
                    paused = False
                    self.running = False
                    pygame.quit
                    quit()

                if screen=="go": #On the game over screen
                    if event.type == pygame.KEYUP: # If a key is pressed to play again
                        paused = False #Reset game
                        pygame.mixer.music.fadeout(500) #turn down music
                        pygame.time.wait(1500) #pause a moment
                        self.livecount=5 #reset and start again
                        # self.running = True
                        self.playing = True
                        self.game_over = False
                        self.enemy_level=1
                        global score
                        score = 0
                        self.new() #Load a new game
                else:
                    if event.type == pygame.KEYUP: #Start screen, new game
                        paused = False

g= Game() #Create a game instance
g.start_screen() #Load start splash screen

while g.running:
    g.new() #start a new game

    g.game_over_screen() #display game over/ restart screen

pygame.quit() #Quite pygame
