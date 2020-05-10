# sprite calsses
# Created by Angie Hollingworth 
# HIT137 2019

# This file is the sprite management file for the game associated with it.
# all sprites are generated and updated with this file.

import pygame
import random
from settings import *

vec = pygame.math.Vector2 # x & y changer - 2 dimensions for gravity

class Player(pygame.sprite.Sprite):
    '''This is a class for generating all the attributes for the main player.\
    Any changes to the sprite images, as well as the movement of them are done within this class.\
    There are 4 methods for this class.\
    init: for initiating the sprites\
    load_images: for loading all the sprite load_images\
    update: for making any changes to the sprites, position, walk count, speed etc.\
    animate: putting it all together to give the illusion of the sprite moving by rotating through the images'''

    def __init__(self, game):
        '''Initiate the player sprite, pass in the game.\
        All counts are set to defaults, screen limits are set to keep the sprite on screen'''
        pygame.sprite.Sprite.__init__(self) #Initiate as a sprite
        self.game = game
        self.walkcount = 0 #Set walk count to 0 for step 1, image 1
        self.last_update = 0 #time elapsed since last update
        self.load_images() #Call the load images method below to add sprite images
        self.image = self.jumping_frames[0] #Initially player is falling
        self.rect = self.image.get_rect() #get image as a rectangle object
        self.rect.center = (window_width/4, -1) #Inital position for the sprite. LHS just outside the frame up top
        self.pos = vec(window_width/4, -1) #Starting fall position
        self.vel = vec(0,0) # the amount that the player is falling
        self.acc = vec(0,0.2) # how faast teh player is falling
        self.onground = False # true for jumping/ falling. initially the player drops in
        self.jumping = True #Player is initially falling so the jump is on to load non-walking images
        self.maxleft = 15 #Limit playing area to onscreen
        self.maxright = window_width-15 #Limit playing area to onscreen
        self.dir = 1 # Player  will be in the direction of right
        self.mask = pygame.mask.from_surface(self.image) #For pixel perfect collision

    def load_images(self):
        '''Sprite images for player character.\
        Images are on two sprite sheets, walking & jumping.\
        Sprite sheets are loaded through the game loop in the new() method.\
        All images are .png files with a transperant background.\
        Images are passed in with their x position, y position, width & height values'''
        self.walking_frames = [self.game.spritesheetwalk.get_image(0, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(74, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(148, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(222, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(296, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(370, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(444, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(518, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(592, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(666, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(740, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(814, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(888, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(962, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(1036, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(1110, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(1184, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(1258, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(1332, 0, 74, 81),
                                self.game.spritesheetwalk.get_image(1406, 0, 74, 81)]
        for frame in self.walking_frames:
            frame.set_colorkey((0,0,0)) # Set images to have a tranperant background

        self.jumping_frames = [self.game.spritesheetjump.get_image(0, 0, 74, 81),
                                self.game.spritesheetjump.get_image(74, 0, 74, 81),
                                self.game.spritesheetjump.get_image(148, 0, 74, 81),
                                self.game.spritesheetjump.get_image(0, 81, 74, 81),
                                self.game.spritesheetjump.get_image(74, 81, 74, 81),
                                self.game.spritesheetjump.get_image(148, 81, 74, 81),
                                self.game.spritesheetjump.get_image(0, 162, 74, 81),
                                self.game.spritesheetjump.get_image(74, 162, 74, 81),
                                self.game.spritesheetjump.get_image(148, 162, 74, 81),
                                self.game.spritesheetjump.get_image(0, 243, 74, 81),
                                self.game.spritesheetjump.get_image(74, 243, 74, 81),
                                self.game.spritesheetjump.get_image(148, 243, 74, 81),
                                self.game.spritesheetjump.get_image(0, 324, 74, 81),
                                self.game.spritesheetjump.get_image(74, 324, 74, 81),
                                self.game.spritesheetjump.get_image(148, 324, 74, 81),
                                self.game.spritesheetjump.get_image(0, 405, 74, 81),
                                self.game.spritesheetjump.get_image(74, 405, 74, 81),
                                self.game.spritesheetjump.get_image(148, 405, 74, 81),
                                self.game.spritesheetjump.get_image(0, 486, 74, 81),
                                self.game.spritesheetjump.get_image(74, 486, 74, 81),
                                self.game.spritesheetjump.get_image(148, 486, 74, 81),
                                self.game.spritesheetjump.get_image(0, 567, 74, 81),
                                self.game.spritesheetjump.get_image(74, 567, 74, 81),
                                self.game.spritesheetjump.get_image(148, 567, 74, 81),
                                self.game.spritesheetjump.get_image(0, 648, 74, 81),
                                self.game.spritesheetjump.get_image(74, 648, 74, 81),
                                self.game.spritesheetjump.get_image(148, 648, 74, 81),
                                self.game.spritesheetjump.get_image(0, 729, 74, 81),
                                self.game.spritesheetjump.get_image(74, 729, 74, 81),
                                self.game.spritesheetjump.get_image(148, 729, 74, 81)]
        for frame in self.jumping_frames:
            frame.set_colorkey((0,0,0)) # Set images to have a tranperant background

    def update(self, game):
        '''Update player.\
        Call the game, update the walkcount for Images.\
        Check if the player is moving and update x, y and gravity (Vel & Acc) where needed.'''
        self.game = game # The game for the sprite
        self.walkcount+=1 #Add one move to the walkcount for image rotation

        keys = pygame.key.get_pressed() #Check which way player is moving
        if keys[pygame.K_LEFT]:
            if self.pos.x + -3.5> self.maxleft: #Check if moving will move the player off screen
                self.dir = -1 #Set direction to left for flipping images
                self.pos.x += -3.5 # move player left by changing their pos.x position
            else:
                self.dir = 1 # set direction to right for unflippped images
        if keys[pygame.K_RIGHT]:
            if self.pos.x + 1< self.maxright: #check if the move willmove the player off screen
                self.pos.x += 1 # move player right by changing their pos.x position
        if keys[pygame.K_UP]: #Jumping
            if self.onground: #Only jump if on the ground, no mid air jumping
                self.jumping = True #Set jumping to tru to have jump images displayed
                effect = pygame.mixer.Sound('sounds/jump.wav') #play jump noise
                effect.play()
                self.vel.y = -10 #Set velocity to a negative value to "jump"
                self.acc.y = 0.2# how fast the player is moving
                self.onground = False # no longer on the ground

        # motion
        self.vel += self.acc #How far the sprite is moving and by how much
        self.pos += self.vel + 0.2 * self.acc # incrementally reduce the negative velocity until it is positive forcing the player to move down again.

        self.animate(self.rect.x, self.rect.y,self.dir)# load the sprite image for the frame
        if self.rect.y<-10: # Keep sprite on screen, do not allow to jump above the frame
            self.vel.y = 2 #New line to stop off screen
        if self.rect.y> window_height: # check if sprite falls off the bottom of the screen into the water
            self.kill() #Remove the sprite, a new one will need to be loaded
        self.rect.midbottom = self.pos #After all moves have been made, establish new position for the bottom of the sprite

    def animate(self,x,y,dir):
        '''Animate method is used to call the correct image for the players current action.\
        The player has two "moves", jumping or walking and also left and right.'''
        now = pygame.time.get_ticks() # get the current game time
        if now - self.last_update > 250:  # check when the image was last changed
            self.last_update = now # 250ms has has passed, set the timer to now
            if self.jumping: # Player is jumping, load jumping psrites
                self.walkcount = (self.walkcount + 1) % len(self.jumping_frames) # add 1 to the jump count, ensure it doesn't pass the number of images
                bottom = self.rect.bottom # reset the bottom of the sprite with the new image
                self.image = self.jumping_frames[self.walkcount] #select the next image in teh list
            else: #Walking
                self.walkcount = (self.walkcount + 1) % len(self.walking_frames) # add 1 to the walk count, ensure it doesn't pass the number of images
                bottom = self.rect.bottom # reset the bottom of the sprite with the new image
                self.image = self.walking_frames[self.walkcount] #select the next image in teh list
            if dir <0:# if direction is negative, then the left facing image needs to be displayed
                self.image = pygame.transform.flip(self.image,True,False) # flip the image on the verticle axis for a left image
            self.rect = self.image.get_rect() #Set a new rect
            self.rect.bottom = bottom # reset the bottom of the sprite with the new image


class Platform(pygame.sprite.Sprite): #Left platform image & piece
    '''Class for a left end platform piece.\
    Piece has two methods, an init for the initial position, speed etc,\
    and an update to move the platform with the screen'''

    def __init__(self, x, y, w, h, game):
        '''Initialise a left platform piece.\
        Select the left image piece, set surface area and x, y locations'''
        pygame.sprite.Sprite.__init__(self)# call the sprite functionality to the object
        self.game = game #Load the game
        self.image = pygame.image.load('images/leftpt.png').convert()# set the sprite to be a left end platform oiece
        self.image = pygame.transform.scale(self.image, (55,40))# resize image
        self.image.set_colorkey((0,0,0))# set background to transperant
        self.rect = self.image.get_rect()# get object rect
        self.rect.x = x #Set object x position using the image box
        self.rect.y = y #Set object y position using the image box
        self.topleft = self.rect.topleft #Find the top left of the image
        self.topright = self.rect.topright #Find the top right of the image
        self.midtop = self.rect.midtop #Find the top middle of the image
        self.speed = game.speed #set the platform speed to be the game speed
        self.mask = pygame.mask.from_surface(self.image) #For pixel perfect collision

    def update(self):
        '''Update platform piece.\
        Set new coordinates, and remove from sprite group if off screen'''
        if self.rect.x <1: #Check how close to the edge of the screen the platform piece is
            self.speed = -3 #Stop platforms slowing down after they pass 0 on the x axis
            self.rect.x = self.rect.x +speed*2# speed up the movement to keep it moving off screen
        else:
            self.rect.x = self.rect.x +speed #Move with the "window"
        if self.rect.x+ self.rect.width <5: #Check if the piece is off the screen
            self.kill()# remove from the sprite group

class PlatformR(pygame.sprite.Sprite): # right platform image & piece
    '''Class for a right end platform piece.\
    Piece has two methods, an init for the initial position, speed etc,\
    and an update to move the platform with the screen'''

    def __init__(self, x, y, w, h, game):
        '''Initialise a right platform piece.\
        Select the right image piece, set surface area and x, y locations'''
        pygame.sprite.Sprite.__init__(self) # call the sprite functionality to the object
        self.game = game #Load the game
        self.image = pygame.image.load('images/rtplt.png').convert() # set the sprite to be a right end platform oiece
        self.image = pygame.transform.scale(self.image, (55,40)) # resize image
        self.image.set_colorkey((0,0,0)) # set background to transperant
        self.rect = self.image.get_rect() # get object rect
        self.rect.x = x #Set object x position using the image box
        self.rect.y = y #Set object y position using the image box
        self.topleft = self.rect.topleft #Find the top left of the image
        self.topright = self.rect.topright #Find the top right of the image
        self.midtop = self.rect.midtop #Find the top middle of the image
        self.speed = game.speed #set the platform speed to be the game speed
        self.mask = pygame.mask.from_surface(self.image) #For pixel perfect collision

    def update(self):
        '''Update platform piece.\
        Set new coordinates, and remove from sprite group if off screen'''
        if self.rect.x <1:  #Check how close to the edge of the screen the platform piece is
            self.speed = -3 #Stop platforms slowing down after they pass 0 on the x axis
            self.rect.x = self.rect.x +speed*2 # speed up the movement to keep it moving off screen
        else:
            self.rect.x = self.rect.x +speed #Move with the "window"
        if self.rect.x+ self.rect.width <5: #Check if the piece is off the screen
            self.kill() # remove from the sprite group

class PlatformM(pygame.sprite.Sprite): #midle platform image & piece
    '''Class for a middle platform piece.\
    Piece has two methods, an init for the initial position, speed etc,\
    and an update to move the platform with the screen'''

    def __init__(self, x, y, w, h, game):
        '''Initialise a middle platform piece.\
        Chose the middle image piece, set surface area and x, y locations'''
        pygame.sprite.Sprite.__init__(self) # call the sprite functionality to the object
        self.game = game #Load the game
        self.image = pygame.image.load('images/midplt.png').convert() # set the sprite to be a middle platform oiece
        self.image = pygame.transform.scale(self.image, (55,40)) # resize image
        self.image.set_colorkey((0,0,0)) # set background to transperant
        self.rect = self.image.get_rect() # get object rect
        self.rect.x = x #Set object x position using the image box
        self.rect.y = y #Set object y position using the image box
        self.topleft = self.rect.topleft #Find the top left of the image
        self.topright = self.rect.topright #Find the top right of the image
        self.midtop = self.rect.midtop #Find the top middle of the image
        self.speed = game.speed#set the platform speed to be the game speed
        self.mask = pygame.mask.from_surface(self.image) #For pixel perfect collision

    def update(self):
        '''Update platform piece.\
        Set new coordinates, and remove from sprite group if off screen'''
        if self.rect.x <1:  #Check how close to the edge of the screen the platform piece is
            self.speed = -3 #Stop platforms slowing down after they pass 0 on the x axis
            self.rect.x = self.rect.x +speed*2 # speed up the movement to keep it moving off screen
        else:
            self.rect.x = self.rect.x +speed #Move with the "window"
        if self.rect.x+ self.rect.width <5: #Check if the piece is off the screen
            self.kill() # remove from the sprite group

class GroundLandLeft(pygame.sprite.Sprite): #Left ground piece and image
    '''Class for a left ground piece.\
    Piece has two methods, an init for the initial position, speed etc,\
    and an update to move the platform with the screen'''

    def __init__(self, x, y, w, h, game):
        '''Initialise a left ground piece.\
        Select the left image piece, set surface area and x, y locations'''
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image  = self.game.spritesheetground.get_image(0, 0, 74, 74)  # set the sprite to be a left end ground oiece
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x #Set object x position using the image box
        self.rect.y = y #Set object y position using the image box
        self.topleft = self.rect.topleft
        self.topright = self.rect.topright
        self.speed = game.speed #set the platform speed to be the game speed
        self.mask = pygame.mask.from_surface(self.image) #For pixel perfect collision

    def update(self):
        '''Update platform piece.\
        Set new coordinates, and remove from sprite group if off screen'''
        if self.rect.x <1:  #Check how close to the edge of the screen the platform piece is
            self.speed = -3 #Stop platforms slowing down after they pass 0 on the x axis
            self.rect.x = self.rect.x +speed*2 # speed up the movement to keep it moving off screen
        else:
            self.rect.x = self.rect.x +speed #Move with the "window"
        if self.rect.x+ self.rect.width <10:#Check if the piece is off the screen
            self.kill() # remove from the sprite group

class GroundLandMiddle(pygame.sprite.Sprite): #Middle ground piece and image
    '''Class for a middle ground piece.\
    Piece has two methods, an init for the initial position, speed etc,\
    and an update to move the platform with the screen'''

    def __init__(self, x, y, w, h, game):
        '''Initialise a middle ground piece.\
        Select the middle image piece, set surface area and x, y locations'''
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image  = self.game.spritesheetground.get_image(0, 74, 74, 74)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x #Set object x position using the image box
        self.rect.y = y #Set object y position using the image box
        self.topleft = self.rect.topleft
        self.topright = self.rect.topright
        self.speed = game.speed
        self.mask = pygame.mask.from_surface(self.image) #For pixel perfect collision

    def update(self):
        '''Update platform piece.\
        Set new coordinates, and remove from sprite group if off screen'''
        if self.rect.x <1:
            self.rect.x = self.rect.x +speed*2
        else:
            self.rect.x = self.rect.x +speed #Move with the "window"
        if self.rect.x+ self.rect.width <5:
            self.kill()

class GroundLandRight(pygame.sprite.Sprite): #Right ground piece and image
    '''Class for a right ground piece.\
    Piece has two methods, an init for the initial position, speed etc,\
    and an update to move the platform with the screen'''

    def __init__(self, x, y, w, h, game):
        '''Initialise a left ground piece.\
        Select the left image piece, set surface area and x, y locations'''
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image  = self.game.spritesheetground.get_image(0, 148, 74, 74)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x #Set object x position using the image box
        self.rect.y = y #Set object y position using the image box
        self.topleft = self.rect.topleft
        self.topright = self.rect.topright
        self.speed = game.speed
        self.mask = pygame.mask.from_surface(self.image) #For pixel perfect collision

    def update(self):
        '''Update platform piece.\
        Set new coordinates, and remove from sprite group if off screen'''
        if self.rect.x <1:
            self.rect.x = self.rect.x +speed*2
        else:
            self.rect.x = self.rect.x +speed #Move with the "window"
        if self.rect.x+ self.rect.width <10:
            self.kill()

class GroundWater(pygame.sprite.Sprite): #Water ground piece and image
    '''Class for a water ground piece.\
    Piece has two methods, an init for the initial position, speed etc,\
    and an update to move the platform with the screen'''

    def __init__(self, x, y, w, h, game):
        '''Initialise a left ground piece.\
        Select the left image piece, set surface area and x, y locations'''
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image  = self.game.spritesheetground.get_image(0, 222, 74, 74) #Load the ground water image
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x #Set object x position using the image box
        self.rect.y = y #Set object y position using the image box
        self.topleft = self.rect.topleft
        self.topright = self.rect.topright
        self.midtop = self.rect.midtop
        self.speed = game.speed
        self.mask = pygame.mask.from_surface(self.image) #For pixel perfect collision

    def update(self):
        '''Update platform piece.\
        Set new coordinates, and remove from sprite group if off screen'''
        if self.rect.x <1:
            self.rect.x = self.rect.x +self.speed*2
        else:
            self.rect.x = self.rect.x +self.speed #Move with the "window"
        if self.rect.x+ self.rect.width <1:
            self.kill()

class Bonus(pygame.sprite.Sprite):# mushroom for bonus points
    '''This is a class for generating all the attributes for the bonus points mushroom.\
    There are 2 methods for this class.\
    init: for initiating the sprites& update: for making any changes to the position etc.'''

    def __init__(self, x, y, pathlength,game):
        '''Initialise a bonus points mushroom.\
        Select the mushroom image, set surface area and x, y locations'''
        pygame.sprite.Sprite.__init__(self) #Initiate as a sprite
        self.game = game
        self.image = pygame.image.load('images/bonus10.png').convert() #load image
        self.image.set_colorkey((0,0,0)) # Set background tp transperant
        self.rect = self.image.get_rect() #get image as a rectangle object
        self.rect.x = x #Set object x position using the image box
        self.rect.y = y #Set object y position using the image box
        self.speed = game.speed # Set object speed
        self.dir = 1# Set initial direction to rigth
        self.pathlength = pathlength-50 # path length is passed in as the length of path the object is spawned on. removing 50 stops it falling off the path object
        self.path = 0 # How far along the path the mushroom has moved
        self.counter = 0# for counting distance & speed
        self.mask = pygame.mask.from_surface(self.image) #For pixel perfect collision

    def update(self):
        '''Update mushroom. \
        Set new coordinates, and ensure sprite is not going past it's platform it was spawned on'''
        self.counter += (speed*self.dir) # Set the move size (left & right are different as all obejcts are moving left)
        if self.path == self.pathlength-2: #object has hit the end of the path, turn
            self.path = 0 # Reset path count
            self.dir *=-1# change directions
            self.counter += (speed*self.dir) +-1 # updating the length of the distance & speed travelling
        elif self.dir<1 and self.path >=(self.pathlength//2):# moving right , half the length of the platorm
            self.counter = 0# reset counter
            self.path = 0# current travelled path is 0
            self.dir *=-1# change directions
        else:
            self.path+=1 #keep moving no turn
        self.rect.x += (speed*self.dir) +-1 # x is  in a fixed coordinate to "go right"
        if self.rect.right <0 or self.rect.y> window_height+20:# remove sprite once it has left the screen
            self.kill()

class Enemy(pygame.sprite.Sprite):#Zombies
    '''This is a class for generating all the attributes for the Enemy/ zombie character.\
    Any changes to the sprite images, as well as the movement of them are done within this class.\
    There are 4 methods for this class.\
    init: for initiating the sprites\
    load_images: for loading all the sprite load_images\
    update: for making any changes to the sprites, position, walk count, speed etc.\
    animate: putting it all together to give the illusion of the sprite moving by rotating through the images'''

    def __init__(self, x, y, pathlength,game):
        '''Initialise an enemy.\
        Select the initial walking image, set surface area and x, y locations and \
        distance of the platform in which the sprite was initiated'''
        pygame.sprite.Sprite.__init__(self) #Initiate as a sprite
        self.game = game
        self.walkcount = 0# set count to zero for no steps taken as of yet
        self.last_update = 0# no updates have happened
        self.load_images()# call the method of this object for loading the spritesheet
        self.image = self.walking_frames[0]# select the first image on the spritesheet
        self.rect = self.image.get_rect() #get image as a rectangle object
        self.rect.x = x #Set object x position using the image box
        self.rect.y = y #Set object y position using the image box
        self.speed = game.speed# set enemy speed as game speed
        self.dir = 1# set direction to the right
        self.pathlength = pathlength-50 # path length is passed in as the length of path the object is spawned on. removing 50 stops it falling off the path object
        self.path = 0 # How far along the path the mushroom has moved
        self.counter = 0 # for counting distance & speed
        self.mask = pygame.mask.from_surface(self.image) #pixel perfect collsion

    def load_images(self):
        '''Sprite images for enemy character.\
        Images are on a spritesheet for walking.\
        Sprite sheets are loaded through the game loop in the new() method.\
        All images are .png files with a transperant background.\
        Images are passed in with their x position, y position, width & height values'''
        self.walking_frames = [self.game.enemyspritesheet.get_image(0, 0, 73, 81),
                                self.game.enemyspritesheet.get_image(73, 0, 73, 81),
                                self.game.enemyspritesheet.get_image(146, 0, 73, 81),
                                self.game.enemyspritesheet.get_image(219, 0, 73, 81),
                                self.game.enemyspritesheet.get_image(292, 0, 73, 81),
                                self.game.enemyspritesheet.get_image(365, 0, 73, 81),
                                self.game.enemyspritesheet.get_image(438, 0, 73, 81),
                                self.game.enemyspritesheet.get_image(511, 0, 73, 81),
                                self.game.enemyspritesheet.get_image(584, 0, 73, 81),
                                self.game.enemyspritesheet.get_image(657, 0, 73, 81)]
        for frame in self.walking_frames:
            frame.set_colorkey((0,0,0)) # Set background to transperant

    def update(self):
        '''Update enemy. \
        Set new coordinates, and ensure sprite is not going past it's platform it was spawned on'''
        self.walkcount+=1 # Add one to the walk count for image selection
        self.counter += (self.speed*self.dir) # Set the move size (left & right are different as all obejcts are moving left)
        if self.path == self.pathlength-2: #object has hit the end of the path, turn
            self.path = 0 # Reset path count
            self.dir *=-1 # change directions
            self.counter += (self.speed*self.dir) +-1 # updating the length of the distance & speed travelling
        elif self.dir<1 and self.path >=(self.pathlength//2): # moving right , half the length of the platorm
            self.counter = 0 # reset counter
            self.path = 0 # current travelled path is 0
            self.dir *=-1 # change directions
        else:
            self.path+=1 #keep moving no turn

        self.rect.x += (self.speed*self.dir) +-1 # x is  in a fixed coordinate to "go right"
        self.animate(self.rect.x, self.rect.y,self.dir)# change to next walking image
        if self.rect.right <0 or self.rect.y> window_height+20: # remove sprite once it has left the screen
            self.kill()

    def animate(self,x,y,dir):
        '''Animate method is used to call the correct image for the enemy current step.'''
        now = pygame.time.get_ticks() # get the current game time
        if now - self.last_update > 250:  # check when the image was last changed
            self.last_update = now# 250ms has has passed, set the timer to now
            self.walkcount = (self.walkcount + 1) % len(self.walking_frames) # add 1 to the walk count, ensure it doesn't pass the number of images
            self.image = self.walking_frames[self.walkcount]# Select next image
            if dir >0:# moving left
                self.image = pygame.transform.flip(self.image,True,False)# flip the image to be facing left
            self.rect = self.image.get_rect()# reset rect
            self.rect.x = x #Set object x position using the image box
            self.rect.y = y #Set object y position using the image box

class Lives(pygame.sprite.Sprite):# Show mushrrom lives top right hand corner
    '''This is a class for generating the little mushroom life count in \
    the top right hand corner.'''

    def __init__(self, x, y, game):
        '''Initialise a life mushroom.Select the image, set surface area and x, y locations'''
        pygame.sprite.Sprite.__init__(self) #Initiate as a sprite
        self.game = game
        self.image = pygame.image.load('images/lives.png').convert() #lives image
        self.image.set_colorkey((0,0,0)) # show background as transperant
        self.rect = self.image.get_rect() #get image as a rectangle object
        self.rect.x = x #Set object x position using the image box
        self.rect.y = y #Set object y position using the image box

    def update(self, game):
        '''Update mushroom. \
        Remove mushroom from the list when a life is lost'''
        self.game = game
        if len(game.lives)>game.livecount: # If there are more images in the list than lives
            self.kill() #remove the image

class LivesLost(pygame.sprite.Sprite):
    '''This is a class for generating the little mushroom that floats up\
    when a life is lost.'''

    def __init__(self, x, y, game):
        '''Initialise a life mushroom.Select the image, set surface area and x, y locations'''
        pygame.sprite.Sprite.__init__(self) #Initiate as a sprite
        self.game = game
        self.image = pygame.image.load('images/lives.png').convert() #lives image
        self.image.set_colorkey((0,0,0))  #show background as transperant
        self.rect = self.image.get_rect() #get image as a rectangle object
        self.rect.x = x #Set object x position using the image box
        self.rect.y = y #Set object y position using the image box

    def update(self, game):
        '''Update mushroom. \
        Remove mushroom from the list when reaches above the window height'''
        self.game = game
        self.rect.y-=2 # reduce y count to move upwards with each frame
        if self.rect.y<0:# check if it has left the screen
            self.kill() #remove from the group


class Projectile(pygame.sprite.Sprite):# Player projectiles to throw at zombies
    '''This is a class for generating the little mushrooms that \
    the player can throw at zombies.'''

    def __init__(self, x, y, game):
        '''Initialise a life mushroom.Select the image, set surface area and x, y locations'''
        pygame.sprite.Sprite.__init__(self) #Initiate as a sprite
        self.game = game
        self.image = pygame.image.load('images/bonus10.png').convert() # Select the bonus mushroom image
        self.image = pygame.transform.scale(self.image, (25,25))# reduce to a smaller size for throwing
        self.image.set_colorkey((0,0,0))  #show background as transperant
        self.rect = self.image.get_rect() #get image as a rectangle object
        self.rect.x = x # Set initial x position
        self.rect.y = y # Set initial x position
        self.dir = game.player.dir # Set the direction the mushroom travel
        self.vel = 5 * self.dir# set the speed at which the mushroom will travel
        self.centre = self.image.get_rect().center # Find the image centre for rolling
        self.last_update = 0 # set image roll updates to 0
        self.fall_update = 0 # Set image fall update to 0
        self.mask = pygame.mask.from_surface(self.image) #pixel perfect collsion

    def update(self, game):
        '''Update mushroom position. \
        Remove mushroom from the list when falls below the window height'''
        self.game = game
        self.rect.x+= self.vel # Set next x pos
        self.animate() # Call the objects method to change what image is displayed
        if self.rect.x<-10 or self.rect.x > window_width+10: # If off the side of the screen
            self.kill() # Remove form teh groups
        if self.rect.y> window_height+10:# if below the screen (always falling)
            self.kill()# remove form teh groups

    def animate(self):
        '''Change how the image is displayed by rotating it with each frame to make it "roll".'''
        now = pygame.time.get_ticks() # set the last time the object was updated
        now_fall = pygame.time.get_ticks() # set the last time the object fell
        if now_fall - self.fall_update > 50: #Make the projectiles slowly fall
            self.fall_update = now_fall# update the time of last fall/ drop
            self.rect.y += 3# add 3 to y position
        if now - self.last_update > 250: #make projectiles spin as they are thrown
            self.last_update = now # set last spin update to now
            self.image = pygame.transform.rotate(self.image,90) # rotate image by 90 degrees
            self.centre = self.image.get_rect().center# set the image centre for new rotated image

class Extra_Life(pygame.sprite.Sprite):
    '''This is a class for generating the little mushrooms that \
    the player can get extra lives with.'''

    def __init__(self, x, y, pathlength,game):
        '''Initialise a life mushroom.Select the image, set surface area and x, y locations'''
        pygame.sprite.Sprite.__init__(self) #Initiate as a sprite
        self.game = game
        self.image = pygame.image.load('images/lives.png').convert() #image of mushroom
        self.image.set_colorkey((0,0,0)) # Set bac to transperant
        self.rect = self.image.get_rect() #get image as a rectangle object
        self.rect.x = x
        self.rect.y = y
        self.speed = game.speed# Set object speed as game speed
        self.dir = 1
        self.pathlength = pathlength-50# path length is passed in as the length of path the object is spawned on. removing 50 stops it falling off the path object
        self.path = 0
        self.counter = 0
        self.mask = pygame.mask.from_surface(self.image) #For pixel perfect collision

    def update(self):
        '''Update eExtra life. \
        Set new coordinates, and ensure sprite is not going past it's platform it was spawned on'''
        self.counter += (speed*self.dir)# Set the move size (left & right are different as all obejcts are moving left)
        if self.path == self.pathlength-2: #Turn
            self.path = 0
            self.dir *=-1
            self.counter += (speed*self.dir) +-1# updating the length of the distance & speed travelling
        elif self.dir<1 and self.path >=(self.pathlength//2):# moving right , half the length of the platorm
            self.counter = 0
            self.path = 0
            self.dir *=-1# change directions
        else:
            self.path+=1 #keep moving no turn
        self.rect.x += (speed*self.dir) +-1 # x is  in a fixed coordinate to "go right"
        if self.rect.right <0 or self.rect.y> window_height+20: #if object moves off screen, remove from group
            self.kill()


class Spritesheet:
    '''Utility class for loading and parsing spritesheets to class object'''

    def __init__(self, filename):
        '''Initiate class and load image'''
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        '''Locate an image on a larger spritesheet'''
        image = pygame.Surface((width, height)) # Size of the image
        image.blit(self.spritesheet, (0, 0), (x, y, width, height)) # blit the found image to the game screen
        return image
