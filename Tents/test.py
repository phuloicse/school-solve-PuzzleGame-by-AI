from gc import is_finalized
import sys
import copy

from tents_and_tree import BoardNode


class Dog():
    def __init__(self, name):
        self.name = name

        # Hashsing and Equal allows the positnode to be used as dictionary key
    
    def passing(self, is_all_ok): 
        is_all_ok = True 
    def test(self):
        is_ok = False
        self.passing(is_all_ok=is_ok)
        if is_ok: 
            print("TRUE TRUE TRUE ")

    def __hash__(self):
        return self.name

    def __eq__(self, other):
        return (self.name) == (other.name)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)


if __name__ == "__main__":
    dog1 = Dog("1")
    dog2 = Dog("2")
    dog3 = Dog("3")
    dog4 = Dog("4")
    dog1.test()
    board: BoardNode = BoardNode(board_grid={}, width=3, height=3, tents={'a': dog1}, trees={}, constraints={})
    board2: BoardNode = BoardNode(board_grid={}, width=3, height=3, tents={'a': dog2}, trees={}, constraints={})
    board3: BoardNode = BoardNode(board_grid={}, width=3, height=3, tents={'a': dog3}, trees={}, constraints={})
    board4: BoardNode = BoardNode(board_grid={}, width=3, height=3, tents={'a': dog4}, trees={}, constraints={})
    set_a = {board,board2}
    print(board3 in set_a)