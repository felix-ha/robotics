import sys, pygame
import numpy as np
import time
from optimization_robotic import GradientDescent
from matrices import translation, flip_y

class Point():
    def __init__(self, x, y, center):
        self.center = center

        self.x = x
        self.y = y
        self.homogen_coordinates =  np.array([x, y, 1])
        self.homogen_coordinates_game = np.matmul(flip_y() * translation(self.center[0], -self.center[1]),
                                                  self.homogen_coordinates)
        self.x_game = int(self.homogen_coordinates_game[0,0])
        self.y_game = int(self.homogen_coordinates_game[0,1])


class Robot():
    def __init__(self, center):
        self.center = center

        self.length = (160, 160)
        self.theta = (0,0)

        self.update_pos(self.theta)

    def update_pos(self, theta):
        self.theta = theta

        self.update_coordinates_joint()
        self.update_coordinates_tcp()

        self.joint_1 = Point(self.x_joint_1, self.y_joint_1, self.center)
        self.tcp = Point(self.x_tcp, self.y_tcp, self.center)

    def update_coordinates_joint(self):
        self.x_joint_1 = int(self.length[0] * np.cos(self.theta[0]))
        self.y_joint_1 = int(self.length[0] * np.sin(self.theta[0]))

    def update_coordinates_tcp(self):
        self.x_tcp = int(self.x_joint_1 + self.length[1] * np.cos( np.sum(self.theta)))
        self.y_tcp = int(self.y_joint_1 + self.length[1] * np.sin(np.sum(self.theta)))

    def forward_kinematic(self, theta):
        x_joint_1 = self.length[0] * np.cos(theta[0])
        y_joint_1 = self.length[0] * np.sin(theta[0])
        x_tcp = x_joint_1 + self.length[1] * np.cos(np.sum(theta))
        y_tcp = y_joint_1 + self.length[1] * np.sin(np.sum(theta))
        return x_tcp, y_tcp

    def get_trajectory(self, coordinates_destination):
        self.coordinates_destination = coordinates_destination

        destination_precession = 1
        opt = GradientDescent(2000, 0.005, destination_precession, self)
        x_0 = np.array([0, 0])

        result = opt.optimize(self.F, x_0)
        result.print()

        return result.x

    def F(self, theta):
        x_tcp, y_tcp = self.forward_kinematic(theta)
        position_current = np.array([x_tcp, y_tcp])
        position_destination = np.array([self.coordinates_destination.x, self.coordinates_destination.y])

        y = .5 * np.linalg.norm(np.array([position_destination - position_current]))

        return y


    def draw(self, screen):
        pygame.draw.line(screen, [0,0,0], (self.center[0], self.center[1]), (self.joint_1.x_game, self.joint_1.y_game), 3)
        pygame.draw.line(screen, [0,0,0], (self.joint_1.x_game, self.joint_1.y_game), (self.tcp.x_game, self.tcp.y_game), 3)

        pygame.draw.circle(screen, [0, 0, 255], (self.joint_1.x_game, self.joint_1.y_game), 10)
        pygame.draw.circle(screen, [0,0,255], (self.tcp.x_game, self.tcp.y_game), 15, 1)
        pygame.draw.circle(screen, [255,0,255], (self.tcp.x_game, self.tcp.y_game), 3)



class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Robot')

        self.black = [0, 0, 0]
        self.white = [255, 255, 255]

        self.width, self.height = 740, 740
        self.size = (self.width, self.height)
        self.center = self.width/2,self.height/2

        self.robot = Robot(self.center)


    def reach_given_destination(self, x, y):
        self.coordinates_destination = Point(x, y, self.center)
        trajectory = self.robot.get_trajectory(self.coordinates_destination)

        self.screen = pygame.display.set_mode(self.size)
        for i in range(len(trajectory)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            self.screen.fill(self.white)
            self.draw_coordinate_system()
            self.draw_destination()

            theta = trajectory[i]
            self.robot.update_pos(theta)
            self.robot.draw(self.screen)

            pygame.display.flip()
            time.sleep(0.0024)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

    def follow_given_trajectory(self, trajectory):
        self.screen = pygame.display.set_mode(self.size)
        for i in range(len(trajectory)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            self.screen.fill(self.white)
            self.draw_coordinate_system()

            theta = trajectory[i]
            self.robot.update_pos(theta)
            self.robot.draw(self.screen)

            pygame.display.flip()
            time.sleep(0.002)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()


    def draw_coordinate_system(self):
        pygame.draw.line(self.screen, self.black, (0, self.center[1]), (self.width, self.center[1]))
        pygame.draw.line(self.screen, self.black, (self.center[0], 0), (self.center[0], self.height))
        pygame.draw.circle(self.screen, self.black, (int(self.center[0]), int(self.center[1])), 5)

    def draw_destination(self):
        rect = pygame.Rect(self.coordinates_destination.x_game,
                           self.coordinates_destination.y_game, 5, 5)
        pygame.draw.rect(self.screen, self.black, rect)


def get_sample_trajectory(length):
    trajectory = np.ndarray(shape=[length,2])
    for i in range(length):
        trajectory[i] = [(i/length) * np.pi,0]

    return trajectory

if __name__ == '__main__':

    game = Game()
    #game.follow_given_trajectory(get_sample_trajectory(1000))
    game.reach_given_destination(-100, 100)