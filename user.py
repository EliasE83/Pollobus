
class User:
    def __init__(self, user):
        self.user = user
    def get_id(self):
        return self.user
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return True