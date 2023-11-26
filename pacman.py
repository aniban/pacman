import time
import random
import pygame

pygame.init()
pygame.display.set_caption('Ani\'s Pac Man')
Icon = pygame.image.load('./pic/pm_0a.png')
pygame.display.set_icon(Icon)
       
mp2 = [
'                            ',
' xxxxxxxxxxxx  xxxxxxxxxxxx ',
' x    x     x  x     x    x ',
' x    x     x  x     x    x ',
' x    x     x  x     x    x ',
' xxxxxxxxxxxxxxxxxxxxxxxxxx ',
' x    x  x        x  x    x ',
' x    x  x        x  x    x ',
' xxxxxx  xxxx  xxxx  xxxxxx ',
'      x     x  x     x      ',
'      x     x  x     x      ',
'      x  xxxxxxxxxx  x      ',
'      x  x   xx   x  x      ',
' xxxxxxxxx   xx   xxxxxxxxx ',
'      x  x        x  x      ',
'      x  xxxxxxxxxx  x      ',
'      x  x        x  x      ',
'      x  x        x  x      ',
' xxxxxxxxxxxx  xxxxxxxxxxxx ',
' x    x     x  x     x    x ',
' x    x     x  x     x    x ',
' xxx  xxxxxxxxxxxxxxxx  xxx ',
'   x  x  x        x  x  x   ',
'   x  x  x        x  x  x   ',
' xxxxxx  xxxx  xxxx  xxxxxx ',
' x          x  x          x ',
' x          x  x          x ',
' xxxxxxxxxxxxxxxxxxxxxxxxxx ',
'                            ']

ROWS = len(mp2)
COLS = len(mp2[0])
SCRW = 900
SCRH = 1000
TOP = 100
CELW = int(SCRW/COLS)
CELH = int((SCRH-TOP)/ROWS)


class cell():
    def __init__(self, row, col, path):
        self.row = row
        self.col = col
        self.path = path
        if path:
            self.dot = True
        self.xlo = int(col*CELW)
        self.ylo = int(TOP+row*CELH)
        #self.x = int((col+0.5)*CELW)
        #self.y = int(TOP+(row+0.5)*CELH)


# DEFINE GRID & PATH OF CELLS -----------------
grid = [list(wrd) for wrd in mp2]
path_list = []

def initialize_grid():
    for r in range(ROWS):
        
        for c in range(COLS):
            is_path = (mp2[r][c]=='x')
            grid[r][c] = cell(r,c, is_path)
            if is_path:
                path_list.append(grid[r][c])

initialize_grid()

# DRAW SCREEN AND TILES-------------------------------
screen = pygame.display.set_mode([SCRW,SCRH])
screen.fill((20,40,20))   
path_colour = (0,0,0)
surf_path_dot = pygame.Surface((CELW,CELH))
surf_path_dot.fill(path_colour)
pygame.draw.circle(surf_path_dot,(255,255,0), (int(CELW/2),int(CELH/2)), int(CELH/10))
surf_path_clear = pygame.Surface((CELW,CELH))
surf_path_clear.fill(path_colour)
costume_eyes = pygame.Surface((CELW,CELH))
costume_eyes.fill(path_colour)
file_n = './pic/ghost_eyes.png'
img = pygame.image.load(file_n)
img = pygame.transform.scale(img, (CELW,CELH))
costume_eyes.blit(img,(0,0))
# text setting
font_obj = pygame.font.Font('freesansbold.ttf', 32)



class ghost():
    def __init__(self, row, col, type=1):
        self.row = row
        self.col = col
        self.type = type
        self.dirn = 0               # 0:right, 1:up, 2:left, 3:down
        self.dead = False
        self.costumes = []
        for dirn in range(4):       # define 4 costumes of ghost
            surf_ = pygame.Surface((CELW,CELH))
            surf_.fill(path_colour)
            file_n = './pic/ghost'+str(type)+'_'+str(dirn)+'.png'
            img = pygame.image.load(file_n)
            img = pygame.transform.scale(img, (CELW,CELH))
            surf_.blit(img,(0,0))
            self.costumes.append(surf_)
     
    def move(self):
        possible_dirn = [self.dirn, (self.dirn +1)%4, (self.dirn +3)%4]
        possible_moves = []         # (delta row, delta col, dirn)
        if 0 in possible_dirn:          #go right
            if self.col < COLS-1:
                if grid[self.row][self.col+1].path:
                    possible_moves.append((0,1,0))
        if 1 in possible_dirn:          #go up
            if self.row > 0:
                if grid[self.row-1][self.col].path:
                    possible_moves.append((-1,0,1))
        if 2 in possible_dirn:           #go left
            if self.col > 0:
                if grid[self.row][self.col-1].path:
                    possible_moves.append((0,-1,2))
        if 3 in possible_dirn:           #go down
            if self.row < ROWS-1:
                if grid[self.row+1][self.col].path:
                    possible_moves.append((1,0,3))
        if len(possible_moves) == 0:     # DEAD-END!
            if self.col == 1:
                self.col = 26
            else:
                self.col = 1
        else:
            chosen_move = random.choice(possible_moves)
            self.row += chosen_move[0]
            self.col += chosen_move[1]
            self.dirn = chosen_move[2]

    def chase(self, t_row, t_col):
        possible_dirn = [self.dirn, (self.dirn +1)%4, (self.dirn +3)%4]
        possible_next_pos = []      # (delta row, delta col, dirn, delta from target)
        if 3 in possible_dirn:           #go down
            if self.row < ROWS-1:
                if grid[self.row +1][self.col].path:
                    if t_row > self.row:
                        possible_next_pos.append((1,0,3,-1))
                    elif t_row < self.row:
                        possible_next_pos.append((1,0,3,+1))
                    else:
                        possible_next_pos.append((1,0,3,+1))
        if 1 in possible_dirn:          #go up
            if self.row > 0:
                if grid[self.row -1][self.col].path:
                    if t_row > self.row:
                        possible_next_pos.append((-1,0,1,+1))
                    elif t_row < self.row:
                        possible_next_pos.append((-1,0,1,-1))
                    else:
                        possible_next_pos.append((-1,0,1,+1))
        if 0 in possible_dirn:          #go right
            if self.col < COLS-1:
                if grid[self.row][self.col+1].path:
                    if t_col > self.col:
                        possible_next_pos.append((0,1,0,-1))
                    elif t_col < self.col:
                        possible_next_pos.append((0,1,0,+1))
                    else:
                        possible_next_pos.append((0,1,0,+1))
        if 2 in possible_dirn:           #go left
            if self.col > 0:
                if grid[self.row][self.col-1].path:
                    if t_col > self.col:
                        possible_next_pos.append((0,-1,2,+1))
                    elif t_col < self.col:
                        possible_next_pos.append((0,-1,2,-1))
                    else:
                        possible_next_pos.append((0,-1,2,+1))
        if t_row == self.row and t_col == self.col:
            possible_next_pos.append((0,0,1,0))
        if len(possible_next_pos) == 0:     # DEAD-END!
            if self.col == 1:
                self.col = 26
            else:
                self.col = 1
        else:
            next_pos = min(possible_next_pos, key=lambda possible_next_pos: possible_next_pos[3])
            self.row += next_pos[0]
            self.col += next_pos[1]
            self.dirn = next_pos[2]
        
        
        
class player():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.dirn = 3   # 0:right, 1:up, 2:left, 3:down
        self.turn = 3   # based on key pressed
        self.costumes = [[],[],[],[]]
        for dirn in range(4):          # define 8 costumes of player
            for c in ['a','b']:
                surf_ = pygame.Surface((CELW,CELH))
                surf_.fill(path_colour)
                file_n = './pic/pm_'+str(dirn)+c+'.png'
                img = pygame.image.load(file_n)
                img = pygame.transform.scale(img, (CELW,CELH))
                surf_.blit(img,(0,0))
                self.costumes[dirn].append(surf_)
        
    def set_dirn(self):
        if self.turn != self.dirn:
            if self.turn == 0:                          #turn right
                if self.col < COLS-1:
                    if grid[self.row][self.col+1].path:
                        self.dirn = 0
            elif self.turn == 1:                        #turn up
                if self.row > 0:
                    if grid[self.row-1][self.col].path:
                        self.dirn = 1
            elif self.turn == 2:                        #turn left
                if self.col > 0:
                    if grid[self.row][self.col-1].path:
                        self.dirn = 2
            else:                                       #turn down
                if self.row < ROWS-1:
                    if grid[self.row+1][self.col].path:
                        self.dirn = 3
    
    def move(self):
        if self.row == 13: # DEAD-END
            if self.col == 1:
                self.col = 26
            elif self.col == 26:
                self.col =1
                
        if self.dirn == 0:           #go right
            if self.col < COLS-1:
                if grid[self.row][self.col+1].path:
                    self.col += 1
        elif self.dirn == 1:         #go up
            if self.row > 0:
                if grid[self.row-1][self.col].path:
                    self.row -= 1
        elif self.dirn == 2:         #go left
            if self.col > 0:
                if grid[self.row][self.col-1].path:
                    self.col -= 1
        else:                        #go down
            if self.row < ROWS-1:
                if grid[self.row+1][self.col].path:
                    self.row += 1
 
start = random.choice(path_list)
p = player(start.row,start.col)
def initialize_ghosts():
    global steps, GHOSTS, ghosts_dead, gst, p
    GHOSTS = 5
    ghosts_dead = 0
    gst = []
    for _ in range (GHOSTS):
        gst.append(ghost(13,13,_%3+1))
    steps = 0
    return

def end_game():
    file_n = './pic/game_over.png'
    img = pygame.image.load(file_n)
    for size in range(100,700,10):
        game_over = pygame.Surface((size,size))
        game_over.fill(path_colour)
        img = pygame.transform.scale(img, (size,size))
        game_over.blit(img,(0,0))
        rect_obj = game_over.get_rect()
        rect_obj.center = (int(SCRW/2), int(SCRH/2))
        screen.blit(game_over,rect_obj)
        pygame.display.flip()
        #time.sleep(0.05)
    return()

initialize_ghosts()
running = True
while running:
    steps += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                p.turn = 1
            elif event.key == pygame.K_DOWN:
                p.turn = 3
            elif event.key == pygame.K_LEFT:
                p.turn = 2
            elif event.key == pygame.K_RIGHT:
                p.turn = 0
            elif event.key == pygame.K_SPACE:
                initialize_ghosts()
    
    for c in path_list:
        if c.dot:
            screen.blit(surf_path_dot,(c.xlo,c.ylo))
        else:
            screen.blit(surf_path_clear,(c.xlo,c.ylo))
    
    screen.blit(p.costumes[p.dirn][steps%2],(grid[p.row][p.col].xlo,grid[p.row][p.col].ylo))
    
    for _ in range(GHOSTS):
        g = gst[_]
        if g.dead:
            screen.blit(costume_eyes,(grid[g.row][g.col].xlo,grid[g.row][g.col].ylo))
        else:
            screen.blit(g.costumes[g.dirn],(grid[g.row][g.col].xlo,grid[g.row][g.col].ylo))
    
    text_surface_obj = font_obj.render('Current step : '+str(steps), True, (0,255,0), (20,40,20))
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (int(SCRW/2), 50)
    screen.blit(text_surface_obj, text_rect_obj)
    
    pygame.display.flip()
    
    grid[p.row][p.col].dot = False   
    p.set_dirn()
    p.move()
    for _ in range(GHOSTS):
        g = gst[_]
        if g.dead:
            g.chase(14,13)
        else:
            g.move()  
            #if steps%3 != 0: 
                #g.chase(p.row,p.col)  
            if g.row == p.row and g.col == p.col:
                g.dead = True
                ghosts_dead += 1
                if ghosts_dead == GHOSTS:
                    end_game()
                    running = False
    time.sleep(0.15)    

        
pygame.quit()






