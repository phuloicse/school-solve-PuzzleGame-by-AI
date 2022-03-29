import os
import string
from PIL import Image
from PIL import ImageFont, ImageDraw, ImageOps

from Nonogram.DFS.PuzzleState import PuzzleState
import functools

from Nonogram.draw_utils import generate_number_text_image, get_num_path

NORMAL_CELL_COLOR = (225, 225, 225, 128)
BLACK_CELL_COLOR = (10, 10, 10, 128)
# IMPOSSIBLE_CELL_COLOR = (255, 100, 60, 128)
BORDER_COLOR = (255, 60, 60, 128)


def draw_rect_on_image(image, row_idx, col_idx, fill_color=NORMAL_CELL_COLOR, cell_size=100):
    rectangle_x = row_idx * cell_size
    rectangle_y = col_idx * cell_size
    rectangle_shape = [
        (rectangle_x, rectangle_y),
        (rectangle_x + cell_size, rectangle_y + cell_size)]

    # Fill the cell with background color
    image.rectangle(
        rectangle_shape,
        fill=fill_color,
        outline=BORDER_COLOR
    )


def draw_nono_board(puzzle: PuzzleState, cell_size=100, result_file_name="board.png", draw_current_contstraints=False):
    state = puzzle.get_state()
    # Transform board state into a rectangle: calculating the constraing
    # Width = board widht + max(len(rows))
    # Height = board height + max(len(heights))
    row_constraints = puzzle.constraints.rows
    col_constraints = puzzle.constraints.columns
    max_row_constraints_len = functools.reduce(lambda acc, item: max(acc, len(item)), row_constraints, 0)
    max_col_constraints_len = functools.reduce(lambda acc, item: max(acc, len(item)), col_constraints, 0)
    board_width = len(col_constraints)
    board_height = len(row_constraints)

    width = board_width + max_row_constraints_len
    height = board_height + max_col_constraints_len

    image = Image.new('RGB', (width * cell_size, height * cell_size))
    generate_number_text_image(size=cell_size)

    draw_image = ImageDraw.Draw(image)

    for row in range(0, width):
        for col in range(0, height):
            draw_rect_on_image(draw_image, row, col, NORMAL_CELL_COLOR, cell_size)
            # Board Block should be offsett

    for row in range(0, board_height):
        for col in range(0, board_width):
            if puzzle.get_with_out_check(row, col):
                # Draw an overlay color
                row_to_paint = row + max_col_constraints_len
                col_to_paint = col + max_row_constraints_len

                draw_rect_on_image(draw_image, col_to_paint, row_to_paint,
                                   BLACK_CELL_COLOR, cell_size)
    output_path = os.path.join(os.curdir, "output", f"{result_file_name}")
    image.save(output_path)

    # Reopen temp image to paste overlays
    result_im = Image.open(output_path).convert("RGB")

    # Overlay the constraints
    for index, row_constraint in enumerate(row_constraints):
        row = index + max_col_constraints_len
        start_col = max_row_constraints_len
        for ordinal, constraint_value in enumerate(reversed(row_constraint)):
            col = start_col - ordinal - 1
            box_to_paste = (col * cell_size, row * cell_size)
            text_img = Image.open(get_num_path(constraint_value))
            text_fg = text_img.resize((cell_size, cell_size)).convert("RGBA")
            result_im.paste(text_fg, box=box_to_paste, mask=text_fg)

    for index, col_constraint in enumerate(col_constraints):
        col = index + max_row_constraints_len
        start_row = max_col_constraints_len
        for ordinal, constraint_value in enumerate(reversed(col_constraint)):
            row = start_row - ordinal - 1
            box_to_paste = (col * cell_size, row * cell_size)
            text_img = Image.open(get_num_path(constraint_value))
            text_fg = text_img.resize((cell_size, cell_size)).convert("RGBA")
            result_im.paste(text_fg, box=box_to_paste, mask=text_fg)


    result_im.save(output_path)
    result_im.show()
