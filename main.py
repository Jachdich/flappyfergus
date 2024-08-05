import pygame, time, random

pygame.init()
screen = pygame.display.set_mode([1920, 1080])
fergus = pygame.image.load("fergus.png").convert_alpha()
fergus_size = fergus.get_rect()
comp = pygame.image.load("comp.png").convert_alpha()
soc = pygame.image.load("soc.png").convert_alpha()

font = pygame.font.SysFont('Comic Sans MS', 100)

running = True
pos = 1080/2+100
velocity = 0
accel = 1

class Pipe:
    def __init__(self, height, start_pos=1920):
        self.height = height
        self.pos = start_pos
        self.vel = 0

    def update(self):
        self.pos -= 10

    def get_upper_bounding_box(self):
        return (self.pos, 0, PIPE_WIDTH, self.height - GAP_WIDTH/2)

    def get_lower_bounding_box(self):
        return (pipe.pos, pipe.height + GAP_WIDTH/2, PIPE_WIDTH, 1080 - pipe.height - GAP_WIDTH/2)

def AABB_intersects(point, r, aabb):
    return point[0] >= aabb[0] - r and point[0] <= aabb[0] + aabb[2] + r and point[1] >= aabb[1] - r and point[1] <= aabb[1] + aabb[3] + r

def die():
    pipes.clear()
    global active_pipe, start_time, pos, velocity, countdown_till_activates
    velocity = 0
    pos = 1080/2+100
    start_time = time.time()
    active_pipe = None
    countdown_till_activates = 100

NUM_PIPES = 4
pipes = []

GAP_WIDTH = 500
PIPE_WIDTH = 100
frames_since_pipe = 120
countdown_till_activates = 100
start_time = time.time()
active_pipe = None
while running:
    frames_since_pipe += 1
    if frames_since_pipe >= 60:
        pipes.append(Pipe(random.randint(400, 1080-400)))
        frames_since_pipe = 0
    if active_pipe and active_pipe.pos < 200 and len(pipes) > 1:
        active_pipe = pipes[1]
    if not active_pipe and countdown_till_activates <= 0:
        countdown_till_activates = 0
        active_pipe = pipes[0]
    countdown_till_activates -= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity = -14
            if event.key == pygame.K_RETURN:
                if active_pipe:
                    active_pipe.vel = -10
                elif len(pipes) > 0:
                    active_pipe = pipes[0]
                
    screen.fill((255, 255, 255))

    for pipe in pipes:
        pipe.update()
        if AABB_intersects((250, pos), 30, pipe.get_upper_bounding_box()) or AABB_intersects((250, pos), 30, pipe.get_lower_bounding_box()):
            die()

    pipes = list(filter(lambda pipe: pipe.pos > -PIPE_WIDTH, pipes))

    velocity += accel
    pos += velocity
    if pos < -10 or pos > 1080 + 10:
        die()

    if active_pipe is not None:
        active_pipe.vel += accel * 0.8
        active_pipe.height += active_pipe.vel
        if active_pipe.height <= GAP_WIDTH/2:
            active_pipe.height = GAP_WIDTH/2
            active_pipe.vel = 0
            die()
        elif active_pipe.height >= 1080 - GAP_WIDTH/2:
            active_pipe.height = 1080 - GAP_WIDTH/2
            active_pipe.vel = 0
            die()

    screen.blit(fergus, (250 - fergus_size.width / 2, pos - fergus_size.height / 2))

    for pipe in pipes:
        upper = pipe.get_upper_bounding_box()
        lower = pipe.get_lower_bounding_box()
        compsoc_top = pygame.transform.scale(comp, upper[2:])
        compsoc_bottom = pygame.transform.scale(soc, lower[2:])
        screen.blit(compsoc_top, (upper[0], upper[1]))
        screen.blit(compsoc_bottom, (lower[0], lower[1]))

    
    text_surface = font.render("Score: " + str(int(time.time() - start_time)), False, (0, 0, 0))
    screen.blit(text_surface, (0, 1080 - 100))
    pygame.display.flip()

    time.sleep(1.0 / 60.0)

pygame.quit()

