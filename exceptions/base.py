class GameException(Exception):
    def __init__(self, message: str = None) -> None:
        if message is None:
            if (cls_message := getattr(self.__class__, 'message', None)) is not None:
                message = cls_message
            else:
                raise AttributeError(f'Cant create instance without error message')

        self.message = message
        super(GameException, self).__init__(message)
