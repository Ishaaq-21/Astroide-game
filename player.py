from circleshape import CircleShape
from constants import *
import pygame
import random
from shot  import Shot
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 180
        self.shot_cooldown_timer = 0
        self.thrusting = False

    def draw(self, screen):
        # Draw the ship body
        pygame.draw.polygon(screen, "white", self.get_ship_shape(), LINE_WIDTH)
        
        # Draw engine glow if moving forward
        if self.thrusting:
            pygame.draw.polygon(screen, "cyan", self.get_flame_shape(), 0) # Fill flame

    def get_ship_shape(self):
        # Detailed ship shape
        rotation = self.rotation
        r = self.radius
        
        # Define relative points for a "cool" ship (pointing along 0,1 initially)
        # We use rotating vectors to position them
        forward = pygame.Vector2(0, 1).rotate(rotation)
        right = pygame.Vector2(0, 1).rotate(rotation + 90)
        
        # Ship vertices
        nose = self.position + forward * r
        l_wing_tip = self.position - forward * (r * 0.4) - right * (r * 0.9)
        r_wing_tip = self.position - forward * (r * 0.4) + right * (r * 0.9)
        l_engine = self.position - forward * (r * 0.8) - right * (r * 0.4)
        r_engine = self.position - forward * (r * 0.8) + right * (r * 0.4)
        center_tail = self.position - forward * (r * 0.5)
        
        return [nose, l_wing_tip, l_engine, center_tail, r_engine, r_wing_tip]

    def get_flame_shape(self):
        # Engine flame shape
        rotation = self.rotation
        r = self.radius
        forward = pygame.Vector2(0, 1).rotate(rotation)
        right = pygame.Vector2(0, 1).rotate(rotation + 90)
        
        # Base of flame is the engines/tail
        l_engine = self.position - forward * (r * 0.8) - right * (r * 0.3) # Slightly inside
        r_engine = self.position - forward * (r * 0.8) + right * (r * 0.3)
        # Flicker effect
        flicker = random.uniform(-10, 10) # Lateral flicker
        flame_len = random.uniform(1.3, 1.8) # Length flicker
        flame_tip = self.position - forward * (r * flame_len) + right * (flicker * 0.5)
        
        return [l_engine, flame_tip, r_engine]

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.thrusting = False # Reset state

        if keys[pygame.K_q]:
           self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_z]:
            self.move(dt)
            self.thrusting = True
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
            self.shot_cooldown_timer -= dt
    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.shot_cooldown_timer > 0 :
            return
        else:
            self.shot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED