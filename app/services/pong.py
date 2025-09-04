from typing import Any, Dict


class Pong:
    def __init__(self):
        self.message = "pong"

    def get_message(self) -> Dict[str, Any]:
        return {"message": self.message}
