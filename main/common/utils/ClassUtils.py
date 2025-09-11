class ClassUtils:
    
    @staticmethod
    def Singleton(method):
        attr_name = f"_{method.__name__}_singleton" # Needs a different name to avoid recursion
        def getter(self):
            if not hasattr(self, attr_name):
                setattr(self, attr_name, method(self)) # Instantiates if not present
            return getattr(self, attr_name)
        return property(getter) # Returns as a property