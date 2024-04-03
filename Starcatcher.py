# This is a game where you control a small spaceship.  Use left and right arrows to move left or right.  Catch stars to get a point.  
# If you catch an asteroid you lose a point. Reach winning score of 6 to win and end game.

import pygame
import random
from sys import exit
import os


#Game helps us keep track of our sprites and control updating them
class Game:
    def __init__(self):
        #sprites
        player_sprite = Player((screenWidth/2,screenHeight))
        asteroid1_sprite = Asteroid((random.randint(25, screenWidth - 50), 0))
        star_sprite = Star((random.randint(25, screenWidth - 50), 0))
        #groups
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.asteroid = pygame.sprite.GroupSingle(asteroid1_sprite)
        self.star = pygame.sprite.GroupSingle(star_sprite)
        
    def run(self):
        # score
        global score
        #Record asteroid collision with player and removes the asteroid and then we generate a new one
        if pygame.sprite.groupcollide(self.player,self.asteroid,False,True):
            score -= 1
            newAsteroid = Asteroid((random.randint(25, screenWidth - 50), 0))
            self.asteroid = pygame.sprite.GroupSingle(newAsteroid)
        #Star collision
        if pygame.sprite.groupcollide(self.player,self.star,False,True):
            score += 1
            newStar = Star((random.randint(25, screenWidth - 50), 0))
            self.star = pygame.sprite.GroupSingle(newStar)
        self.player.update()
        self.asteroid.update()
        self.star.update()
        self.player.draw(screen)
        self.asteroid.draw(screen)
        self.star.draw(screen)

#The spaceship is our main player
class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load('images/playerUFO.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.velocity = 5
    
    def get_input(self):
        keys = pygame.key.get_pressed()

        #On right arrow click, move player right with constraint that we can't go off screen
        if keys[pygame.K_RIGHT]:
            if self.rect.x >= screenWidth-self.image.get_width():
                self.rect.right = screenWidth
            else:
                self.rect.x += self.velocity 
        #On left arrow click, move player left with constraint that we can't go off screen        
        elif keys[pygame.K_LEFT]:
            if self.rect.x <= 0:
                self.rect.left = 0
            else:
                self.rect.x -= self.velocity
    
    def update(self):
        self.get_input()

#Falling asteroid object in the screen that we want players to avoid
class Asteroid(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load('images/asteroid.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.velocity = 4
 
    def update(self):
        #Want this object to keep falling, if it hits the bottom then we reset it back at the top at random x position
        if self.rect.y > screenHeight:
            self.resetPosition()
        self.rect.y += self.velocity
    
    def resetPosition(self):
        self.rect.x = random.randint(25, screenWidth - 50)
        self.rect.y = 0

#Falling star object in the screen that we want players to collect.
class Star(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load('images/star.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.velocity = 4
 
    def update(self):
        #Want this object to keep falling, if it hits the bottom then we reset it back at the top at random x position
        if self.rect.y > screenHeight:
            self.resetPosition()
        self.rect.y += self.velocity
    
    def resetPosition(self):
        self.rect.x = random.randint(25, screenWidth - 50)
        self.rect.y = 0

#Rendering text on screen for Score and also instructions underneath the score
def showScore():
    score_text = font.render("Score: " + str(score), True, (255,255,255))
    game_text = font.render("Catch only stars! ", True, (255,255,255))
    instructions_text = font.render("Use L and R arrows", True, (255,255,255))
    screen.blit(score_text,(25,25))
    screen.blit(game_text,(25,75))
    screen.blit(instructions_text,(25,125))

#This is text to indicate the game is over
def gameOver():
    game_over_text = font.render("YOU WIN!",True,(255,255,255))
    screen.blit(game_over_text,(screenWidth/2 - 80,screenHeight/3))

#Initializing the game and screen
pygame.init()
pygame.font.init()

#Screen
screenWidth = 800
screenHeight = 800
screen = pygame.display.set_mode((screenWidth,screenHeight))
backgroundImage = pygame.image.load('images/galaxy800.jpg').convert()
backgroundMusic = pygame.mixer.Sound('music/spacemusic.wav')
backgroundMusic.play(loops = -1)
#Score 
score = 0
winningScore = 6

font = pygame.font.Font('freesansbold.ttf', 32)
clock = pygame.time.Clock()



def main():
    #Initialize game
    game = Game()
    #Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        #Background
        screen.fill((30,30,30))

        #Check if game is over, display to player they won and then quit after some time
        if score == winningScore:
            gameOver()
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            exit()
        #Updating stuff in game such as sprites and score
        screen.blit(backgroundImage, (0,0))
        game.run()
        showScore()

        pygame.display.flip()
        clock.tick(60)

main()