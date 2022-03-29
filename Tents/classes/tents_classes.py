# Used for DFS Search


from copy import copy, deepcopy
from enum import Enum
from typing import Dict, List, Set
import heapq
import functools




# * Frontier for DFS strategy


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, board):
        return any(node.board == board for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

# * Frontier for BFS strategy
class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


# * This frontier will keep an sorted list of nodes based on there heuristics function
# * On removal, pop out the node with highest value of heuristics value
# * On insert, calculate and push the node in its correct order
# ==> Heap is suitable for this



class A_Star_Frontier(StackFrontier):
    def __init__(self):
        self.frontier = []

    def add(self, node):
        wrapped_node = HeuristicNode(node)
        heapq.heappush(self.frontier, wrapped_node)

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = heapq.heappop(self.frontier)
            return node
# Note: Index of the game start from 1


class PositionNode():
    def __init__(self, row_index, col_index):
        self.row_index = row_index
        self.col_index = col_index

    # Hashsing and Equal allows the positnode to be used as dictionary key
    def __hash__(self):
        return self.row_index * 10 + self.col_index

    def __eq__(self, other):
        return (self.row_index, self.col_index) == (other.row_index, other.col_index)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)

    def __str__(self) -> str:
        return f'PosNode({self.row_index},{self.col_index})'


class TreeNode(PositionNode):
    def __init__(self, row_index, col_index):
        PositionNode.__init__(self, row_index, col_index)
        self.is_alone_tree = False
        self.is_properly_binded = False
    # def bindTent


class TentNode(PositionNode):
    def __init__(self, row_index, col_index):
        PositionNode.__init__(self, row_index, col_index)
        self.posible_tree_binded = set()

    def bind_tree(self, tree_node: TreeNode):
        if tree_node.is_alone_tree:
            tree_node.is_properly_binded = True
        self.posible_tree_binded.add(tree_node)

    def __str__(self) -> str:
        return f'TentNode({self.row_index},{self.col_index})'


class ConstraintNodeType(Enum):
    ROW = 1
    COL = 2


# Row or Col: specifying the sums of tent required on the row or col


class ConstraintNode(PositionNode):
    def __init__(self, row_index, col_index, tents_number_required):
        PositionNode.__init__(self, row_index, col_index)
        self.contraint_type = ConstraintNodeType.COL if row_index == 0 else ConstraintNodeType.ROW
        self.tents_number_required = tents_number_required

    def is_satisfied(self) -> bool:
        return self.tents_number_required == 0


def get_node_char(node: PositionNode) -> str:
    if isinstance(node, TreeNode):
        return "T"
    elif isinstance(node, ConstraintNode):
        char = "C" + \
               str(node.col_index) if node.contraint_type == ConstraintNodeType.COL else "R" + \
                                                                                         str(str(
                                                                                             node.row_index))
        return char + ":" + str(node.tents_number_required)
    elif isinstance(node, TentNode):
        return "A"
    else:
        return "#"


def calculate_key(row_index: int, col_index: int) -> int:
    return int(int(row_index) * 10 + int(col_index))


# Class defining an action
class Action():
    # Put an tent on a position on the board
    def __init__(self, pos: PositionNode) -> None:
        self.tent_pos = pos

    def print(self):
        print(
            f'A tent is placed on: {self.tent_pos.row_index} , {self.tent_pos.col_index}')

    def __str__(self) -> str:
        return f'Tent to: ({self.tent_pos})'


class BoardStateType(Enum):
    VALID = 1
    INVALID = 2
    SOLVED = 3
    NO_SOLUTION = 4


# Containt the board state and main board functionalities
class BoardNode():
    board_state: BoardStateType

    def __init__(self, board_grid: Dict[int, PositionNode], width: int, height: int, tents=None,
                 trees=None, constraints=None):
        if tents is None:
            tents = {}
        if trees is None:
            trees = {}
        if constraints is None:
            constraints = {}
        # Useful positions saved for fast access: Not used currently
        self.diagonal_to_trees = {}
        self.straight_adjacent_to_trees = {}
        self.grid = board_grid

        self.width = width
        self.height = height

        self.tents_dict = tents
        self.trees_dict = trees
        self.possible_locations = board_grid

        self.constraint_dict = constraints
        # Keep the constraints for reviewing
        temp = deepcopy(constraints)
        self.constraint_set = set(temp.values())

        self.board_state = BoardStateType.VALID

        self.update_possible_location(init=True)

        self.is_all_ok_shorcut_check = False

    # Hashsing and Equal allows the positnode to be used as dictionary key
    def __hash__(self):
        return hash(frozenset(self.tents_dict.keys()))

    def __eq__(self, other):
        return self.tents_dict.keys() == other.tents_dict.keys()

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)

    def update_possible_location(self, init=False, tent_node: TentNode = None):
        # Remove the pos of tree: do this only once
        if init:
            # Remove the tree values
            pos_to_remove = set()

            tree_set = set(self.trees_dict.values())
            diagonal_to_trees = set()
            straight_adjacent_to_trees = set()
            adjacent_to_tree = set()

            tree_dict_values = self.trees_dict.values()
            for tree in tree_dict_values:
                diagonal_to_trees = diagonal_to_trees.union(
                    set(self.get_diagonal_adjacent_nodes(tree).values()))

                straight_adjacent_to_trees = straight_adjacent_to_trees.union(
                    set(self.get_straight_adjacent_nodes(tree).values()))

                adjacent_to_tree = adjacent_to_tree.union(
                    set(self.get_adjacent_nodes(tree).values()))

            self.diagonal_to_trees = diagonal_to_trees
            self.straight_adjacent_to_trees = straight_adjacent_to_trees
            pure_diagonal_to_tree = diagonal_to_trees.difference(
                straight_adjacent_to_trees)

            pos_to_remove = pos_to_remove.union(
                pure_diagonal_to_tree).union(tree_set)

            # Filter out the zeored column and row
            zeroed_contraints = [constraint for constraint in self.constraint_dict.values() if
                                 isinstance(constraint, ConstraintNode) and constraint.tents_number_required == 0]
            pos_removed_by_constraints_set = set()
            for con in zeroed_contraints:
                if con.contraint_type == ConstraintNodeType.COL:
                    col_idx = con.col_index
                    pos_to_remove = pos_to_remove.union(
                        set(self.get_whole_col(col_idx)))
                else:
                    row_idx = con.row_index
                    pos_to_remove = pos_to_remove.union(
                        set(self.get_whole_row(row_idx)))

            possible_pos_set = set(
                self.possible_locations.values()).difference(pos_to_remove)
            possible_pos_set = possible_pos_set.intersection(adjacent_to_tree)

            self.possible_locations = dict(
                [(hash(item), item) for item in possible_pos_set])

        # Remove the ZEROED row and columns:
        if tent_node:
            self.place_tent_node_and_check_constraint(tent_node)
            if self.board_state == BoardStateType.INVALID:
                return

            # Remove the adjacent nodes from the possible list
            adjacent_to_tents = self.get_adjacent_nodes(tent_node)
            self.remove_nodes_from_pos_list(adjacent_to_tents)

            # Update the state related to tree
            tree_set = set(self.trees_dict.values())
            cross_adjacent_to_tent = set(
                self.get_straight_adjacent_nodes(tent_node).values())

            possible_tree_binded = tree_set.intersection(
                cross_adjacent_to_tent)
            if len(possible_tree_binded) == 1:
                tree_binded = possible_tree_binded.pop()
                key = hash(tree_binded)
                self.trees_dict[key].is_properly_binded = True
                adjacent_to_tree = self.get_straight_adjacent_nodes(
                    tree_binded)
                for adjacent_node in adjacent_to_tree.values():
                    adjacents_set = set(
                        self.get_straight_adjacent_nodes(adjacent_node).values())
                    adjacents_set = adjacents_set.difference([tree_binded])
                    found_other_tree = False
                    for node in adjacents_set:
                        if hash(node) in self.trees_dict.keys():
                            found_other_tree = True
                            break
                    if not found_other_tree:
                        self.remove_nodes_from_pos_list([adjacent_node])
            # Check for invalid tree
            diagonal_to_tent_set = set(
                self.get_diagonal_adjacent_nodes(tent_node).values())
            tree_diag_to_tent = tree_set.intersection(diagonal_to_tent_set)
            for tree in tree_diag_to_tent:
                if not set(self.get_straight_adjacent_nodes(tree).values()).intersection(set(self.possible_locations.values())):
                    self.board_state = BoardStateType.INVALID
                    return
            # * If we bind to an alone tree --> Other pos straight adjacent to tree is removed
            trees_to_bind = len(self.trees_dict) - len(self.tents_dict)
            if len(self.possible_locations) < trees_to_bind:
                self.board_state = BoardStateType.INVALID
                return
            # If the number of possible location is equal to number of tents => Shorcut: Try place them and check for contraints
            if len(self.possible_locations) == trees_to_bind:
                is_all_ok = False
                for pos in self.possible_locations.values():
                    is_all_ok = self.place_tent_node_and_check_constraint(
                        pos, is_shorcut_checking=True)
                    if self.board_state == BoardStateType.INVALID:
                        return
                if is_all_ok == True:
                    self.board_state = BoardStateType.SOLVED

    def place_tent_node_and_check_constraint(self, tent_node, is_shorcut_checking=False):
        if is_shorcut_checking:
            # Updating tents for visualization purpose
            tent_location = tent_node
            tent = TentNode(tent_location.row_index,
                            tent_location.col_index)
            self.grid[hash(tent)] = tent
            self.tents_dict[hash(tent)] = tent
        # Decrease the allowed tents on the chosen node
        constraint_row_node = self.get_row_constraint(tent_node)
        constraint_col_node = self.get_col_constraint(tent_node)
        if constraint_row_node.tents_number_required == 0:
            self.board_state = BoardStateType.INVALID
            return False
        if constraint_col_node.tents_number_required == 0:
            self.board_state = BoardStateType.INVALID
            return False
        constraint_col_node.tents_number_required -= 1
        if constraint_col_node.is_satisfied():
            self.remove_nodes_from_pos_list(
                self.get_whole_col(constraint_col_node.col_index))
        constraint_row_node.tents_number_required -= 1
        if constraint_row_node.is_satisfied():
            self.remove_nodes_from_pos_list(
                self.get_whole_row(constraint_row_node.row_index))

        if len(self.tents_dict) > len(self.trees_dict):
            self.board_state = BoardStateType.INVALID
            return False

        return True

    def print_board(self, mode="board_text"):
        for key in self.grid.keys():
            node = self.grid[key]
            if mode == "board_text":
                print(f'{get_node_char(node=node)}', end="")
            elif mode == "class_presentation":
                print(node)
            if node.col_index % self.width == 0:
                print("")

    def apply_actions(self, action: Action):
        # Update the possible location list
        tent_location = action.tent_pos
        tent = TentNode(tent_location.row_index, tent_location.col_index)
        self.grid[hash(tent)] = tent
        self.tents_dict[hash(tent)] = tent
        self.update_possible_location(tent_node=tent)

    def get_adjacent_nodes(self, node: PositionNode) -> Dict[int, PositionNode]:
        (row_index, col_index) = self.get_index_tuple_from_node(node)
        result = {}
        for x, y in [(row_index + i, col_index + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0]:
            key = calculate_key(x, y)
            if key in self.grid:
                node = self.grid[key]
                result[key] = PositionNode(node.row_index, node.col_index)
        return result

    #
    #   #X#X
    #   ##N#
    #   #X#X
    def get_diagonal_adjacent_nodes(self, node: PositionNode) -> Dict[int, PositionNode]:
        (row_index, col_index) = self.get_index_tuple_from_node(node)
        result = {}
        for x, y in [(row_index + i, col_index + j) for i in (-1, 1) for j in (-1, 1)]:
            key = calculate_key(x, y)
            if key in self.grid:
                node = self.grid[key]
                result[key] = PositionNode(node.row_index, node.col_index)
        return result

    #
    #   ##X#z
    #   #XNX
    #   ##X#

    def get_straight_adjacent_nodes(self, node: PositionNode) -> Dict[int, PositionNode]:
        (row_index, col_index) = self.get_index_tuple_from_node(node)
        result = {}
        top = calculate_key(row_index - 1, col_index)
        bottom = calculate_key(row_index + 1, col_index)
        right = calculate_key(row_index, col_index + 1)
        left = calculate_key(row_index, col_index - 1)
        for key in [top, bottom, right, left]:
            if key in self.grid:
                node = self.grid[key]
                result[key] = PositionNode(node.row_index, node.col_index)
        return result

    def get_index_tuple_from_node(self, node: PositionNode):
        node_hash_val = hash(node)
        row_index = int(node_hash_val / 10)
        col_index = node_hash_val % 10
        return (row_index, col_index)

    def get_row_constraint(self, node: PositionNode) -> ConstraintNode:
        return self.constraint_dict.get(hash(PositionNode(row_index=node.row_index, col_index=0)))

    def get_col_constraint(self, node: PositionNode) -> ConstraintNode:
        return self.constraint_dict.get(hash(PositionNode(row_index=0, col_index=node.col_index)))

    def get_whole_col(self, col_idx):
        return [PositionNode(i, col_idx) for i in range(1, self.height + 1)]

    def get_whole_row(self, row_idx):
        return [PositionNode(row_idx, j) for j in range(1, self.width + 1)]

    def remove_nodes_from_pos_list(self, nodes: dict | List[PositionNode] | Set[PositionNode]):
        possible_pos_set = set(self.possible_locations.values())
        set_to_remove = None
        if isinstance(nodes, dict):
            set_to_remove = set(nodes.values())
        elif isinstance(nodes, list):
            set_to_remove = set(nodes)
        else:
            set_to_remove = nodes
        if set_to_remove is None:
            return
        new_set = possible_pos_set.difference(set_to_remove)
        self.possible_locations = dict(
            [(hash(item), item) for item in new_set])


# Contains the board and the state and parent information for measuring perforamance and backtracking


class GameNode():
    # state is the board
    def __init__(self, board: BoardNode, parent, action: Action):
        self.board = board
        self.parent = parent
        self.action = action


# * Wrapper of an action so we calculate its heuristics value
class HeuristicNode(GameNode):
    # Put an tent on a position on the board
    def __init__(self, game_node: GameNode) -> None:
        self.board = game_node.board
        self.action = game_node.action
        self.parent = game_node.parent
        # The smaller, the better
        self.heuristic_value = self.calculate_heuristic_value(game_node.board)

    def __hash__(self):
        return hash(self.game_node.board)

    def __eq__(self, other):
        return ((self.game_node.board) == (other.game_node.board))

    def __lt__(self, other):
        return self.heuristic_value < other.heuristic_value

    def calculate_heuristic_value(self, board: BoardNode):
        # Basic heuristic:
        # * The sums of values of constraints
        # * The smaller the sums --> Less options left for next tent --> better
        # * The heapq lib is originaly an min heap as well
        return functools.reduce(lambda a, b: a + b.tents_number_required, board.constraint_dict.values(), 0)

