class Node:
    def __init__(self, state, parent=None):
        self.visits = 1
        self.reward = 0.0
        self.state = state
        self.children = []
        self.children_move = []
        self.parent = parent

    def add_child(self, child_state, move):
        child = Node(child_state, self)
        self.children.append(child)
        self.children_move.append(move)

    def update(self, reward):
        self.reward += reward
        self.visits += 1

    def fully_explored(self):
        if len(self.children) == len(self.state.legal_moves()):
            return True
        return False