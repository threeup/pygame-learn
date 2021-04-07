''' holds world class '''

from cnphy.body import Body


class World():
    '''
    A class which holds all entities
    '''
    # Physics collision types
    COLLTYPE_DEFAULT = 0
    COLLTYPE_PAWN = 1
    COLLTYPE_TARGET = 2
    COLLTYPE_CURSOR = 3

    def __init__(self, space):
        self.space = space

        self.space.add_collision_handler(
            self.COLLTYPE_PAWN, self.COLLTYPE_TARGET, self.pawn_target_func)
        self.space.add_collision_handler(
            self.COLLTYPE_PAWN, self.COLLTYPE_PAWN, self.pawn_pawn_func)
        self.space.add_collision_handler(
            self.COLLTYPE_PAWN, self.COLLTYPE_CURSOR, self.pawn_cursor_func)

        self.ents = []
        self.elapsed_time = 0
        self.run_physics = True

    def tick(self, delta):
        ''' increment the game '''
        self.elapsed_time += delta
        for ent in self.ents:
            ent.tick(delta)

    def draw(self, screen, flipy):
        ''' draw the game '''
        for ent in self.ents:
            ent.draw(screen, flipy)

    @staticmethod
    def pawn_cursor_func(_arbiter, _space, _data):
        ''' pawn does not collide with cursor'''
        return False

    @staticmethod
    def pawn_pawn_func(_arbiter, _space, _data):
        ''' pawn does not collide with pawns'''
        return False

    @staticmethod
    def pawn_target_func(arbiter, _space, _data):
        '''Simple callback that increases the radius of circles touching the mouse'''
        shape1, shape2 = arbiter.shapes
        cnshape1 = shape1.cnshape
        cnshape2 = shape2.cnshape
        cnbody1 = shape1.body.cnbody
        cnbody2 = shape2.body.cnbody

        id1 = cnshape1.owner.name[-1]
        id2 = cnshape2.owner.name[-1]
        if id1 == id2:
            if cnbody1.get_body_type() == Body.DYNAMIC:
                cnshape2.owner.attach = cnshape1.owner
            elif cnbody2.get_body_type() == Body.DYNAMIC:
                cnshape1.owner.attach = cnshape2.owner
            return False
        return True
