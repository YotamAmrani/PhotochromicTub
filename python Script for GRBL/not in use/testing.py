import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((800,600))
# https://www.pygame.org/docs/ref/time.html#pygame.time.set_timer

going = True
while going:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print("YO")
            if event.key == pygame.K_a:
                print("yo")
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        print("zo")
    # without this there is "Fatal Python error: PyEval_SaveThread: NULL tstate\nAbort trap: 6"
    clock.tick(60)

# events = pygame.event.get()
# xyz = [False, False, False, False, False, False]
# for event in events:
#     if event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_a:
#             # move_left()
#             xyz[0] = True
#         elif event.key == pygame.K_d:
#             # move_right()
#             xyz[1] = True
#         if event.key == pygame.K_w:
#             # move_front()
#             xyz[2] = True
#         elif event.key == pygame.K_s:
#             # move_back()
#             xyz[3] = True
#         if event.key == pygame.K_z:
#             # move_up()
#             xyz[4] = True
#         elif event.key == pygame.K_x:
#             # move_down()
#             xyz[5] = True
# if xyz[0]:
#     move_left()
# elif xyz[1]:
#     move_right()
# if xyz[2]:
#     move_front()
# elif xyz[3]:
#     move_back()
# if xyz[4]:
#     move_up()
# elif xyz[5]:
#     move_down()
