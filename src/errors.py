from enum import Enum

# Login errors message.
class LOGIN_ERROR(Enum):
    INVALID_USERNAME_PASSWORD = '0'
    USERNAME_EXIST = '1'

# Method that converts the inbound login error to a more elaborate description.
# In addition, a type is given to select the color.
def getLoginErrorMessage(error_id: str) -> {'message': str, 'type': str}:
    if LOGIN_ERROR(error_id) == LOGIN_ERROR.INVALID_USERNAME_PASSWORD:
        return {'message': 'Invalid Username or Password.', 'type': 'danger'}
    elif LOGIN_ERROR(error_id) == LOGIN_ERROR.USERNAME_EXIST:
        return {'message': 'Username already exists.', 'type': 'danger'}
    