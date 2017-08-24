import os

from crypto.bls.bls_crypto import BlsSerializer
from crypto.bls.bls_key_manager import BlsKeyManager


class BlsKeyManagerFile(BlsKeyManager):
    BLS_KEYS_DIR_NAME = 'bls_keys'
    BLS_SK_FILE_NAME = 'bls_sk'
    BLS_PK_FILE_NAME = 'bls_pk'

    BLS_KEYS_DIR_MODE = 0o744
    BLS_SK_FILE_MODE = 0o600
    BLS_PK_FILE_MODE = 0o644

    def __init__(self, serializer: BlsSerializer, basedir, node_name):
        super().__init__(serializer)
        self._key_path = os.path.join(basedir, node_name)
        self._init_dirs()

    def _init_dirs(self):
        assert os.path.isdir(self._key_path)
        self._bls_keys_dir = os.path.join(self._key_path, self.BLS_KEYS_DIR_NAME)
        if not os.path.exists(self._bls_keys_dir):
            os.mkdir(self._bls_keys_dir, self.BLS_KEYS_DIR_MODE)

    def _save_secret_key(self, sk: bytes):
        self.__save_to_file(sk, self.BLS_SK_FILE_NAME, self.BLS_SK_FILE_MODE)

    def _save_public_key(self, pk: bytes):
        self.__save_to_file(pk, self.BLS_PK_FILE_NAME, self.BLS_PK_FILE_MODE)

    def _load_secret_key(self) -> bytes:
        return self.__load_from_file(self.BLS_SK_FILE_NAME)

    def _load_public_key(self) -> bytes:
        return self.__load_from_file(self.BLS_PK_FILE_NAME)

    def __save_to_file(self, key: bytes, name, mode):
        path = os.path.join(self._bls_keys_dir, name)
        with open(path, 'wb') as f:
            f.write(bytearray(key))
        os.chmod(path, mode)

    def __load_from_file(self, name) -> bytes:
        path = os.path.join(self._bls_keys_dir, name)
        with open(path, 'rb') as f:
            key = f.read()
        return key