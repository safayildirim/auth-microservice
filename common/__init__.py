def make_error(err_payload, http_status_code):
    return err_payload, http_status_code


errors = {
    'WrongCredentialError': make_error({'status': '401', 'message': 'Email or password does not match.'}, 401),
    'UserAlreadyExistError': make_error({'status': '401', 'message': 'User already exist.'}, 401),
    'UserNotFoundError': make_error({'status': '404', 'message': 'User is not found.'}, 404),

}
