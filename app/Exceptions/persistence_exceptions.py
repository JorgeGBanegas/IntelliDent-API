class RecordNotFoundException(Exception):
    pass


class RecordAlreadyExistsException(Exception):
    pass


class IntegrityErrorException(Exception):
    pass


class InvalidDataException(Exception):
    pass
