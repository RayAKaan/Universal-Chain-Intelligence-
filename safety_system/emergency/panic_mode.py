class PanicMode:
    def __init__(self):
        self.active = False
        self.reason = ""

    def activate(self, reason: str) -> None:
        self.active = True
        self.reason = reason

    def deactivate(self, authorization: str) -> None:
        if authorization != "human_authorized":
            raise PermissionError("human authorization required")
        self.active = False
        self.reason = ""
