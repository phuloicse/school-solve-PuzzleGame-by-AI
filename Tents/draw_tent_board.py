import enum
from PIL import Image, ImageDraw, ImageFont,ImageEnhance
import os
import random
# from Tents.tents_and_tree import calculate_key
from draw_utils import generate_number_text_image, get_num_path,get_tree_img_path, get_tent_img_path
from tents_classes import BoardNode, TreeNode,ConstraintNode,PositionNode, TentNode, calculate_key
from tents_solver import Tents
def draw_grid(grid_tuple,cell_size,result_file_name="result.png"):
    width,height = grid_tuple

    image = Image.new('RGB', (width * cell_size,height * cell_size))

    draw_image = ImageDraw.Draw(image)
    tree_im = Image.open(get_tree_img_path())
    tent_im = Image.open(get_tent_img_path())


    tree_list = [(2,4),(2,2)]
    tent_list = [(1,1),(3,4)]
    for col in range(width):
        for row in range(height):
            rectangle_x = row*cell_size
            rectangle_y = col*cell_size

            rectangle_shape = [
                (rectangle_x, rectangle_y),
                (rectangle_x + cell_size, rectangle_y + cell_size)]

            draw_image.rectangle(
                rectangle_shape,
                fill=(60, 60, 60, 128),
                outline=(255, 60, 60, 128)
            )

            if (col,row) in tree_list:
                draw_image.rectangle(
                    rectangle_shape,
                    fill=(60, 255, 60, 128),
                    outline=(255, 60, 60, 128)
                )

            if (col,row) in tent_list:
                draw_image.rectangle(
                    rectangle_shape,
                    fill=(255, 255, 60, 128),
                    outline=(255, 60, 60, 128)
                )

    image.save(result_file_name)

    result_im = Image.open(result_file_name).convert("RGB")

    tree_fg = tree_im.resize((cell_size,cell_size))
    tent_fg = tent_im.resize((cell_size,cell_size)).convert("RGBA")
    result_im.paste(tree_fg, box=(cell_size,0), mask=tree_fg)
    result_im.paste(tent_fg, box=(cell_size,cell_size), mask=tent_fg)

    result_im.save(result_file_name)
    result_im.show()

NORMAL_CELL_COLOR = (60, 60, 60, 128)
POSSIBLE_CELL_COLOR = (10, 160, 60, 128)
IMPOSSIBLE_CELL_COLOR = (255, 100, 60, 128)
BORDER_COLOR = (255, 60, 60, 128)
def draw_tents_board(board: BoardNode, cell_size = 100, result_file_name="board.png", draw_current_contstraints= False, auto_output_path = None):
    grid = board.grid
    # Draw the initial constrain instead of current (Which is ZEROES for a solution board)
    initial_constraints = board.constraint_set 
    current_constraints = board.constraint_dict
    width = board.width + 1
    height = board.height + 1
    image = Image.new('RGB', (width * cell_size,height * cell_size))
    generate_number_text_image(size=cell_size)

    draw_image = ImageDraw.Draw(image)
    # Get the tent and tree image then resize
    tree_im = Image.open(get_tree_img_path())
    tent_im = Image.open(get_tent_img_path())
    tree_fg = tree_im.resize((cell_size,cell_size))
    tent_fg = tent_im.resize((cell_size,cell_size)).convert("RGBA")

    for pos in grid.values():
        row = pos.row_index
        col = pos.col_index
        rectangle_x = row*cell_size
        rectangle_y = col*cell_size
        rectangle_shape = [
            (rectangle_x, rectangle_y),
            (rectangle_x + cell_size, rectangle_y + cell_size)]

        # Fill the cell with background color
        draw_image.rectangle(
                rectangle_shape,
                fill=NORMAL_CELL_COLOR,
                outline=BORDER_COLOR
            )


    for pos in board.possible_locations.values():
        row = pos.row_index
        col = pos.col_index
        rectangle_x = col*cell_size
        rectangle_y = row*cell_size
        rectangle_shape = [
            (rectangle_x, rectangle_y),
            (rectangle_x + cell_size, rectangle_y + cell_size)]

        # Fill the cell with background color
        draw_image.rectangle(
                rectangle_shape,
                fill=POSSIBLE_CELL_COLOR,
                outline=BORDER_COLOR
            )

    output_path = os.path.join(os.curdir,"output",f"test/{result_file_name}")
    if auto_output_path:
        output_path = auto_output_path
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)

    # Reopen temp image to paste overlays
    result_im = Image.open(output_path).convert("RGB")
    # Overlay the images
    for pos in grid.values():
        row = pos.row_index
        col = pos.col_index
        box_to_paste = (col * cell_size, row * cell_size)
        if isinstance(pos, TreeNode):
            result_im.paste(tree_fg, box=box_to_paste, mask=tree_fg)
        elif isinstance(pos, TentNode):
            result_im.paste(tent_fg, box=box_to_paste, mask=tent_fg)
    # Overlay the constraints
    if draw_current_contstraints == True: 
        for pos in current_constraints.values():
            row = pos.row_index
            col = pos.col_index
            box_to_paste = (col * cell_size, row * cell_size)
            value = pos.tents_number_required
            text_img = Image.open(get_num_path(value))
            text_fg = text_img.resize((cell_size,cell_size)).convert("RGBA")
            result_im.paste(text_fg, box=box_to_paste, mask=text_fg)
    else: 
        for pos in initial_constraints:
            row = pos.row_index
            col = pos.col_index
            box_to_paste = (col * cell_size, row * cell_size)
            value = pos.tents_number_required            
            text_img = Image.open(get_num_path(value))
            text_fg = text_img.resize((cell_size,cell_size)).convert("RGBA")
            result_im.paste(text_fg, box=box_to_paste, mask=text_fg)
        
    result_im.save(output_path)
    result_im.show()

def test_draw_board():
    path = os.path.join(os.curdir, "input/6x6/puzzle3.txt")
    game = Tents(path)
    draw_tents_board(board = game.start.board,cell_size=100,result_file_name="board_test.png")

# test_draw_board()