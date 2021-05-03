"""This example spawns (bouncing) balls randomly on a L-shape constructed of 
two segment shapes. Not interactive.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

# Python imports
import random
from typing import List

# Library imports
import pygame

# pymunk imports
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

class Bread(object):

    def __init__(self, height) -> None:
        x = 600
        delta = 30
        # x, y = position
        y = height
        x -= delta

        mass = 25
        body = pymunk.Body()
        body.position = x, y
        shape = pymunk.Segment(body, (0, 0), (60, 0), 4)
        shape.mass = mass
        shape.elasticity = 0
        shape.friction = 0.9

        self.body = body
        self.shape = shape

class Surface(object):
    def __init__(self, height) -> None:
        x = 600
        y = height
        # x, y = position
        fp = [(20, -20), (-120, 0), (20, 20)]
        mass = 100
        # moment = pymunk.moment_for_poly(mass, fp)

        r_flipper_body = pymunk.Body()
        r_flipper_body.position = x + 120, y + 20 - 3
        r_flipper_shape = pymunk.Poly(r_flipper_body, fp)
        r_flipper_shape.mass = mass
        r_flipper_shape.friction = 0.9
        r_flipper_shape.elasticity = 0

        r_flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        r_flipper_joint_body.position = r_flipper_body.position
        j = pymunk.PinJoint(r_flipper_body, r_flipper_joint_body, (0, 0), (0, 0))
        s = pymunk.DampedRotarySpring(
            r_flipper_body, r_flipper_joint_body, 0.15, 20000000, 900000
        )


        self.body = r_flipper_body
        self.shape = r_flipper_shape
        self.j = j
        self.s = s

class Environment(object):
    """
    This class implements a simple scene in which there is a static platform (made up of a couple of lines)
    that don't move. Balls appear occasionally and drop onto the platform. They bounce around.
    """

    def __init__(self, bread, surface) -> None:
        # Space
        self._space = pymunk.Space()
        self._space.gravity = (0.0, 4 * 980)

        # Physics
        # Time step
        self._dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1

        # pygame
        self.width = 1000
        self.height = 1200 
        pygame.init()
        self._screen = pygame.display.set_mode((self.width, self.height))
        self._clock = pygame.time.Clock()

        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Static barrier walls (lines) that the balls bounce off of
        self._add_static_scenery()

        self.bread = bread
        self.surface = surface


        # Execution control and time until the next ball spawns
        self._running = True
        self._ticks_to_next_ball = 10

    def run(self) -> None:
        """
        The main loop of the game.
        :return: None
        """
        self._space.add(bread.body, bread.shape)
        self._space.add(surface.body, surface.shape)
        self._space.add(surface.j, surface.s)
        # surface.body.apply_impulse_at_local_point(
        #     Vec2d.unit() * -6000, (-100, 0)
        # )
        # Main loop
        # self._create_bread()
        while self._running:
            # Progress time forward
            for x in range(self._physics_steps_per_frame):
                self._space.step(self._dt)
            print(self.bread.body._get_angle() / (3.14/2))
            self._process_events()
            # self._create_bread()
            # self._update_balls()
            self._clear_screen()
            self._draw_objects()
            pygame.display.flip()
            # Delay fixed time between frames
            self._clock.tick(500)
            pygame.display.set_caption("fps: " + str(self._clock.get_fps()))

    def _add_static_scenery(self) -> None:
        """
        Create the static bodies.
        :return: None
        """
        static_body = self._space.static_body
        height = 900

        ground = pymunk.Segment(static_body, (0, height), (1000, height), 20)
        ground.elasticity = 0.9
        ground.friction = 0.9

        self._space.add(ground)



    def _process_events(self) -> None:
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(self._screen, "bouncing_balls.png")

    # def _update_balls(self) -> None:
    #     """
    #     Create/remove balls as necessary. Call once per frame only.
    #     :return: None
    #     """
    #     self._ticks_to_next_ball -= 1
    #     if self._ticks_to_next_ball <= 0:
    #         self._create_bread()
    #         self._ticks_to_next_ball = 100
    #     # Remove balls that fall below 100 vertically
    #     balls_to_remove = [ball for ball in self._rods if ball.body.position.y > 700]
    #     for ball in balls_to_remove:
    #         self._space.remove(ball, ball.body)
    #         self._rods.remove(ball)

    # def _create_bread(self) -> None:
    #     """
    #     Create a rods (bread).
    #     :return:
    #     """
    #     mass = 10
    #     inertia = pymunk.moment_for_segment(mass, (1, 2), (4, 2), 2)
    #     body = pymunk.Body(mass, inertia)

    #     x = 200
    #     y = 400 - 300
    #     body.position = x, y
    #     shape = pymunk.Segment(body, (0, 40), (40, -40), 6)
    #     shape.elasticity = 0.8
    #     shape.friction = 0.9
    #     self._space.add(body, shape)

    def _clear_screen(self) -> None:
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill(pygame.Color("white"))

    def _draw_objects(self) -> None:
        """
        Draw the objects.
        :return: None
        """
        self._space.debug_draw(self._draw_options)


if __name__ == "__main__":
    # position = 600, 320
    h = 75
    height = 890 - h * 4
    bread = Bread(height)
    surface = Surface(height)
    env = Environment(bread, surface)
    env.run()