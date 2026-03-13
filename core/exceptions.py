
class NotFoundException(Exception):
    status_code = 404

class BadRequestException(Exception):
    status_code = 400

class ConflictException(Exception):
    status_code = 409