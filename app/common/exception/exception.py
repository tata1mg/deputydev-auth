class SignUpError(Exception):
    """
    Exception raised for errors during sign-up.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(f"Sign-Up Error: {self.message}")
