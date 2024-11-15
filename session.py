class Session:
    _instance = None
  
    def __init__(self):
        self.current_user = None
  
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Session()
        return cls._instance
  
    def login(self, user):
        self.current_user = user
  
    def logout(self):
        self.current_user = None
  
    def get_current_user(self):
        return self.current_user