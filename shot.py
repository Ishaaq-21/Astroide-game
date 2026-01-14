from circleshape import CircleShape
from constants import *
import pygame

class Shot(CircleShape) :
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
    def draw(self, screen):
        # Draw a directional streak
        if self.velocity.length() > 0:
            # Calculate tail and head
            # Visual length can be longer than hitbox radius
            direction = self.velocity.normalize()
            head = self.position + direction * self.radius
            tail = self.position - direction * self.radius * 2
            pygame.draw.line(screen, "white", tail, head, LINE_WIDTH + 1)
        else:
            pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)



    def update(self, dt):
        self.position += self.velocity * dt