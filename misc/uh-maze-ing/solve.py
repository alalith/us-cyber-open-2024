from pwn import *

def grid(maze):
    ''' Maze Properties'''
    num_rows = len(maze)
    num_cols = len(maze[0])
    end_pt = (maze[num_rows-1].index(b' '),num_rows-1)
    print(maze[0])
    start_pt = (maze[0].index(b' '), 0)
    #print(start_pt)
    #print(end_pt)

    '''BFS'''
    visited = {end_pt: None}
    queue = [end_pt]
    while queue:
        #print(queue)
        current = queue.pop(0)
        if current == start_pt:
            #print(start_pt)
            shortest_path = []
            while current:
                shortest_path.append(str(current))
                current_col, current_row = current
                get_row = list(maze[current_row])
                get_row[current_col] = 0x2e
                maze[current_row] = bytes(get_row)
                current = visited[current]

            for i in maze:
                print(i)
            return shortest_path
        adj_points = []
        '''FIND ADJACENT POINTS'''
        current_col, current_row = current
        #UP
        if current_row > 0:
            #print(current_row)
            if maze[current_row - 1][current_col] == 0x20:
                adj_points.append((current_col, current_row - 1))
        #RIGHT
        if current_col < (len(maze[0])-1):
            if maze[current_row][current_col + 1] == 0x20: ## There was an error here!
                adj_points.append((current_col + 1,current_row))
        #DOWN
        if current_row < (len(maze) - 1):
            if maze[current_row + 1][current_col] == 0x20:
                adj_points.append((current_col, current_row + 1))
        #LEFT
        if current_col > 0:
            if maze[current_row][current_col - 1] == 0x20:
                adj_points.append((current_col - 1, current_row))

        '''LOOP THROUGH ADJACENT PTS'''
        for point in adj_points:
            if point not in visited:
                visited[point] = current
                queue.append(point)

r = remote('0.cloud.chals.io', 12743)

r.recvuntil('Here we go...\n\n\n')
for x in range(0,100):
    maze = []
    for i in range(0,29):
        row = r.recvline().rstrip()
        #print(row.decode())
        row = row.replace(b'\xe2\x96\x88', b'|')
        maze.append(row)


    for i in maze:
        print(i)
    solve = ','.join(grid(maze))
    solve = solve.replace(' ','')
    #print(solve)
    r.sendline(solve.encode())
    r.recvline()
    r.recvuntil('> ')
r.interactive()
