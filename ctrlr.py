''' holds Ctrlr class '''

class Ctrlr:
    '''
    A class which manipulates controlled entities
    '''

    def __init__(self):
        self.list = []
        self.count = len(self.list)

    def add_enty(self, enty):
        ''' associate an entity to a controller '''
        self.list.append(enty)
        self.count = len(self.list)

    def tick(self, _delta):
        ''' no op '''
        return
