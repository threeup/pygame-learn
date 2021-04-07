# pylint: skip-file
import math


class Vec2:
    '''
    A two dimensional vector composed of two floats
    '''

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vec2(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vec2(x, y)

    def __truediv__(self, other):
        x = self.x / other
        y = self.y / other
        return Vec2(x, y)

    def __len__(self):
        return 2

    def __str__(self):
        return str(self.x)+","+str(self.y)

    def __repr__(self):
        return str(self.x)+","+str(self.y)

    def to_tuple(self):
        '''
        converts to a tuple
        ((float, float))
        '''
        return (self.x, self.y)

    def rotated(self, angle):
        '''
        Rotates by an amount in degrees
        > (float)
        < (Vec2)
        '''
        x = self.x * math.cos(angle) - self.y*math.sin(angle)
        y = self.x * math.sin(angle) + self.y*math.cos(angle)
        return Vec2(x, y)

    def length(self):
        '''
        Returns vector length
        < (float)
        '''
        return math.sqrt(self.x**2 + self.y**2)

    def scaled(self, scale):
        '''
        Scales by an amount
        > (float)
        < (Vec2)
        '''
        return Vec2(self.x*scale, self.y*scale)


    def normalized_and_length(self):
        '''
        Returns length and normalized vector
        < (float,Vec2)
        '''
        vec_len = self.length()
        if vec_len > 0.0001:
            vec_dir = self.scaled(1/vec_len)
        else:
            vec_dir = Vec2(0,0)
        return (vec_dir, vec_len)

    def normalized(self):
        '''
        Returns normalized vector
        < (Vec2)
        '''
        (vec_dir, _) = self.normalized_and_length()
        return vec_dir

    def lerp_percent(self, other, percent):
        inv = 1 - percent
        return Vec2(self.x*inv + other.x*percent, 
            self.y*inv + other.y*percent)

    def lerp_step(self, other, step):
        (diff_dir, diff_len) = (other - self).normalized_and_length()
        amount = min(diff_len, step)
        return self + diff_dir.scaled(amount)