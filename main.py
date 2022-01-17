import pygame
import numpy as np
import random

col_about_to_die = (200, 200, 225)
col_alive = (255, 255, 215)
col_background = (10, 10, 40)
col_grid = (30, 30, 60)
x = 50
y = 50
zx = []

for i in range(y):
    z = []
    for i in range(x):
        z.append(random.randint(0, 1))
    zx.append(z)

def play_music(midi_filename):
    pygame.mixer.music.load(midi_filename)
    pygame.mixer.music.play(-1)


midi_filename = 'gol.mid'

freq = 44100  # audio CD quality
bitsize = -16  # unsigned 16 bit
channels = 2  # 1 is mono, 2 is stereo
buffer = 1024  # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)
pygame.mixer.music.set_volume(1.0)
def update(surface, cur, sz):
    nxt = np.zeros((cur.shape[0], cur.shape[1]))

    for r, c in np.ndindex(cur.shape):
        num_alive = np.sum(cur[r-1:r+2, c-1:c+2]) - cur[r, c]

        if cur[r, c] == 1 and num_alive < 2 or num_alive > 3:
            col = col_about_to_die
        elif (cur[r, c] == 1 and 2 <= num_alive <= 3) or (cur[r, c] == 0 and num_alive == 3):
            nxt[r, c] = 1
            col = col_alive

        col = col if cur[r, c] == 1 else col_background
        pygame.draw.rect(surface, col, (c*sz, r*sz, sz-1, sz-1))

    return nxt

def init(dimx, dimy):
    cells = np.zeros((dimy, dimx))
    pattern = np.array(zx);
    pos = (45,45)
    cells[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern
    return cells

def main(dimx, dimy, cellsize):
    gen = 0
    pygame.init()
    surface = pygame.display.set_mode((dimx * cellsize, dimy * cellsize))
    pygame.display.set_caption("John Conway's Game of Life. Gen:")

    cells = init(dimx, dimy)

    while True:
        print("Gen:", gen)
        gen = gen + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        surface.fill(col_grid)
        cells = update(surface, cells, cellsize)
        pygame.display.update()

if __name__ == "__main__":
    play_music(midi_filename)
    main(120, 120, 10)