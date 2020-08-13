
try:
    import pygame
    import sys
    import math
    import random
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    import os
    from cell import Cell
    from data import fixed_maze, fixed_weights
except:
    import install_requirements  # install packages

    import pygame
    import sys
    import math
    import random
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    import os
    from cell import Cell
    from data import fixed_maze, fixed_weights

screen = pygame.display.set_mode((800, 800))
screen.fill((255, 255, 255))



cols = 50
grid = [0 for i in range(cols)]
row = 50
openSet = []
closedSet = []
purple = (128,0,128)
teal = (173,216,230)
blue = (0, 0, 255)
black = (0, 0, 0)
w = 800 / cols
h = 800 / row
cameFrom = []
weight_colors = [ [(0,0,0), 1], [(220,220,220), 0], [(180,180,180), 0] ]

# create 2d array
for i in range(cols):
    grid[i] = [0 for i in range(row)]

# Create Spots
for i in range(cols):
    for j in range(row):
        grid[i][j] = Cell(pygame, screen, w, h, row, cols, i, j)


# Set start and end node
start = grid[12][5]
end = grid[3][6]

#Algorithm choice
option = 'A*'

#heuristic choice
h_option = 'Euclidean'

#initial layout choice
m_option = 'Blank'

#weights
w_option = 'All Weights 1'

# SHOW RECT
for i in range(cols):
    for j in range(row):
        grid[i][j].show((0, 0, 0), 1)

for i in range(0,row):
    grid[0][i].show(black, 0)
    grid[0][i].obs = True
    grid[cols-1][i].obs = True
    grid[cols-1][i].show(black, 0)
    grid[i][row-1].show(black, 0)
    grid[i][0].show(black, 0)
    grid[i][0].obs = True
    grid[i][row-1].obs = True

def onsubmit():
    global start
    global end
    st = startBox.get().split(',')
    ed = endBox.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    window.quit()
    window.destroy()

window = Tk()
label = Label(window, text='Start (x,y) : ')
startBox = Entry(window)
label1 = Label(window, text='End (x,y) : ')
endBox = Entry(window)
var = IntVar()
showPath = ttk.Checkbutton(window, text='Show Steps :', onvalue=1, offvalue=0, variable=var)
tkvar = StringVar(window)
tkvar1 = StringVar(window)
tkvar2 = StringVar(window)
tkvar3 = StringVar(window)

# List with options
choices = [ 'A*','Dijkstra','DFS','BFS' ]
h_choices = [ 'Euclidean', 'Manhattan', 'Diagonal' ]
m_choices = [ 'Blank', 'Fixed Maze', 'Random' ]
w_choices = [ 'All Weights 1', 'Fixed Weights', 'Random Weights' ]

tkvar.set('A*') # set the default option
tkvar1.set('Euclidean')
tkvar2.set('Blank')
tkvar3.set('All Weights 1')
# on change dropdown value
def change_heuristic(*args):
    global h_option
    h_option = tkvar1.get()
    print( h_option )

hMenu = OptionMenu(window, tkvar1, *h_choices, command=change_heuristic)

def change_weight(*args):
    global w_option
    w_option = tkvar3.get()
    print( w_option )

wMenu = OptionMenu(window, tkvar3, *w_choices, command=change_weight)

def change_dropdown(*args):
    global option
    option = tkvar.get()
    print( option )
    if option != 'A*':
        hMenu.configure(state='disabled')
        if option != 'Dijkstra':
            wMenu.configure(state='disabled')
        else:
            wMenu.configure(state='normal')
    else:
        hMenu.configure(state='normal')
        wMenu.configure(state='normal')

popupMenu = OptionMenu(window, tkvar, *choices, command=change_dropdown)

def change_layout(*args):
    global m_option
    m_option = tkvar2.get()
    print( m_option )

mMenu = OptionMenu(window, tkvar2, *m_choices, command=change_layout)

submit = Button(window, text='Submit', command=onsubmit)

label1.grid(row=1, pady=3)
endBox.grid(row=1, column=1, pady=3)
startBox.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=3)
Label(window, text="Algorithm:").grid(row=2, pady=3, padx=3)
popupMenu.grid(row=2, column=1, pady=3)
Label(window, text="Weight:").grid(row=3, pady=3, padx=3)
wMenu.grid(row=3, column=1, pady=3)
Label(window, text="Heuristic:").grid(row=4, pady=3, padx=3)
hMenu.grid(row=4, column=1, pady=3)
Label(window, text="Starting Layout:").grid(row=5, pady=3, padx=3)
mMenu.grid(row=5, column=1, pady=3)
Label(window, text="1 ≤ x ≤ 48 and 1 ≤ y ≤ 48").grid(row=6, column=0, pady=3, padx=25)
Label(window, text="Use cursor to draw walls.").grid(row=7, column=0, pady=3, padx=25)
Label(window, text="Press 'SPACE' to start.").grid(row=8, column=0, pady=3, padx=25)
showPath.grid(columnspan=2, row=9, pady=3)
submit.grid(columnspan=2, row=10)

window.update()
mainloop()

pygame.init()
openSet.append(start)

if m_option == 'Random':
    for i in range(1,cols-1):
        for j in range(1,row-1):
            if random.choice([1, 2, 3, 4]) == 2 and grid[i][j]!=start and grid[i][j]!=end :
                grid[i][j].obs = True
                grid[i][j].show(black, 0)
elif m_option == 'Fixed Maze':
    for i in range(1,cols-1):
        for j in range(1,row-1):
            if fixed_maze[j][i] and grid[i][j]!=start and grid[i][j]!=end :
                grid[i][j].obs = True
                grid[i][j].show(black, 0)

if option != 'BFS' and option != 'DFS':
    if w_option == 'Random Weights':
        for i in range(1,cols-1):
            for j in range(1,row-1):
                if grid[i][j]!=start and grid[i][j]!=end and grid[i][j].obs==False :
                    weight = random.choice([0,0,0,1,2])
                    grid[i][j].value =  weight+1
                    grid[i][j].show(weight_colors[weight][0], weight_colors[weight][1])
    elif w_option == 'Fixed Weights':
        for i in range(1,cols-1):
            for j in range(1,row-1):
                if grid[i][j]!=start and grid[i][j]!=end and grid[i][j].obs==False:
                    weight = fixed_weights[j][i]-1
                    grid[i][j].value =  weight+1
                    grid[i][j].show(weight_colors[weight][0], weight_colors[weight][1])

def mousePress(x):
    t = x[0]
    w = x[1]
    g1 = t // (800 // cols)
    g2 = w // (800 // row)
    acess = grid[g1][g2]
    if acess != start and acess != end:
        if acess.obs == False:
            acess.obs = True
            acess.show(black, 0)

end.show((255, 50, 50), 0)
start.show((50, 255, 50), 0)

loop = True
while loop:
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
                break

for i in range(cols):
    for j in range(row):
        grid[i][j].addNeighbors(grid)

def heurisitic(n, e):
    if h_option == 'Euclidean':
        d = math.sqrt((n.i - e.i)**2 + (n.j - e.j)**2)
    elif h_option == 'Manhattan':
        d = abs(n.i - e.i) + abs(n.j - e.j)
    elif h_option == 'Diagonal':
        d = max([abs(n.i - e.i), abs(n.j - e.j)])
    return d

def a_star():
    end.show((255, 50, 50), 0)
    start.show((50, 255, 50), 0)
    while len(openSet) > 0:
        lowestIndex = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowestIndex].f:
                lowestIndex = i

        current = openSet[lowestIndex]
        if current == end:
            print('done', current.f)
            start.show((50, 255, 50),0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.show((0,0,255), 0)
                current = current.previous
            end.show((255, 50, 50), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', ('The program finished, the shortest distance/least weighted path \n is ' + str(temp) + '\n would you like to re run the program?'))
            if result == True:
                os.execl(sys.executable,sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()

        openSet.pop(lowestIndex)
        closedSet.append(current)

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            if neighbor not in closedSet:
                tempG = current.g + current.value
                if neighbor in openSet:
                    if neighbor.g > tempG:
                        neighbor.g = tempG
                else:
                    neighbor.g = tempG
                    openSet.append(neighbor)
                    if var.get():
                        neighbor.show(teal,0)

            neighbor.h = heurisitic(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h

            if neighbor.previous == None:
                neighbor.previous = current
        
        if var.get() and current != start:
            current.show(purple,0)
        current.closed = True

def dijkstra():
    end.show((255, 50, 50), 0)
    start.show((50, 255, 50), 0)
    while len(openSet) > 0:
        lowestIndex = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowestIndex].f:
                lowestIndex = i

        current = openSet[lowestIndex]
        if current == end:
            print('done', current.f)
            start.show((50, 255, 50),0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.show((0,0,255), 0)
                current = current.previous
            end.show((255, 50, 50), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', ('The program finished, the shortest distance/least weighted path \n is ' + str(temp) + '\n would you like to re run the program?'))
            if result == True:
                os.execl(sys.executable,sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()
            break
        
        openSet.pop(lowestIndex)
        closedSet.append(current)

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            if neighbor not in closedSet:
                tempG = current.g + current.value
                if neighbor in openSet:
                    if neighbor.g > tempG:
                        neighbor.g = tempG
                else:
                    neighbor.g = tempG
                    openSet.append(neighbor)
                    if var.get():
                        neighbor.show(teal,0)

            neighbor.f = neighbor.g

            if neighbor.previous == None:
                neighbor.previous = current

        if var.get() and current != start:
            current.show(purple,0)
        current.closed = True

def dfs():
    end.show((255, 50, 50), 0)
    start.show((50, 255, 50), 0)
    while len(openSet) > 0:
        current = openSet.pop(-1)
        if current == end:
            print('done', current.f)
            start.show((50, 255, 50),0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.show((0,0,255), 0)
                current = current.previous
            end.show((255, 50, 50), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', ('The program finished, the shortest distance \n to the path is ' + str(temp) + ' blocks away, \n would you like to re run the program?'))
            if result == True:
                os.execl(sys.executable,sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()
            break

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            if not neighbors[i] in closedSet:
                openSet.append(neighbors[i])
                neighbors[i].previous = current
                neighbors[i].f = current.f + 1
                if var.get():
                    neighbors[i].show(teal,0)

        closedSet.append(current)
        if var.get() and current != start:
            current.show(purple,0)        
        
        current.closed = True

def bfs():
    end.show((255, 50, 50), 0)
    start.show((50, 255, 50), 0)
    current = start
    current.closed = True
    closedSet.append(current)
    while len(openSet) > 0:
        current = openSet.pop(0)
        if var.get() and current != start:
            current.closed = False
            current.show(purple,0) 
            current.closed = True

        if current == end:
            print('done', current.f)
            start.show((50, 255, 50),0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.show((0,0,255), 0)
                current = current.previous
            end.show((255, 50, 50), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', ('The program finished, the shortest distance \n to the path is ' + str(temp) + ' blocks away, \n would you like to re run the program?'))
            if result == True:
                os.execl(sys.executable,sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()
            break

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            if not neighbors[i] in closedSet:
                openSet.append(neighbors[i])
                neighbors[i].previous = current
                neighbors[i].f = current.f + 1
                if var.get():
                    neighbors[i].show(teal,0)
                neighbors[i].closed = True
                closedSet.append(neighbors[i])       
        

def main():
    print( option )
    print( m_option )
    if option == 'A*':
        print( h_option )
        a_star()
    elif option == 'Dijkstra':
        dijkstra()
    elif option == 'DFS':
        dfs()
    elif option == 'BFS':
        bfs()

while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    main()

