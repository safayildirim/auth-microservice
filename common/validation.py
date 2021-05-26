class RegisterRequestDTO:
    email: str = 'test@'
    password: str = 'test'

    def __str__(self) -> str:
        return f'email: {self.email}, password: {self.password}'


def request(dataType):
    def decorator(fun):
        d = dataType()
        print(d)
        print(getattr(d, 'email'))
        print(getattr(d, 'email'))
        setattr(d, 'username', 'zeevac')
        print(getattr(d, 'username'))
        print(d.username)

        def wrapper(*args, **kwargs):
            kwargs['request'] = d
            return fun(*args, **kwargs)

        return wrapper

    return decorator


@request(RegisterRequestDTO)
def sum(request):
    print('string request: ', request)


print(sum())
