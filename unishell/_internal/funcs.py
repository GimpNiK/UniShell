class StubClass:
    """Класс-заглушка, который поглощает любые обращения"""
    
    def __getattr__(self, name):
        return self
    
    def __call__(self, *args, **kwargs):
        return self
    
    def __getitem__(self, key):
        return self
    
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
    
    def __iter__(self):
        return iter([])
    
    def __next__(self):
        raise StopIteration
    
    def __len__(self):
        return 0
    
    def __str__(self):
        return "<Stub>"
    
    def __repr__(self):
        return "<Stub>"
    
    def __bool__(self):
        return False