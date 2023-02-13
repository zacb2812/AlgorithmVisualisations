import os
import pygame
from queue import PriorityQueue
from tkinter import messagebox

WIDTH = 900
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Algorithm Visualisation")


BG = (200, 200, 200)
START = (0, 255, 0)
END = (255, 0, 0)
BARRIER = (0, 0, 0)
PATH = (0, 0, 255)
SEARCHED = (255, 255, 0)
UNSEARCHED = (255, 165, 0)
LINES = (0, 0, 0)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = BG
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col

    def is_searched(self):
        return self.color == SEARCHED

    def is_unsearched(self):
        return self.color == UNSEARCHED

    def is_barrier(self):
        return self.color == BARRIER

    def is_start(self):
        return self.color == START

    def is_end(self):
        return self.color == END

    def reset(self):
        self.color = BG

    def make_searched(self):
        self.color = SEARCHED

    def make_unsearched(self):
        self.color = UNSEARCHED

    def make_barrier(self):
        self.color = BARRIER

    def make_start(self):
        self.color = START

    def make_end(self):
        self.color = END

    def make_path(self):
        self.color = PATH

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        # check node below
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbours.append(grid[self.row+1][self.col])

        # check node above
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbours.append(grid[self.row-1][self.col])

        # check node right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbours.append(grid[self.row][self.col+1])

        # check node left
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbours.append(grid[self.row][self.col-1])


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)


def construct_path(came_from, curr_node, draw):
    count = 0
    while curr_node in came_from:
        count += 1
        curr_node = came_from[curr_node]
        curr_node.make_path()
        draw()
    return count


def algorithm(draw, grid, start_node, end_node):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start_node))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start_node] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start_node] = h(start_node.get_position(), end_node.get_position())

    open_set_hash = {start_node}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os.system("python Python\Algorithms\menu.py")

        curr_node = open_set.get()[2]
        open_set_hash.remove(curr_node)

        if curr_node == end_node:
            path_count = construct_path(came_from, end_node, draw)
            end_node.make_end()
            start_node.make_start()
            messagebox.showinfo("", f"Path length: {path_count} blocks")
            return True

        for neighbour in curr_node.neighbours:
            temp_g_score = g_score[curr_node] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = curr_node
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_position(), end_node.get_position())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_unsearched()

        draw()

        if curr_node != start_node:
            curr_node.make_searched()

    return False


def make_grid(rows, width):
    grid = []
    node_width = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, node_width, rows)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    node_width = width // rows
    for i in range(rows):
        pygame.draw.line(win, LINES, (0, i*node_width), (width, i*node_width))
        for j in range(rows):
            pygame.draw.line(win, LINES, (j*node_width, 0), (j*node_width, width))


def draw(win, grid, rows, width):
    win.fill(BG)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_mouse_pos(pos, rows, width):
    node_width = width // rows
    x, y = pos

    row = x // node_width
    col = y // node_width

    return row, col


def main(win, width):
    run = True

    ROWS = 75
    grid = make_grid(ROWS, width)

    start_node = None
    end_node = None

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # left mouse click
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
                curr_node = grid[row][col]
                if not start_node and curr_node != end_node:
                    start_node = curr_node
                    start_node.make_start()
                elif not end_node and curr_node != start_node:
                    end_node = curr_node
                    end_node.make_end()
                elif curr_node != start_node and curr_node != end_node:
                    curr_node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # right mouse click
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
                curr_node = grid[row][col]
                curr_node.reset()
                if curr_node == start_node:
                    start_node = None
                elif curr_node == end_node:
                    end_node = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_node and end_node:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start_node, end_node)

                if event.key == pygame.K_c:
                    start_node = None
                    end_node = None
                    grid = make_grid(ROWS, width)

    pygame.quit()
    os.system("python Python\Algorithms\AlgorithmVisualisations\menu.py")


if __name__ == "__main__":
    try:
        main(WIN, WIDTH)
    except Exception as e:
        if str(e) == "display Surface quit":  # handle exception thrown when window is closed during search
            pass
        elif str(e) == "video system not initialized":  # handle irrelevant error
            pass
        else:
            print(e)
