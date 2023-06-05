import pygame
import random
import math

FONT = 'freesansbold.ttf'
FONT_SIZE = 32

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Asteroids')
icon = pygame.image.load('./aircraft.png')
pygame.display.set_icon(icon)


class MovingObject:
    def __init__(self, img_location, xcor, ycor, falling_speed):
        self.img = pygame.image.load(img_location)
        self.xcor = xcor
        self.ycor = ycor
        self.falling_speed = falling_speed

    def paste(self):
        screen.blit(self.img, (self.xcor, self.ycor))

    def fall(self):
        self.ycor += self.falling_speed

# Inheritance
class Asteroid(MovingObject):
    def __init__(self, img_location, xcor, ycor, falling_speed):
        super().__init__(img_location, xcor, ycor, falling_speed)

    def increase_speed(self, amount):
        self.falling_speed += amount

    def reposition(self):
        self.ycor = random.randint(-120, -64)
        self.xcor = random.randint(0, 734)


class PowerUp(MovingObject):
    def __init__(self, img_location, xcor, ycor, falling_speed):
        super().__init__(img_location, xcor, ycor, falling_speed)

    # Association
    def add_powerup(self, spaceship_obj):
        spaceship_obj.power_up = True

    def detect_collision(self, spaceship_obj):
        distance = math.sqrt(
            math.pow(spaceship_obj.xcor - self.xcor, 2) + (math.pow(spaceship_obj.ycor - self.ycor, 2)))
        if distance < 64:
            return True
        else:
            return False

    def reposition(self):
        self.xcor = random.randint(0, 730)
        self.ycor = random.randint(-2000, -1000)


class Safety(MovingObject):
    def __init__(self, img_location, xcor, ycor, falling_speed):
        super().__init__(img_location, xcor, ycor, falling_speed)

    def detect_collision(self, spaceship_obj):
        distance = math.sqrt(
            math.pow(spaceship_obj.xcor - self.xcor, 2) + (math.pow(spaceship_obj.ycor - self.ycor, 2)))
        if distance < 64:
            return True
        else:
            return False

    def add_safety(self, spaceship_obj):
        spaceship_obj.safety = True

    def reposition(self):
        self.xcor = random.randint(0, 730)
        self.ycor = random.randint(-2000, -1000)


class Life(MovingObject):
    def __init__(self, img_location, xcor, ycor, falling_speed):
        super().__init__(img_location, xcor, ycor, falling_speed)

    def detect_collision(self, spaceship_obj):
        distance = math.sqrt(
            math.pow(spaceship_obj.xcor - self.xcor, 2) + (math.pow(spaceship_obj.ycor - self.ycor, 2)))
        if distance < 64:
            return True
        else:
            return False

    def add_life(self, spaceship_obj):
        if spaceship_obj.lifes < 4:
            spaceship_obj.lifes += 1

    def reposition(self):
        self.xcor = random.randint(0, 730)
        self.ycor = random.randint(-5000, -750)


class Coin(MovingObject):
    def __init__(self, img_location, xcor, ycor, falling_speed):
        super().__init__(img_location, xcor, ycor, falling_speed)

    def increase_score(self, label_obj):
        label_obj.score += 1

    def reposition(self):
        self.ycor = random.randint(-1200, -450)
        self.xcor = random.randint(0, 730)

    def collision(self, spaceship_obj):
        distance = math.sqrt(
            math.pow(spaceship_obj.xcor - self.xcor, 2) + (math.pow(spaceship_obj.ycor - self.ycor, 2)))
        if distance < 64:
            return True
        else:
            return False


class SpaceShip:
    def __init__(self, bullet_obj, img_location, xcor, ycor, movement_speed, powered_bullet):
        # Aggregation
        self.bullet = bullet_obj
        self.lifes = 3
        self.image = pygame.image.load(img_location)
        self.xcor = xcor
        self.ycor = ycor
        self.movement_speed = movement_speed
        self.safety = False
        self.powered_bullets = powered_bullet
        self.power = False

    def update_bullet(self):
        self.bullet.update_location(self.xcor + 16, self.ycor + 10)

    def paste(self):
        screen.blit(self.image, (self.xcor, self.ycor))

    def move_left(self):
        self.xcor -= self.movement_speed

    def move_right(self):
        self.xcor += self.movement_speed

    def fire(self):
        self.bullet.fire()
        self.bullet.paste()

    def powerup(self):
        if self.power:
            self.powered_bullets.fire(self.xcor, self.ycor)

    def paste_powerup(self):
        self.powered_bullets.paste()

    def collision(self, asteroid_obj):
        distance = math.sqrt(math.pow(asteroid_obj.xcor - self.xcor, 2) + (math.pow(asteroid_obj.ycor - self.ycor, 2)))
        if distance < 64:
            return True
        else:
            return False

    def hit(self, asteroid_obj):
        if self.bullet.hit(asteroid_obj):
            return True
        else:
            return False

    def powered_hit(self, asteroid_obj):
        return self.powered_bullets.check_hits(asteroid_obj)

    def throw_bullets(self):
        self.powered_bullets.fall()


class Bullet(MovingObject):
    def __init__(self, img_location, xcor, ycor, falling_speed):
        super().__init__(img_location, xcor, ycor, falling_speed)
        self.state = 'off'

    def reload(self):
        self.state = 'on'

    def fire(self):
        super().fall()
        self.state = 'off'

    def reposition(self):
        self.ycor = -1000

    def hit(self, asteroid_obj):
        distance = math.sqrt(
            math.pow(asteroid_obj.xcor - self.xcor, 2) + (math.pow(asteroid_obj.ycor - self.ycor, 2)))
        if distance < 64:
            self.state = 'on'
            self.reposition()
            return True
        else:
            return False

    def update_location(self, xcor, ycor):
        self.xcor = xcor
        self.ycor = ycor

    def custom_fall(self, xcor_falling_speed):
        self.fall()
        self.xcor += xcor_falling_speed


class PoweredBullet:
    def __init__(self, img_location, xcor, ycor, falling_speed):
        # Composition
        bullet_1 = Bullet(img_location, xcor, ycor, falling_speed)
        bullet_2 = Bullet(img_location, xcor, ycor, falling_speed)
        bullet_3 = Bullet(img_location, xcor, ycor, falling_speed)
        self.bullets = [bullet_1, bullet_2, bullet_3]

    def fire(self, spaceship_xcor, spaceship_ycor):
        xcors = [0, 16, 32]
        ycors = [10, 10, 10]
        for i in range(len(self.bullets)):
            self.bullets[i].xcor = spaceship_xcor + xcors[i]
            self.bullets[i].ycor = spaceship_ycor + ycors[i]

    def paste(self):
        for i in self.bullets:
            i.paste()

    def delete_bullet(self):
        for i in self.bullets:
            if i.ycor < - 10:
                self.bullets.remove(i)

    def fall(self):
        xcor_falling_speeds = [-0.3, 0, 0.3]
        for i in self.bullets:
            index = self.bullets.index(i)
            i.custom_fall(xcor_falling_speeds[index])

    def check_hits(self, asteroid_obj):
        for i in self.bullets:
            if i.hit(asteroid_obj):
                i.reposition()
                asteroid_obj.reposition()
                return True


class Label:
    def __init__(self, score, font, size, xcor, ycor):
        self.score = score
        self.font = font
        self.size = size
        self.xcor = xcor
        self.ycor = ycor

    def paste(self):
        font = pygame.font.Font(self.font, self.size)
        score = font.render("Score : " + str(self.score), True, (255, 255, 255))
        screen.blit(score, (self.xcor, self.ycor))

    def update(self):
        self.score += 1


class ScoreBoard(Label):
    def __init__(self, score, font, size, xcor, ycor):
        super().__init__(score, font, size, xcor, ycor)
        self.highscore = self.set_highscore('./highscore.txt')

    def set_highscore(self, location):
        try:
            with open(location, 'r') as file:
                data = int(file.read())
                return data
        except:
            with open(location, 'w') as file:
                a = ''
                return 0

    def update_highscore(self):
        highscore = self.highscore
        if self.score > self.highscore:
            highscore = self.score
        with open('./highscore.txt', 'w') as file:
            file.write(str(highscore))

    def paste(self):
        font = pygame.font.Font(self.font, self.size)
        score = font.render("Score : " + str(self.score) + " Highscore : " + str(self.highscore), True, (255, 255, 255))
        screen.blit(score, (self.xcor, self.ycor))


class Level(Label):
    def __init__(self, level, font, size, xcor, ycor):
        super().__init__(level, font, size, xcor, ycor)

    def increase_level(self, scoreboard_obj):
        if scoreboard_obj.score < 15:
            self.score = 1
        else:
            score = scoreboard_obj.score
            self.score = (score // 15) + 1

    def paste(self):
        font = pygame.font.Font(self.font, self.size)
        score = font.render("Level : " + str(self.score), True, (255, 255, 255))
        screen.blit(score, (self.xcor, self.ycor))

    def calc_asteroids(self):
        if self.score < 6:
            asteroids_no = self.score + 2
            return asteroids_no
        else:
            asteroid_no = 9
            return asteroid_no


class LifeBars:
    def __init__(self, img_location, xcor, ycor):
        self.xcor = xcor
        self.ycor = ycor
        self.life_1 = pygame.image.load(img_location)
        self.life_2 = pygame.image.load(img_location)
        self.life_3 = pygame.image.load(img_location)
        self.life_4 = pygame.image.load(img_location)
        self.lives = [self.life_1, self.life_2, self.life_3, self.life_4]

    def paste(self, spaceship_obj):
        lives_num = spaceship_obj.lifes
        self.needed_lives = self.lives[:lives_num]
        xcor = self.xcor
        for i in self.needed_lives:
            screen.blit(i, (xcor, self.ycor))
            xcor += 20


def change_coins(coins):
    if level_banner.score % 5 == 0:
        if len(coins) == 20:
            return
        else:
            new_coins_amount = 20 - len(coins)
            for i in range(new_coins_amount):
                xcor = random.randint(0, 734)
                ycor = random.randint(-1200, -300)
                new_coin = Coin(img_location='./star.png', xcor=xcor, ycor=ycor, falling_speed=0.3)
                coins.append(new_coin)
    else:
        if len(coins) == 3:
            return
        else:
            while len(coins) != 3:
                coins.pop(0)

def check_level_and_increase_asteroids(asteroids, level_banner):
    if len(asteroids) == level_banner.calc_asteroids():
        return
    elif len(asteroids) == 8:
        score = level_banner.score
        base_speed = 0.2
        speed_to_increase = score / 1000
        final_speed = base_speed + speed_to_increase
        for i in asteroids:
            i.increase_speed(final_speed)
    else:
        new_asteroids_num = level_banner.calc_asteroids() - len(asteroids)
        for i in range(new_asteroids_num):
            ycor = random.randint(-120, 64)
            xcor = random.randint(0, 734)
            new_asteroid_obj = Asteroid(img_location='./asteroid.png', xcor=xcor, ycor=ycor, falling_speed=0.35)
            asteroids.append(new_asteroid_obj)


# Shield object
shield = Safety(img_location='./shield.png', xcor=random.randint(0, 730), ycor=random.randint(-1200, -700),
                falling_speed=0.3)

# Floating life object
floating_life = Life('./life.png', random.randint(0, 730), random.randint(-2000, -750), 0.3)

# power up object

# floating_powerup = PowerUp('./bullet.png', xcor=random.randint(0,730), ycor=random.randint(-4000,-2000), falling_speed=0.3)
floating_powerup = PowerUp('./merkaba.png', xcor=50, ycor=50, falling_speed=0.8)

# Making Bullets and spaceship
bullet = Bullet(img_location='./bullet.png', xcor=0, ycor=0, falling_speed=-3)
powered_bullets = PoweredBullet(img_location='./bullet.png', xcor=1000, ycor=0, falling_speed=-3)
spaceship = SpaceShip(bullet, './spaceship.png', 370, 480, 2, powered_bullets)

# Level banner and scoreboard and lives
scoreboard = ScoreBoard(0, FONT, 20, 0, 0)
level_banner = Level(1, FONT, 20, 400, 0)
lifebars = LifeBars('./heart.png', 700, 0)

# Making coins objects
coins = []
for i in range(3):
    xcor = random.randint(0, 734)
    ycor = random.randint(-1200, -300)
    new_coin = Coin(img_location='./star.png', xcor=xcor, ycor=ycor, falling_speed=0.3)
    coins.append(new_coin)

# Making asteroids objects
asteroid_num = level_banner.calc_asteroids()
asteroids = []
for i in range(asteroid_num):
    ycor = random.randint(-120, 64)
    xcor = random.randint(0, 734)
    new_asteroid_obj = Asteroid(img_location='./asteroid.png', xcor=xcor, ycor=ycor, falling_speed=0.5)
    asteroids.append(new_asteroid_obj)

# Making the background
background = pygame.image.load('./refined_bg.jpg')

safety_bubble = pygame.image.load('./safetybubble.png')
move_left = False
move_right = False
powerup_available = False
# Game loop
throw_count = 50_000
bullet_available = True
game_on = True
game_over = False
game_over_font = pygame.font.Font(FONT, FONT_SIZE)
game_over_img = game_over_font.render("Game Over", True, (255, 255, 255))
bonus_level = False

bonus_banner_font = pygame.font.Font(FONT, 35)
bonus_banner_img = bonus_banner_font.render("BONUS ROUND", True, (255,215,0))


while game_on:
    # setting the background
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))


    #Checking if bonus level is on (Every multiple of 5 is a bonus level)
    if level_banner.score % 5 == 0:
        bonus_level = True
        screen.blit(bonus_banner_img, (300,100))
    else:
        bonus_level = False
    # Functionality required to make quitting the game accessible

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False

        # Adding functionality to keys and checking if they are pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_SPACE:
                if bullet_available:
                    spaceship.update_bullet()
                    bullet_available = False
            if event.key == pygame.K_s:
                if powerup_available:
                    spaceship.power = False
                    powerup_available = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False

    if spaceship.bullet.ycor < 0:
        bullet_available = True

    if spaceship.xcor < 0:
        move_left = False
    if spaceship.xcor > 730:
        move_right = False

    if move_left:
        spaceship.move_left()
    if move_right:
        spaceship.move_right()

    if not game_over:
        # adjusting coins according to bonus level (every multiple of 5)
        change_coins(coins)
        # making asteroids fall
        if not bonus_level:
            for asteroid in asteroids:
                asteroid.fall()
                asteroid.paste()

                # checking if the bullet hit the asteroid
                if spaceship.hit(asteroid):
                    scoreboard.update()
                    asteroid.reposition()
                    bullet_available = True

                if spaceship.powered_hit(asteroid):
                    scoreboard.update()

                # Checking for collision
                if spaceship.collision(asteroid):
                    asteroid.reposition()
                    if spaceship.safety:
                        spaceship.safety = False
                    else:
                        spaceship.lifes -= 1

                # Checking if the asteroid is out of bounds
                if asteroid.ycor > 550:
                    asteroid.reposition()
                    spaceship.lifes -= 1

        # Tracking the life
        if floating_life.detect_collision(spaceship):
            floating_life.add_life(spaceship)
            floating_life.reposition()

        if floating_life.ycor > 550:
            floating_life.reposition()

    # Tracking the shield
    if shield.detect_collision(spaceship):
        spaceship.safety = True
        shield.reposition()
    if not game_over:
        # Making coins fall
        for coin in coins:
            coin.fall()
            coin.paste()

            # repositioning coins in case they fall out of bounds
            if coin.ycor > 550:
                coin.reposition()

            if coin.collision(spaceship):
                scoreboard.update()
                coin.reposition()

    # making the safety bubble image visible if the spaceship's safety is on
    if spaceship.safety:
        screen.blit(safety_bubble, (spaceship.xcor - 3, spaceship.ycor))

    # Tracking the floating powerup
    if floating_powerup.detect_collision(spaceship):
        spaceship.power = True
        floating_powerup.reposition()
        spaceship.powerup()
        powerup_available = True
    if not game_over:
        if floating_powerup.ycor > 550:
            floating_powerup.reposition()
        floating_powerup.fall()
        floating_powerup.paste()
        floating_life.paste()
        floating_life.fall()
        shield.paste()
        shield.fall()

    if spaceship.lifes < 1:
        game_over = True
        screen.blit(game_over_img, (300, 250))
        scoreboard.update_highscore()

    # Polymorphic behaviour with paste()
    spaceship.throw_bullets()
    spaceship.paste_powerup()
    spaceship.powerup()
    check_level_and_increase_asteroids(asteroids, level_banner)
    spaceship.fire()
    scoreboard.paste()
    level_banner.increase_level(scoreboard)
    level_banner.paste()
    spaceship.paste()
    lifebars.paste(spaceship)

    pygame.display.update()
