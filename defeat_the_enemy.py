#import and initialize pygame
import pygame
pygame.init()

#initialize a window for display
window = pygame.display.set_mode((400,400))
#set window caption
pygame.display.set_caption("Defeat the enemy")

#load player sprites
playerWalkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
playerWalkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]

#set background image
bgimg = pygame.image.load('bg.jpg')

#standing player sprite
playerStanding = pygame.image.load('standing.png')

#create an object to help track time
clock = pygame.time.Clock()

#set score variable to 0
score = 0

#set the screen width
screenWidth = 400

class Player(object):
    """Create the player's character"""
    def __init__(self, x, y, width, height):
        #characters attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5         
        self.left = False
        self.right = False
        self.standing = True
        self.steps = 0
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, window):
        """Draw the character"""
        #display each sprite in 3 frames
        if self.steps + 1 >= 27:
            self.steps = 0

        if self.standing == False:
            if self.left == True:
                #index the correct sprite; each sprite will appear 3 times
                window.blit(playerWalkLeft[self.steps//3], (self.x,self.y)) 
                self.steps += 1
            elif self.right == True:
                window.blit(playerWalkRight[self.steps//3], (self.x,self.y))
                self.steps += 1
        #if the character is standing, we check to see the direction he is facing
        else:
            if self.right == True:
                window.blit(playerWalkRight[0], (self.x, self.y))
            else:
                window.blit(playerWalkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
    
    def hit(self):
        #restart player's position after collision
        self.x = 10
        self.y = 335
        self.steps = 0
        setFont = pygame.font.SysFont('comicsans', 100)
        #display '-2' on the screen
        hitScoreText = setFont.render('-2', 1, (255, 0, 0))
        window.blit(hitScoreText, (screenWidth/2 - (hitScoreText.get_width()/2), 100))
        pygame.display.update()

        #check for events
        i = 0
        while i < 300:
            pygame.time.delay(2)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

class Projectile(object):
    """Create the bullets"""
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction #this attribute is going to be 1 or -1
        self.speed = 8 * direction

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

class Enemy(object):
    """Create the enemy"""
    #load enemy sprites    
    enemyWalkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    enemyWalkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    
    def __init__(self, x, y, width, height, end):
        """Create the enemy's character"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.limits = [self.x, self.end]
        self.steps = 0
        self.speed = 3
        self.health = 15
        self.visible = True
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)

    def draw(self, window):
        """Draw the enemy"""
        self.move()
        if self.visible == True:
            #display each sprite in 3 frames
            if self.steps + 1 >= 33:
                self.steps = 0

            if self.speed > 0:
                #if the enemy is moving right
                window.blit(self.enemyWalkRight[self.steps //3], (self.x, self.y))
                self.steps += 1
            else:
                #if the enemy is moving left
                window.blit(self.enemyWalkLeft[self.steps //3], (self.x, self.y))
                self.steps += 1

            #draw the health bar
            pygame.draw.rect(window, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) #red health bar
            pygame.draw.rect(window, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50/15) * (15 - self.health)), 10)) #green health bar
            self.hitbox = (self.x + 17, self.y + 2, 30, 57)

    def move(self):
        """Check movement"""
        #if the enemy is moving to the right
        if self.speed > 0:
            if self.x + self.speed < self.limits[1]:
                #if the enemy hasn't reached the right side of the limit he can make the move
                self.x += self.speed
            else:
                #the enemy has reached the limit so he needs to change direction
                self.speed = self.speed * -1
                self.steps = 0
        #if the enemy is moving to the left
        else:
            if self.x - self.speed > self.limits[0]:
                #if the enemy hasn't reached the left side of the limit he can make the move
                self.x += self.speed
            else:
                #the enemy has reached the limit so he needs to change direction
                self.speed = self.speed * -1
                self.steps = 0

    def hit(self):
        """Check if the enemy is hit"""
        if self.health > 0:
            self.health -=1
        else:
            #if the enemy's health is below 0, he is no longer displayed on the window
            self.visible = False
        print("hit")

         
def redrawGameWindow():
    """Redraw the game window"""
    window.blit(bgimg, (0,0)) #filling the screen with a picture so the user can't see the character repeating
    
    #display the score on the window
    scoreText = font.render("Score: " + str(score), 1, (0, 0, 0))
    window.blit(scoreText, (250, 10))

    #drawing the characters on the window
    hero.draw(window)
    enemy.draw(window)
    
    #draw the bullets
    for bullet in bullets:
        bullet.draw(window)    
    pygame.display.update()

def open_file():
    """Open and print the game instructions"""
    try:
        text_file = open("instructions.txt", "r")
        instructions_text = text_file.read()
        print()
        print(instructions_text)
        print()
        text_file.close()
    except (FileNotFoundError):
        print("\nDefeat the enemy!\nUse the SPACE key to shoot bullets.\n")

#MAIN LOOP
#initialize and set the style of the font
font = pygame.font.SysFont('comicsans', 25, True) #True -> bold text

#create instances of the characters
hero = Player(200, 335, 64, 64) 
enemy = Enemy(90, 335, 64,64, 270)

#empty list to keep the bullets
bullets = []

#setting a basic timer for bullets
shoot = 0

open_file()

run = True
while run:
    #set the framerate
    clock.tick(27)

    if enemy.visible == True:
        #if the top of the hero's hitbox is ABOVE the bottom of the enemy's hitbox AND the bottom of the hero's hitbox is BELOW the top of the enemy's hitbox
        if hero.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and hero.hitbox[1] + hero.hitbox[3] > enemy.hitbox[1]:
            #if the right side of the hero's hitbox is AFTER the left side of the enemy's hitbox AND the left side of the hero's hitbox is BEFORE the right side of the enemy's hitbox
            if hero.hitbox[0] + hero.hitbox[2] > enemy.hitbox[0] and hero.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
                hero.hit()
                score -= 2

    #timer; sets a few milliseconds break between the bullets so that they are not making groups
    if shoot > 0:
        shoot += 1
    if shoot > 3:
        shoot = 0
        
    #check for events = anything that happens from the user
    for event in pygame.event.get():
        #if the user is clicking the 'X' button in the right top corner of the game window
        if event.type == pygame.QUIT:
            #exits the loop
            run = False

    for bullet in bullets:
        #if the top of the bullet is ABOVE the bottom of the enemy's hitbox AND the bottom of the bullet is BELOW the top of the enemy's hitbox
        if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
            #if the right side of the bullet is AFTER the left side of the enemy's hitbox AND the left side of the bullet is BEFORE the right side of the enemy's hitbox
            if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                enemy.hit()
                score += 1
                #first we add the bullet to the list, then we remove it
                bullets.pop(bullets.index(bullet))
                
        if bullet.x < screenWidth and bullet.x > 0:
            #if the bullet is still on the window, we can add the move
            bullet.x += bullet.speed
        else:
            #otherwise, we delete it from the list
            bullets.pop(bullets.index(bullet))

    #setting up a list for keys
    keys = pygame.key.get_pressed()

    #animating the hero
    if keys[pygame.K_SPACE] and shoot == 0:
        if hero.left:
            #if the hero is looking to the left, it shoots in that direction
            direction = -1
        else:
            direction = 1
          
        if len(bullets) < 5:
            #creates an instance of the bullet and adds it to the bullets list
            #the bullets are shot from the middle of the hero
            bullets.append(Projectile(round(hero.x + hero.width //2), round(hero.y + hero.height //2), 6, (0, 0, 0), direction))

        shoot = 1
        
    if keys[pygame.K_LEFT] and hero.x > hero.speed: 
        #move the hero towards left
        hero.x -= hero.speed
        hero.left = True
        hero.right = False
        hero.standing = False
    elif keys[pygame.K_RIGHT] and hero.x < screenWidth - hero.width - hero.speed: #also check if the character is still on the screen
        #move the hero towards right
        hero.x += hero.speed
        hero.right = True
        hero.left = False
        hero.standing = False
    else:
        #hero is standing
        hero.standing = True
        hero.steps = 0
        
    redrawGameWindow()
pygame.quit()
