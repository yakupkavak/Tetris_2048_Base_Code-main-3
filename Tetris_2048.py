import numpy as np

import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types/shapes


# MAIN FUNCTION OF THE PROGRAM
# -------------------------------------------------------------------------------
# Main function where this program starts execution
def start():
    # set the dimensions of the game grid
    grid_h, grid_w = 20, 12
    # set the size of the drawing canvas
    canvas_h, canvas_w = 40 * grid_h, 40 * grid_w
    stddraw.setCanvasSize(canvas_w, canvas_h)
    # set the scale of the coordinate system
    stddraw.setXscale(-0.5, grid_w - 0.5)
    stddraw.setYscale(-0.5, grid_h - 0.5)

    # set the dimension values stored and used in the Tetromino class
    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w

    # create the game grid
    grid = GameGrid(grid_h, grid_w)
    # create the first tetromino to enter the game grid
    # by using the create_tetromino function defined below
    current_tetromino = create_tetromino(grid_h, grid_w)
    next_tetromino = create_tetromino(grid_h, grid_w)
    grid.current_tetromino = current_tetromino

    # display a simple menu before opening the game
    # by using the display_game_menu function defined below
    display_game_menu(grid_h, grid_w)

    # the main game loop (keyboard interaction for moving the tetromino)
    while True:
        # check user interactions via the keyboard
        if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
            key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
            # if the left arrow key has been pressed
            if key_typed == "left":
                # move the active tetromino left by one
                current_tetromino.move(key_typed, grid)
                # if the right arrow key has been pressed
            elif key_typed == "right":
                # move the active tetromino right by one
                current_tetromino.move(key_typed, grid)
            # if the down arrow key has been pressed
            elif key_typed == "down":
                # Perform hard drop of the active tetromino
                current_tetromino.hard_drop(grid)
                # Lock the tetromino onto the grid after hard drop


            # FOR ROTATE
            elif key_typed == "k":
                print("keybord k pressed");
                current_tetromino.rotate()

            elif key_typed == "p":
                print("keybord p pressed");
                pause(grid)



            # clear the queue of the pressed keys for a smoother interaction
            stddraw.clearKeysTyped()

        # move the active tetromino down by one at each iteration (auto fall)
        success = current_tetromino.move("down", grid)

        # place the active tetromino on the grid when it cannot go down anymore
        if not success:
            # get the tile matrix of the tetromino without empty rows and columns
            # and the position of the bottom left cell in this matrix
            tiles, pos = grid.current_tetromino.get_min_bounded_tile_matrix(True)
            # update the game grid by locking the tiles of the landed tetromino
            game_over = grid.update_grid(tiles, pos)
            # end the main game loop if the game is over

            if game_over:
                break
            # create the next tetromino to enter the game grid
            # by using the create_tetromino function defined below
            current_tetromino = next_tetromino
            next_tetromino = create_tetromino(grid_h, grid_w)

            grid.current_tetromino = current_tetromino

        cleared_lines = grid.clear_full_lines()  # <--- Clear full lines here

        # display the game grid and the current tetromino
        grid.display()

    # print a message on the console when the game is over
    print("Game over")

def game_cycle():
    game = Game()
    grid = GameGrid(20, 12)
    current_tetromino = create_tetromino(grid.grid_height, grid.grid_width)

    while not game.check_game_over(grid):
        success = current_tetromino.move("down", grid)
        if not success:
            tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
            game_over = grid.update_grid(tiles, pos)
            if game_over:
                game.set_game_over(True)
                break
            cleared_lines = grid.clear_full_lines()
            game.score.update_score(cleared_lines)
            current_tetromino = create_tetromino(grid.grid_height, grid.grid_width)
            grid.current_tetromino = current_tetromino

        grid.display()

    game.show_game_over_menu()



class Score:
    def __init__(self):
        self.score = 0

    def update_score(self, cleared_lines):
        # Calculate score based on the number of lines cleared
        if cleared_lines == 1:
            self.score += 40
        elif cleared_lines == 2:
            self.score += 100
        elif cleared_lines == 3:
            self.score += 300
        elif cleared_lines == 4:
            self.score += 1200

    def get_score(self):
        return self.score

    def reset_score(self):
        self.score = 0


class Game:
    def __init__(self):
        self.game_over = False
        self.score = Score()

    @staticmethod
    def check_game_over(grid):
        return grid.game_over

    def set_game_over(self, value):
        self.game_over = value

    def show_game_over_menu(self):
        print("Game Over! Your final score:", self.score.get_score())
        # You can add menu options for restarting or quitting the game here


# A method for clearing full lines in the game grid and updating the score
# A method for clearing full lines in the game grid and updating the score





def pause(grid):
    pause = True
    # the loop causes pause the game.
    while pause:
        # display the game grid and the current tetromino
        grid.display()

        # Check for user input
        if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
            # Check if the user presses the 'p' key to resume the game
            if key_typed == "p":
                pause = False


# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
    # type (shape) of the tetromino is determined randomly
    tetromino_types = ['I', 'J', 'L', 'O', 'S', 'Z', 'T']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    # create and return the tetromino
    tetromino = Tetromino(random_type)
    return tetromino


# Function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
    # colors used for the menu
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    # clear the background canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # path of the image file
    img_file = current_dir + "/images/menu_image.png"
    # center coordinates to display the image
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
    # image is represented using the Picture class
    image_to_display = Picture(img_file)
    # display the image
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # dimensions of the start game button
    button_w, button_h = grid_width - 1.5, 2
    # coordinates of the bottom left corner of the start game button
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # display the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "Click Here to Start the Game"
    stddraw.text(img_center_x, 5, text_to_display)
    # menu interaction loop
    while True:
        # display the menu and wait for a short time (50 ms)
        stddraw.show(50)
        # check if the mouse has been left-clicked on the button
        if stddraw.mousePressed():
            # get the x and y coordinates of the location at which the mouse has
            # most recently been left-clicked
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # check if these coordinates are inside the button
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    break  # break the loop to end the method and start the game


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    start()
