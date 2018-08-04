from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def gernerate_confirmation_token(expiration=3600):
    s = Serializer('{id:123,name:fjl}', expiration)
    return s.dumps({'confirm': 2})


def get_data(token):

    s = Serializer('{id:123,name:fjl}')

    data = s.loads(token)
    print(data)

tokent=gernerate_confirmation_token()


get_data(tokent)
