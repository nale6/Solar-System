# Alejandro Cazorla

# A simulation of the Solar System using the pygame import. Currently only simulates the four terrestrial planets and the sun
# If there are troubleshooting errors, make sure python is added to PATH.
# Make sure there is only one version of python downloaded on the system.
# Change cd to the python script folder and paste the following line into cmd:
# python -m pip install pygame

# Imported modules
import pygame
import math

# Initialize pygame
pygame.init()

# Global variables for the window
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System")
pygame.display.flip()

# Color values for sun and planets
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 140, 230)
RED = (190, 40, 50)
GREY = (80, 80, 80)
BEIGE = (210, 185, 150)

# Creating a planet class to easily create the other planets as objects
class Planet:
  # Astronomical Units
  AU = (149.6e6 * 1000)

  # Gravity? FIXME
  GC = 6.67428e-11

  # Scale of Solar System down to our application
  # 1 AU to 1 PX = FIXME
  SCALE = (200 / AU)

  # Standard unit of elapsed time, which is per day per second
  ELAPSEDTIME = (3600 * 24)

  # Initialized variables for planet
  def __init__(self, x, y, radius, color, mass):
    self.x = x
    self.y = y
    self.radius = radius
    self.color = color
    self.mass = mass

    #True false flag for whether it is the sun or not
    self.sun = False
    self.distance_to_sun = 0
    self.orbit = []

    self.x_vel = 0
    self.y_vel = 0

  # Draws to the window
  def draw(self, win):
    x = self.x * self.SCALE + WIDTH / 2
    y = self.y * self.SCALE + HEIGHT / 2
    pygame.draw.circle(win, self.color, (x, y), self.radius)

  # Force of attraction that calculates the orbit using math functions
  def attraction(self, other):
    other_x, other_y = other.x, other.y
    distance_x = other_x - self.x
    distance_y = other_y - self.y
    
    # Calculates distance from sun
    distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

    # Checks if the other object is the sun
    if other.sun:
      self.distance_to_sun = distance

    # Physics calculations for attraction
    force = self.GC * self.mass * other.mass / (distance**2)
    theta = math.atan2(distance_y, distance_x)
    force_x = math.cos(theta) * force
    force_y = math.sin(theta) * force

    return force_x, force_y
    
  # Redraws the planet based on where their location would be for a given timeframe
  def update_position(self, planets):
      total_fx = total_fy = 0

      # Validation check to only update the correct planet
      for planet in planets:
        if self == planet:
          continue

        fx, fy = self.attraction(planet)

        total_fx += fx
        total_fy += fy
      
      # Calculations on the location of the planet in their orbit based on the time
      self.x_vel += total_fx / self.mass * self.ELAPSEDTIME
      self.y_vel += total_fy / self.mass * self.ELAPSEDTIME

      self.x += self.x_vel * self.ELAPSEDTIME
      self.y += self.y_vel * self.ELAPSEDTIME

      self.orbit.append((self.x, self.y))


def main():
  # List of planets
  sun = Planet(0, 0, 25, YELLOW, (1.98892 * 10**30))
  sun.sun = True

  mercury = Planet((0.387 * Planet.AU), 0, 8, GREY, (3.30 * 10**23))
  mercury.y_vel = -47.4 * 1000

  venus = Planet((0.723 * Planet.AU), 0, 13, BEIGE, (4.8685 * 10**24))
  venus.y_vel = -35.02 * 1000

  earth = Planet((-1 * Planet.AU), 0, 15, BLUE, (5.9742 * 10**24))
  earth.y_vel = 29.783 * 1000

  mars = Planet((-1.524 * Planet.AU), 0, 11, RED, (6.39 * 10**23))
  mars.y_vel = 24.077 * 1000

  planets = [sun, mercury, venus, earth, mars]

  run = True
  clock = pygame.time.Clock()

  # While the application is running, the window remains and updates the planet based on elapsed time and prior calculations
  while run:
    clock.tick(60)
    WIN.fill((0,0,0))

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

    for planet in planets:
      planet.update_position(planets)
      planet.draw(WIN)

    pygame.display.update()
  
  # Quits upon exiting the window
  pygame.quit()

main()