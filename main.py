import numpy as np
from typing import List
from pymunk.vec2d import Vec2d
import pygame
import argparse

import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d


class Bread(object):
    def __init__(self, height, delta) -> None:
        x = 600
        delta = 0
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
        r_flipper_body.position = x + 120, y + 10
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

    def __init__(self, bread, surface, impulse, display=False) -> None:
        # Space
        self.display = display
        self._space = pymunk.Space()
        self._space.gravity = (0.0, 4 * 980)

        # Physics
        # Time step
        self._dt = 5.0 / 600.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1

        # pygame
        self.width = 1000
        self.height = 1200

        if display:
            pygame.init()
            self._screen = pygame.display.set_mode((self.width, self.height))
            self._clock = pygame.time.Clock()

            self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        self._add_ground()

        self.bread = bread
        self.surface = surface
        self.impulse = impulse

        # Execution control and time until the next ball spawns
        self._running = True
        self._ticks_to_next_ball = 10

    def run(self) -> bool:
        """
        The main loop of the game.
        :return: None
        """
        self._space.add(self.bread.body, self.bread.shape)
        self._space.add(self.surface.body, self.surface.shape)
        self._space.add(self.surface.j, self.surface.s)

        self._space.step(0.1)
        self.surface.body.apply_impulse_at_local_point(
            Vec2d.unit() * self.impulse, (-50, 0)
        )
        # Main loop
        while self._running:
            # Progress time forward
            for x in range(self._physics_steps_per_frame):
                self._space.step(self._dt)
            half_turn = self.bread.body._get_angle() / (3.14 / 2)
            butter_side_down = bool(round(half_turn) % 2)

            _, by = self.bread.body.position
            gy = 900
            dis = gy - by

            if 23.86 < abs(dis) < 24:
                if self.display:
                    self._clock.tick(1)
                # print(half_turn)
                break

            if self.display:
                pygame.display.flip()
                # Delay fixed time between frames
                self._clock.tick(10)

                self._process_events()
                self._clear_screen()
                self._draw_objects()
                pygame.display.set_caption("degree = %.1f" % (half_turn * 180))
        return butter_side_down

    def _add_ground(self) -> None:
        """
        Create ground.
        :return: None
        """
        static_body = self._space.static_body
        height = 900

        ground = pymunk.Segment(static_body, (0, height), (1000, height), 20)
        ground.elasticity = 0.9
        ground.friction = 0.9

        self.ground = ground

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


def simulation():
    # print('sim')
    height = np.random.random(1000) * 130 + 50 # 50 - 180
    # height = np.random.random(1000) * 200  # 50 - 180

    height = 890 - height * 4

    # Palm force: n(0, 10000)
    impluse = np.random.normal(0, 1000, size=1000)
    # relative position between the bread and the palm: u(-15, 0).
    delta = -np.random.random(1000) * 60

    results = []
    for h, i, d in zip(height, impluse, delta):
        bread = Bread(h, d)
        surface = Surface(h)
        env = Environment(bread, surface, i, display=False)
        butter_side_down = env.run()
        results.append(butter_side_down)
    # print(results)
    print(
        "probability of butter-side down is %.1f%%"
        % (sum(results) * 100 / len(results))
    )


def demo():
    h = 175
    height = 890 - h * 4
    bread = Bread(height, 0)
    surface = Surface(height)
    env = Environment(bread, surface, 10000, display=True)
    env.run()


if __name__ == "__main__":
    # position = 600, 320
    # simulation()
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--simulation", action="store_true")
    args = parser.parse_args()
    if args.simulation:
        simulation()
    if args.demo:
        demo()
