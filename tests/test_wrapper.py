import StringIO

class testfile(StringIO.StringIO):
    '''StringIO file that doesn't really close, so that we can
    examinate its contents later on.'''
    def close(self):
        pass
