import os

class UserInfo:
    def __init__(self, first_name, last_name, email, app_password, smtp_server, smtp_port):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.app_password = app_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port


    def __str__(self):
        return f"UserInfo(first_name={self.first_name}, last_name={self.last_name}, email={self.email}, password={self.app_password}, smtp_server={self.smtp_server}, smtp_port={self.smtp_port})"
    
    
    def save(self):
        if not os.path.exists("./files"):
            os.makedirs("./files")
        if not os.path.exists("./files/userInfo.txt"):
            open("./files/userInfo.txt", 'w').close()
        with open("./files/userInfo.txt", 'w') as file:
            file.write(f"{self.first_name},{self.last_name},{self.email},{self.app_password},{self.smtp_server},{self.smtp_port}\n")

    @classmethod
    def load(cls):
        if not os.path.exists("./files/userInfo.txt"):
            return None
        with open("./files/userInfo.txt", 'r') as file:
            data = file.readline().strip().split(',')
            if len(data) == 6:
                return cls(*data)
            else:
                return None