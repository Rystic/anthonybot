import pygame
import socket
import time

pygame.init()

BLACK = (250, 250, 250)
WHITE = (255, 255, 255)

size = [700, 500]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Anthony-Bot Control Room")

done = False

clock = pygame.time.Clock()

joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print ("Error, I didn't find any joysticks.")
else:
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init()

HOST = input("Please enter the IP to connect to: ")    # The remote host
PORT = 50010            # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

prev_horiz_axis_pos = 0
prev_vert_axis_pos = 0

a_button = 0

b_button = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if event.type == pygame.JOYAXISMOTION:
        if joystick_count != 0:
            if (my_joystick.get_axis(0) < -.25):
                horiz_axis_pos = -1
            elif (my_joystick.get_axis(0) > .25):
                horiz_axis_pos = 1
            else:
                horiz_axis_pos = 0

            if (my_joystick.get_axis(1) < -.25):
                vert_axis_pos = -1
            elif (my_joystick.get_axis(1) > .25):
                vert_axis_pos = 1
            else:
                vert_axis_pos = 0

            if (horiz_axis_pos != prev_horiz_axis_pos or prev_vert_axis_pos != vert_axis_pos):
                prev_horiz_axis_pos = horiz_axis_pos
                prev_vert_axis_pos = vert_axis_pos
                data = "joystick," + str(horiz_axis_pos) + " " + str(vert_axis_pos) + "!"
                s.send(data.encode())
                screen.fill(BLACK)
            else:
                screen.fill(WHITE)
    if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
        if (a_button != my_joystick.get_button(0)):
            a_button = my_joystick.get_button(0)
            if (a_button == 1):
                data = "a_button"
                s.send(data.encode())
                screen.fill(BLACK)
            if (a_button == 0):
                data = "a_button_off"
                s.send(data.encode())
                screen.fill(BLACK)
        if b_button == 0 and my_joystick.get_button(1) == 1:
                data = "b_button"
                s.send(data.encode())
                screen.fill(BLACK)
                break
    b_button = my_joystick.get_button(1)
    pygame.display.flip()
    clock.tick(60)
s.close()
pygame.quit()