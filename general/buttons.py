

class Buttons:
    '''Button class returning the value of the current button pressed.
       0 = x, 1 = a, 2 = y, 3 = b, 4 = None
    '''

    def __init__(self, BTN_X, BTN_Y, BTN_A, BTN_B) -> None:
        self.x = BTN_X
        self.y = BTN_Y
        self.a = BTN_A
        self.b = BTN_B

    def get_value(self):
        if self.x.value == False:
            return 0
        elif self.a.value == False:
            return 1
        elif self.y.value == False:
            return 2
        elif self.b.value == False:
            return 3
        return 4
