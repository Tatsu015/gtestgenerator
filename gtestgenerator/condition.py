# -*- coding: utf-8 -*-

class AbstractCondition:
    def __init__(self):
        pass

    def check(self, data_obj):
        pass

class MergeCondition(AbstractCondition):
    def __init__(self):
        super().__init__()

    def check(self, data_obj):
        if 'classname' in data_obj:
            if len(data_obj['fixturebody']) > 0:
                return True
            else:
                return False
        if 'functionname' in data_obj:
            if len(data_obj['testbody']) > 0:
                return True
            else:
                return False
        return False
