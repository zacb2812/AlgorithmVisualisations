import os
import pygame
import random
import math
pygame.init()


class VisualInfo:
    BG = (200, 200, 200)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    GRADIENTS = [
        (98, 98, 98),
        (64, 64, 64),
        (32, 32, 32)
    ]

    FONT = pygame.font.SysFont("None", 30)
    SMALL_FONT = pygame.font.SysFont("None", 20)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bubble Sort Visualisation")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.bar_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.bar_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_draw = self.SIDE_PAD // 2


def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst


def draw(vis_info, ascending):
    vis_info.window.fill(vis_info.BG)

    controls = vis_info.FONT.render("R - Reset | SPACE - Sort | A - Ascending | D - Descending", 1, vis_info.BLACK)
    vis_info.window.blit(controls, ((vis_info.width - controls.get_width())/2, 35))

    curr_order = vis_info.SMALL_FONT.render(f"{'Currently Ascending' if ascending else 'Currently Descending'}", 1, vis_info.BLACK)
    vis_info.window.blit(curr_order, ((vis_info.width - curr_order.get_width())/2, 75))

    draw_list(vis_info)
    pygame.display.update()


def draw_list(vis_info, color_positions={}, clear_bg=False):
    lst = vis_info.lst

    if clear_bg:
        clear_rect = (vis_info.SIDE_PAD//2, vis_info.TOP_PAD, vis_info.width-vis_info.SIDE_PAD, vis_info.height-vis_info.TOP_PAD)
        pygame.draw.rect(vis_info.window, vis_info.BG, clear_rect)

    for i, val in enumerate(lst):
        x = vis_info.start_draw + (vis_info.bar_width * i)
        y = vis_info.height - (val - vis_info.min_val) * vis_info.bar_height

        color = vis_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(vis_info.window, color, (x, y, vis_info.bar_width, vis_info.height))

    if clear_bg:
        pygame.display.update()


def bubble_sort(vis_info, ascending):
    lst = vis_info.lst

    for i in range(len(lst)):
        for j in range(0, len(lst)-i-1):
            if (lst[j] > lst[j+1] and ascending) or (lst[j] < lst[j+1] and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(vis_info, {j: vis_info.GREEN, j+1: vis_info.RED}, True)
                yield True

    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    sorting = False
    ascending = True

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)

    vis_info = VisualInfo(800, 600, lst)

    algorithm_generator = None

    while run:
        clock.tick(120)

        if sorting:
            try:
                next(algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(vis_info, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    lst = generate_starting_list(n, min_val, max_val)
                    vis_info.set_list(lst)
                    sorting = False
                elif event.key == pygame.K_SPACE and not sorting:
                    sorting = True
                    algorithm_generator = bubble_sort(vis_info, ascending)
                elif event.key == pygame.K_a and not sorting:
                    ascending = True
                elif event.key == pygame.K_d and not sorting:
                    ascending = False

    pygame.quit()
    os.system("python Python\Algorithms\AlgorithmVisualisations\menu.py")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if str(e) == "display Surface quit":  # handle exception thrown when window is closed during search
            pass
        elif str(e) == "video system not initialized":  # handle irrelevant error
            pass
        else:
            print(e)
