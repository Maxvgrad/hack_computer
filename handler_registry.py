
class HandlerRegistry:

    def __init__(self, handlers) -> None:
        super().__init__()
        self.handlers = handlers

    def find(self, type):
        for handler in self.handlers:
            if handler.can_handle(type):
                return handler
        return None

    # def reset(self):
    #     for handler in self.handlers:
    #         handler.reset()
