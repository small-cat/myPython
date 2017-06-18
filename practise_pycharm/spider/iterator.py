# -*- encoding: utf-8 -*-
class Fabs:
    def __init__(self, number):
        self.a = 0
        self.b = 1
        self.count = number
        self.start = 0

    def __iter__(self):
        return self

    def next(self):
        if self.start < self.count:
            self.a, self.b = self.b, self.a + self.b
            self.start += 1
            return self.a
        else:
            raise StopIteration


print Fabs(3)

for key in Fabs(10):
    print key,