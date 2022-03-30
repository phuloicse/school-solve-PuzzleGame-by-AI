import copy
import sys

from classes.tents_classes import BoardNode, BoardStateType, ConstraintNode, GameNode, PositionNode, A_Star_Frontier, \
    TentNode, TreeNode, get_node_char, Action, EMPTY_CHAR, TREE_CHAR, TENT_CHAR, StackFrontier
import time
import resource

"""
    _: the character to ignore (only valid at [0][0])
    #: indicates an empty cell
    T: indicates a tree location
    number: only valid for contraints, specifying number of tents in this row or col
"""


HEX_SET = {"A","B","C","D","E","F","1","2","3","4","5","6","7","8","9","0"}

def hex_char_to_int(char:str):
    return int("0x" + char,0)

class Tents():
    def __init__(self, filename: str):
        self.solution_found = None
        with open(filename) as f:
            contents = f.read()
        # Make sure the input is valid
        self.validate_and_init_game_state(contents)
        self.solution = None

    def validate_and_init_game_state(self, contents):
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = len(contents[0])
        # Check if every row have the same number of char
        board = {}
        self.tree_dict = {}
        self.contraints_dict = {}

        for row_index, row in enumerate(contents):
            if len(row) != self.width:
                raise Exception(
                    f"Every row must have the same width:: Expected {self.width}, Found {len(row)}")
            # Set up the tree positions
            for col_index, char in enumerate(row):
                if char == "_":
                    continue
                elif char == EMPTY_CHAR:
                    pos_node = PositionNode(row_index, col_index)
                    board[hash(pos_node)] = pos_node
                elif char == TREE_CHAR:
                    tree_node = TreeNode(row_index, col_index)
                    board[hash(tree_node)] = tree_node
                    self.tree_dict[hash(tree_node)] = tree_node
                elif char == TENT_CHAR:
                    tent = TentNode(row_index, col_index)
                    board[hash(tent)] = tent
                elif char in HEX_SET:
                    constraint_node = ConstraintNode(
                        row_index, col_index, hex_char_to_int(char))
                    self.contraints_dict[hash(
                        constraint_node)] = constraint_node
                else:
                    print("char invalid is: " + str(char))
                    raise Exception("Please check the Input again" + str(char))

        self.start = GameNode(board=BoardNode(board_grid=board, width=self.width - 1, height=self.height - 1,
                                              tents={}, trees=self.tree_dict, constraints=self.contraints_dict),
                              parent=None, action=None)


    def solve(self, print_step_by_step = False):
        """Finds a solution to puzzle, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        self.current = self.start
        frontier = StackFrontier()
        frontier.add(self.current)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            if print_step_by_step:
                node.board.print_board()

            # If node is the goal, then we have a solution
            if self.solution_found:
                actions = []
                boards = []
                while node.parent is not None:
                    actions.append(node.action)
                    boards.append(node.board)
                    node = node.parent
                actions.reverse()
                boards.reverse()
                self.solution = (actions, boards)
                return

            # Mark node as explored
            self.explored.add(node.board)

            # Add neighbors to frontier
            for action, board_applied_action in self.neighbors(node.board):
                if not frontier.contains_state(board_applied_action) and board_applied_action not in self.explored:
                    child = GameNode(board=board_applied_action, parent=node, action=action)
                    frontier.add(child)


    def neighbors(self, board: BoardNode):
        actions = [Action(pos) for pos in board.possible_locations.values()]

        result = []
        for action in actions:
            new_board = copy.deepcopy(board)
            new_board.apply_actions(action)
            if new_board.board_state != BoardStateType.INVALID:
                result.append((action, new_board))
                if new_board.board_state == BoardStateType.SOLVED:
                    self.solution_found = True
                    break

        return result

    # Check if all the constraint are passed

    def check_completeted(self, board: BoardNode) -> bool:
        # ? Is it true that there are exactly 1 solution ?
        # Check number of tents vs number of tree
        tent_number_check = False
        if len(board.tents_dict) < len(board.trees_dict):
            return False

        # All the constraints are satisfied
        constraint_check = False
        for constraint in board.constraint_dict.values():
            if not constraint.is_satisfied:
                return False
        # All the tree must be binded by exactly 1 tent
        bind_check = False

        return tent_number_check and bind_check and constraint_check

    def print(self):
        print(f"CONSTRAINTS:")
        self.print_contraints_dict()
        print("\nBOARD:")
        self.start.board.print_board()

    def print_solution(self, output_file_name = None, auto_output_path = None):
        if self.solution:
            print("\nSOLUTION BOARD: ")
            board_solved = self.solution[1][-1]
            board_solved.print_board()
            if output_file_name:
                from draw_tent_board import draw_tents_board
                draw_tents_board(board=board_solved, result_file_name=output_file_name, auto_output_path=auto_output_path)


    def print_node_state(self, game_node: GameNode):
        # Print a game state: default to print start node
        node_to_print = game_node if game_node is not None else self.start
        board = node_to_print.board
        board.print()

    def print_contraints_dict(self):
        for key in self.contraints_dict.keys():
            print(get_node_char(self.contraints_dict[key]), end=" ")


def draw_board_as_image(board: BoardNode, filename="board.png"):
    from PIL import Image, ImageDraw
    cell_size = 50
    cell_border = 2

    # Create a blank canvas
    img = Image.new(
        "RGBA",
        (board.width * cell_size, board.height * cell_size),
        "black"
    )
    draw = ImageDraw.Draw(img)

    for index, pos in enumerate(board.grid.values()):
        return

def solve_from_input(input_file_name: str):
    game = Tents(input_file_name)
    game.solve()


if __name__ == '__main__':

    time_start = time.perf_counter()

    if len(sys.argv) not in [2,3]:
        sys.exit("Usage: python tents_solver.py input_file.txt  ||  python tents_solver.py input_file.txt output_file_name")

    game = Tents(str(sys.argv[1]))
    print("Tents initialized: ")
    game.print()

    print("Trying to solve the puzzle")
    game.solve()
    print("Num of state explored: ", game.num_explored)
    print("Solution: ", game.solution)

    output_file_name = None
    if len(sys.argv)  == 3:
        output_file_name = str(sys.argv[2])
    game.print_solution(output_file_name)

    # insert code here ...
    time_elapsed = (time.perf_counter() - time_start)
    # memB = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # print("%5.1f secs %5.1f MByte" % (time_elapsed, memB))



