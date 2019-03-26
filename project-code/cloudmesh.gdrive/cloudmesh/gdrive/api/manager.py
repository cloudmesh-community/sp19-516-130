class Manager(object):

    def __init__(self):
        print("init {name}".format(name=self.__class__.__name__))

    def list(self, parameter):
        print("list", parameter)

    def create_dir(storage=None, directory = None):
        pass

    # storage [--storage=<SERVICE>] create dir DIRECTORY
    #def [--storage=<SERVICE>] list SOURCE [--recursive]
    #def [--storage=<SERVICE>] put SOURCE DESTINATION [--recursive]
    #def [--storage=<SERVICE>] get SOURCE DESTINATION [--recursive]
    #def [--storage=<SERVICE>] delete SOURCE
    # storage [--storage=<SERVICE>] search DIRECTORY FILENAME [--recursive]


    #source or destination means file or directory


    def funcname(self, parameter_list):
        raise NotImplementedError [--storage=<SERVICE>] search DIRECTORY FILENAME [--recursive]

    def list(self, storage = None, source = None):
        pass

    def put(self, storage = None, source = None, destination = None):
        pass

    def get(self, storage = None, source = None, destination = None):
        pass
    
    def delete(self, storage = None, source=None):
        pass

    def search(self, storage=None, directory = None, filename =None):
        pass
