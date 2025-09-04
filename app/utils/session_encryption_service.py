from app.utils.config_manager import ConfigManager
from app.utils.encryption import EncryptionService


class SessionEncryptionService(EncryptionService):
    """
    A service for handling session encryption using the functionalities provided
    by the EncryptionService class.

    Attributes:
        PASSWORD_STR (str): The encryption password retrieved from the configuration.
        PASSWORD (bytes): The encoded version of the encryption password.
    """

    PASSWORD_STR: str = ConfigManager.configs()["SESSION_ENCRYPTION_PASSWORD"]
    PASSWORD: bytes = PASSWORD_STR.encode()
