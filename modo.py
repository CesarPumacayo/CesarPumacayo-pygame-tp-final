DEBUG = False

def cambiar_modo():
    global DEBUG
    DEBUG = not DEBUG # supongo ver hitbox

def get_modo():
    return DEBUG