import stateless.generate as G

def validate(inputstr):
    try:
        if inputstr[0] != b'H':
            return G.Status.Incorrect, None, None
        if inputstr[1] != b'E':
            return G.Status.Incorrect, None, None
        if inputstr[2] != b'L':
            return G.Status.Incorrect, None, None
        if inputstr[3:5].b != b'LO':
            return G.Status.Incorrect, None, None
        return G.Status.Complete, None, None
    except G.NeedMoreException as e:
        return G.Status.Incomplete, None, None

