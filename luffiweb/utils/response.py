# Author: harry.cai
# DATE: 2018/11/17
class BaeResponse(object):
    def __init__(self):
        self.data = None
        self.code = None
        self.error = None
    @property
    def get_dict(self):
        return self.__dict__