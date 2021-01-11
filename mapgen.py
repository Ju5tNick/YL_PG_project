import pygame
from random import randrange, choice

X, Y = 40, 20

def render(chunk: list):
    render_map = pygame.sprite.Group()
    for rrow in range(Y):
        for rcol in range(X):
            tile = pygame.sprite.Sprite()
            if chunk[rrow][rcol] == 1:
                image = pygame.image.load(f"data/images/grass/grass{str(choice(list(range(1, 7))))}.png")
            if chunk[rrow][rcol] == 3:
                image = pygame.image.load(f"data/images/sand/sand{str(choice(list(range(1, 4))))}.png")
            if chunk[rrow][rcol] == 0:
                image = pygame.image.load(f"data/images/water/water3{str(choice(list(range(1, 4))))}.png")

            tile.image = image
            tile.rect = image.get_rect()
            tile.rect.x, tile.rect.y = rcol * 25, rrow * 25
            render_map.add(tile)
    render_map.draw(screen)
    pygame.display.flip()


def generate():
    chunk, flag = [], False
    for i in range(Y):
        intermediate = []
        for j in range(X): 
         
            if randrange(300) in range(1) and flag == False: # 0.33% шанс что новый тайл будет "началом" водоема
                if 2 < i < Y - 12:
                    r_lenght, r_width, flag = randrange(2, 4), randrange(7, 14), True  # длина и ширина будущего водоема
                    r_lenght_2, loc_x, r_width_2 = r_lenght, randrange(13, X - 15), r_width 
         
            if flag and r_lenght_2 != 0 and intermediate.count(1) == loc_x:
                intermediate.append(0)
                r_lenght_2 -= 1
            
            elif len(intermediate) != X:
                intermediate.append(1)
            
        if flag:
            if r_width - r_width_2 in range(0, int(r_width / 2)):
                r_lenght, loc_x = r_lenght + randrange(choice([1, 2]), 4), loc_x - randrange(1, 3)
            elif r_width - r_width_2 in range(int(r_width / 2) + 1, r_width):
                r_lenght, loc_x = r_lenght - randrange(choice([1, 2]), 4), loc_x + randrange(1, 3)

            r_width_2, r_lenght_2 = r_width_2 - 1, r_lenght
            flag = False if r_width_2 == 0 else True  

        chunk.append(intermediate)

    if choice([True, False, False]):  # 33% водоем будт с песком
        for i in range(Y):  # окантовка водоемов "песком"
            for j in range(X):
                if i < Y - 1 and chunk[i][j] in [1, 3] and chunk[i + 1][j] == 0:
                    chunk[i][j] = 3
                    chunk[i - 1][j] = 3 if i < Y - 2 else 1
                    chunk[i][j - 1] = 3 if j != X - 2 else 1

                if i - 1 != 0 and chunk[i][j] in [1, 3] and chunk[i - 1][j] == 0:
                    chunk[i][j] = 3
                    if i - 2 > 0:
                        chunk[i + 1][j] = 3 
                    chunk[i][j - 1] = 3 if j - 2 > 0 else 1     

                if j < X - 1 and chunk[i][j] in [1, 3] and chunk[i][j + 1] == 0:
                    chunk[i][j] = 3
                    chunk[i][j - 1] = 3 if j < X - 2 else 1

                if j - 1 > 0 and chunk[i][j] in [1, 3] and chunk[i][j - 1] == 0:
                    chunk[i][j] = 3
                    chunk[i][j + 1] = 3 if j - 2 > 0 else 1

                if i != Y - 2 and j < X - 2 and chunk[i][j] == 0 and chunk[i + 1][j + 1] == 1:
                    chunk[i + 1][j + 1] = 3 
                if i - 2 != 0 and j < X - 2 and chunk[i][j] == 0 and chunk[i - 1][j + 1] == 1:
                    chunk[i - 1][j + 1] = 3
                
                         
    return chunk


def save():
    chunks_file = open("chunks.txt", "w")
    for elem in chunks:
        chunks_file.write(''.join(elem) + "\n")


if __name__ == "__main__":
    flag = False
    pygame.init()
    screen = pygame.display.set_mode((X * 25, Y * 25))
    last_x, last_y, x, y, w, h = -1, -1, 0, 0, 20, 10
    chunks_file = open("chunks.txt", "r")
    chunks = list(chunks_file.read())
    running = True
    clock = pygame.time.Clock()
    render(generate())
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #save()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    flag = True
        if flag:
            render(generate())
            flag = False