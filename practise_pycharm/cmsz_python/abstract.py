# -*- encoding: utf-8 -*-
__metaclass__ = type
class Secret:
    print "Class Secret being defined"
    def __inaccess(self):
        print "Bet, you can't see me."


    def access(self):
        print "The secret message is:"
        self.__inaccess()

print "main"
s = Secret()
d = Secret()
s.access()

# __inaccess() -> _Secret__inaccess()
s._Secret__inaccess()
