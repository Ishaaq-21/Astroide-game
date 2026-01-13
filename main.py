import pygame
from constants import *
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from logger import log_event
import sys
def main():

    pygame.init()
    print("Starting Asteroids")
    print("Screen width: 1280")
    print("Screen height: 720")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0


    updatable  = pygame.sprite.Group()
    drawable  = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, drawable, updatable)

    astroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        log_state()

        updatable.update(dt)
        for obj in asteroids :
            if obj.collides_with(player) :
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            for shot in shots:
                if shot.collides_with(obj):
                    log_event("asteroid_shot")
                    obj.split()
                    shot.kill()
        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000
if __name__ == "__main__":
    main()