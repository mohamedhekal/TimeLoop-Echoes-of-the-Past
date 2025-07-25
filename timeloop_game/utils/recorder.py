class Recorder:
    def __init__(self):
        self.moves = []
        self.last_pos = None

    def record(self, pos):
        if self.last_pos is None:
            self.last_pos = pos
            self.moves.append({'x': 0, 'y': 0})
        else:
            dx = pos[0] - self.last_pos[0]
            dy = pos[1] - self.last_pos[1]
            self.moves.append({'x': dx, 'y': dy})
            self.last_pos = pos

    def get_moves(self):
        return self.moves 