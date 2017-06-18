# -*- encoding: utf-8 -*-
__metaclass__ = type


class Bird:
    def __init__(self):
        self.hungry = True

    def eat(self):
        if self.hungry:
            print "Aaaah..."
            self.hungry = False
        else:
            print "No, thanks!"


class SongBird(Bird):
    def __init__(self):
        super(SongBird, self).__init__()
        self.sound = "Squawk!"

    def sing(self):
        print self.sound

print "--------Bird---------"
bird = Bird()
bird.eat()
bird.eat()

print "------Song Bird------"
sbird = SongBird()
sbird.sing()
sbird.eat()
sbird.eat()