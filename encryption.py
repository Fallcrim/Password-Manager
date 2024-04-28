from cryptography.fernet import Fernet


class EncryptionHandler(object):
    """
    Class EncryptionHandler handles the encryption of the database file
    """
    def __init__(self, password: bytes):
        self._cipher = Fernet(password)

    def encrypt(self, raw_data: bytes):
        """
        Encrypts the plaintext data
        :param raw_data:
        :return:
        """
        return self._cipher.encrypt(raw_data)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """
        Decrypts the encrypted data
        :param encrypted_data:
        :return:
        """
        return self._cipher.decrypt(encrypted_data)
