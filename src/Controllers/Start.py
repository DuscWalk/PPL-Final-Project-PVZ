class Start:
    def __init__(self):
        self.running = True
        with open("users.txt", "r") as f:
            self.username = f.read()

    def run(self):


    def get_username(self):
        return self.username
