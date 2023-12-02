import random
import pgzrun
from pgzhelper import *

# TODO: Replace the slime with Actor(images)
# TODO: Add a HP counter
# TODO: Add a score counter
# TODO: Add a game over screen
# TODO: Add a background image
# TODO: Add sound effects
# TODO: Adds collision detection between the player and the slimes

WIDTH = 800
HEIGHT = 450

# Player images
player_walk_imgs = [
    'male/male01-walk-1',
    'male/male01-walk-2',
    'male/male01-walk-3',
    'male/male01-walk-4',
    'male/male01-walk-5',
    'male/male01-walk-6',
]

# Player death images
player_death_imgs = [
    'male/male01-death-1',
    'male/male01-death-2',
    'male/male01-death-3',
]

# Projectile images
fireball_imgs = [
    'fireball/1',
    'fireball/2',
    'fireball/3',
    'fireball/4',
    'fireball/5',
    'fireball/6',
    'fireball/7',
    'fireball/8',
    'fireball/9',
    'fireball/10',
    'fireball/11',
    'fireball/12',
    'fireball/13',
    'fireball/14',
    'fireball/15',
    'fireball/16',
    'fireball/17',
    'fireball/18',
    'fireball/19',
    'fireball/20',
    'fireball/21',
    'fireball/22',
    'fireball/23',
    'fireball/24',
    'fireball/25',
    'fireball/26',
    'fireball/27',  
    'fireball/28',
    'fireball/29',
    'fireball/30',
]

slime_imgs = ['slime/idle/tile000',
              'slime/idle/tile001',
              'slime/idle/tile002',
              'slime/idle/tile003',
              'slime/idle/tile004',
              'slime/idle/tile005',
              'slime/idle/tile006',]

slime_death_imgs = ['slime/death/tile000',
                    'slime/death/tile001',
                    'slime/death/tile002',
                    'slime/death/tile003',
                    'slime/death/tile004',
                    'slime/death/tile005',
                    'slime/death/tile006',
]

enemies = []

# Initialize player Actor
slime = Actor(slime_imgs[0])
slime.images = slime_imgs

player = Actor(player_walk_imgs[0])
player.images = player_walk_imgs
player.scale = 3
player.left = 0
player.y = HEIGHT / 2
player.score = 0

projs = []
player.hp = random.randint(1,10)





def update():
    # Animate the player character
    player.animate()
    # Check if the player is in the death animation state
    if player.image in player_death_imgs:
        # Reset player images to walking animations when death animation is complete
        if player.image == player_death_imgs[-1]:
            print('done')
            player.images = player_walk_imgs
        print(f'{player.image} pending..')
        return
  

    # Player movement controls
    if keyboard.w:
        player.move_left(5)
    if keyboard.s:
        player.move_right(5)
    if keyboard.a:
        player.flip_x = True
        player.move_back(5)
    if keyboard.d:
        player.move_forward(5)
        player.flip_x = False


    # Boundary checks to keep the player within the screen
    if player.top < 0:
        player.top = 0
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT
    if player.left < 0:
        player.left = 0
    if player.right > WIDTH:
        player.right = WIDTH

    # Shooting projectiles when SPACE key is pressed
    if keyboard.SPACE:
        p = Actor(fireball_imgs[0])
        p.images = fireball_imgs
        p.pos = player.pos
        if player.flip_x:
            p.direction = 180
        else:
            p.direction = 0

        p.y += 10
        projs.append(p)

    # Remove projectiles that go off-screen
    for p in projs:
        p.animate()
        if p.x < 0 or p.x > WIDTH:
            projs.remove(p)
        else:
            p.move_in_direction(10)

    # Spawn enemies occasionally
    if random.randint(0, 100) < 1:
        e = Actor('slime/idle/tile000')  # Use a single image for simplicity
        e.images= slime_imgs
        e.scale = 3
        e.x = WIDTH
        e.y = random.randint(10, HEIGHT - 10)
        enemies.append(e)

    # Update enemy positions and interactions
    for e in enemies:
        e.animate()
        if e.image in slime_death_imgs:
            if e.image == slime_death_imgs[-1]:
                enemies.remove(e)
        else:
            e.move_towards(player,random.randint(1,4))
            if player.collide_pixel(e):
                player.hp -= 1
                player.images = player_death_imgs
                enemies.remove(e)
                print(player.hp)
            else:
                for p in projs:
                    if p.collide_pixel(e):
                        projs.remove(p)
                        e.images = slime_death_imgs
                        player.score += 1
                    
        e.x -= 5  # Move enemies from right to left
        e.scale = 3  # Set the scale for the enemy (adjust as needed)

        # Check if the player collides with an enemy


def draw():
    screen.clear()
    screen.draw.text(f'HP:{player.hp}',(10,10),fontsize=50)
    screen.draw.text(f'SCORE:{player.score}',(50,50),fontsize=50)
    player.draw()
    for p in projs:
        p.draw()
    for e in enemies:
        e.draw()
    if player.hp <= 0:
        screen.draw.text(f'You Lose',(WIDTH/2-80,HEIGHT/2), fontsize=80)


# Start the game
pgzrun.go()
