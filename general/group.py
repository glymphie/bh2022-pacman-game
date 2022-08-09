import displayio

class Group:
    def __init__(self, *sprites) -> None:
        self.group = displayio.Group()

        for sprite in sprites:
            self.group.append(sprite)

    def append(self, *sprites) -> None:
        for sprite in sprites:
            self.group.append(sprite)


