import math
import argparse


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Position(x = {}, y = {})".format(self.x, self.y)


class Circle:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

    def __str__(self):
        return "Circle(position = {}, radius = {})".format(self.position, self.radius)


def circle_contains_circle(big_circle, small_circle):
    x_distance = big_circle.position.x - small_circle.position.x
    y_distance = big_circle.position.y - small_circle.position.y
    center_distance = math.sqrt((x_distance * x_distance) + (y_distance * y_distance))
    if big_circle.radius >= center_distance + small_circle.radius:
        return True
    else:
        return False


def circle_contains_position(circle, position):
    x_distance = circle.position.x - position.x
    y_distance = circle.position.y - position.y
    center_distance = math.sqrt((x_distance * x_distance) + (y_distance * y_distance))
    if circle.radius >= center_distance:
        return True
    else:
        return False


def calculate_gas_circle(big_circle, small_circle, ratio):
    reversed_ratio = 1.0 - ratio
    ratio_x = (reversed_ratio * big_circle.position.x) + (ratio * small_circle.position.x)
    ratio_y = (reversed_ratio * big_circle.position.y) + (ratio * small_circle.position.y)
    ratio_radius = small_circle.radius + (reversed_ratio * (big_circle.radius - small_circle.radius))
    return Circle(Position(ratio_x, ratio_y), ratio_radius)


def calculate_time_in_gas(current_time_in_gas, current_time, big_circle, small_circle, close_time, time_step, player_position, player_speed):
    current_time += time_step
    if close_time >= current_time:
        gas_circle = calculate_gas_circle(big_circle, small_circle, current_time / close_time)
        player_in_gas = not circle_contains_position(gas_circle, player_position)

        if not circle_contains_circle(big_circle, small_circle):
            print("Invalid arguments, big circle does not completely contain small circle")

        print("-------------------------------------------------------------------------------------------------------")
        print("Big circle: {}".format(big_circle))
        print("Gas circle: {}".format(gas_circle))
        print("Small circle: {}".format(small_circle))
        print("Current time: {}".format(current_time))
        print("Close time: {}".format(close_time))
        print("Time step: {}".format(time_step))
        print("Player position: {}".format(player_position))
        print("Player speed: {}".format(player_speed))
        print("Player in gas: {}".format(player_in_gas))
        print("-------------------------------------------------------------------------------------------------------")
        if player_in_gas:
            current_time_in_gas += time_step
        return calculate_time_in_gas(current_time_in_gas, current_time, big_circle, small_circle, close_time, time_step, player_position, player_speed)
    return current_time_in_gas


parser = argparse.ArgumentParser(description="Warzone Gas Circle Calculator")
parser.add_argument("--bigx", required=True, help="X Position of the Big circle", type=float)
parser.add_argument("--bigy", required=True, help="Y Position of the Big circle", type=float)
parser.add_argument("--bigradius", required=True, help="Radius of the Big circle", type=float)
parser.add_argument("--smallx", required=True, help="X Position of the Small circle", type=float)
parser.add_argument("--smally", required=True, help="Y Position of the Small circle", type=float)
parser.add_argument("--smallradius", required=True, help="Radius of the Small circle", type=float)
parser.add_argument("--closetime", required=True, help="Time left for the Big circle to reach the Small circle", type=float)
parser.add_argument("--timestep", required=True, help="Time that passes between each step", type=float)
parser.add_argument("--playerx", required=True, help="X Position of the Player", type=float)
parser.add_argument("--playery", required=True, help="Y Position of the Player", type=float)
parser.add_argument("--playerspeed", required=True, help="Distance covered by Player per unit of time", type=float)
args = parser.parse_args()

input_big_circle = Circle(Position(args.bigx, args.bigy), args.bigradius)
input_small_circle = Circle(Position(args.smallx, args.smally), args.smallradius)
input_player_position = Position(args.playerx, args.playery)

if not circle_contains_position(input_big_circle, input_player_position):
    print("Invalid arguments, big circle does not contain player")
    exit(1)

time_in_gas = calculate_time_in_gas(0.0, 0.0, input_big_circle, input_small_circle, args.closetime, args.timestep, input_player_position, args.playerspeed)
print("Player spent {} time in gas".format(time_in_gas))