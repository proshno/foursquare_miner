import re
import sys
import traceback


class AttributeWarningManager(object):
    def __init__(self):
        pass


    def __enter__(self):
        pass


    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            pass
        else:
            if exc_type in (AttributeError, KeyError):
                code = traceback.extract_tb(exc_tb)[-1][3]
                attr_name = re.findall(r'(\w+)[ \t]*=.*', code)[0]
                print "The attribute %s could not be found" % attr_name
            else:
                traceback.print_tb(exc_tb)

            return True


_attr_warn = AttributeWarningManager()
