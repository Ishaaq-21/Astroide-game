from circleshape import *
from constants import *
from logger import log_event
import random
class Asteroid(CircleShape): 
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.vectors = []
        self.generate_shape()
        self.rotation_speed = random.uniform(-50, 50)

    def generate_shape(self):
        # Generate a random irregular polygon
        self.vectors = []
        full_circle = 360
        num_points = 8
        step = full_circle / num_points
        self.angle_offset = random.uniform(0, 360) # Random initial rotation
        
        for i in range(num_points):
            angle = (i * step) + random.uniform(-10, 10)
            # Vary the distance to create jagged/irregular look
            # Staying within radius to respect hitbox roughly, but some spikes might poke out slightly visually
            dist = random.uniform(self.radius * 0.7, self.radius * 1.1) 
            # We store vectors relative to (0,0)
            vec = pygame.Vector2(0, 1).rotate(angle) * dist
            self.vectors.append(vec)

    def draw(self, screen):
        # Transform vectors based on position
        points = [self.position + vec.rotate(self.angle_offset) for vec in self.vectors]
        
        # Draw main body
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)
        
        # Optional: Add internal details for larger asteroids
        if self.radius > ASTEROID_MIN_RADIUS:
             # Draw a smaller inner loop or simple crack line
             start_idx = 0
             end_idx = int(len(points)/2)
             pygame.draw.line(screen, "white", points[start_idx], points[end_idx], 1)

    def update(self, dt):
        self.position += self.velocity * dt
        self.angle_offset += self.rotation_speed * dt


    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid split")
            rand_angle = random.uniform(20, 50)

            velocity1 = self.velocity.rotate(rand_angle)
            velocity2 = self.velocity.rotate(-rand_angle)

            new_radius = self.radius - ASTEROID_MIN_RADIUS

            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

            asteroid1.velocity = velocity1 * 1.2
            asteroid2.velocity = velocity2 * 1.2