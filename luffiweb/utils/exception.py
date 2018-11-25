# Author: harry.cai
# DATE: 2018/11/17

class PricePolicyInvalid(Exception):
    def __init__(self, msg):
        self.msg = msg
