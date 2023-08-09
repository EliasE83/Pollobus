mock_users = {'admin':'123456'}

class dbHelper:
    def get_user(self,user):
        if user in mock_users:
            return mock_users[user]
        return None