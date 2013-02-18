class GameObject:
    def __init__(self, image, x, y, screen):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = image
        self.moves = 0
        
    def draw(self):
        self.screen.blit( self.image, ( self.x, self.y ) )
        
    def set_image(self, image):
        self.image = image
        
    def move(self, rel_x, rel_y, lvl, img, o, pl):
        try:
            if not lvl.lvl[(self.y + rel_y*lvl.esize)/lvl.esize][(self.x + rel_x*lvl.esize)/lvl.esize] == '#':
                if ((self.x + rel_x)*lvl.esize)/lvl.esize < 0 or ((self.y + rel_y)*lvl.esize)/lvl.esize < 0:
                    return
                self.x = self.x + rel_x*lvl.esize
                self.y = self.y + rel_y*lvl.esize
                if lvl.lvl[self.y/lvl.esize][self.x/lvl.esize] == '$':
                    o[self.y/lvl.esize][self.x/lvl.esize].set_image(img['_'])
                    lvl.lvl[self.y/lvl.esize][self.x/lvl.esize] = '_'
                    pl.raise_points()
                if lvl.lvl[self.y/lvl.esize][self.x/lvl.esize] == 'E':
                    pl.set_finish(1)
            else:
                if ((self.x + rel_x)*lvl.esize)/lvl.esize < 0 or ((self.y + rel_y)*lvl.esize)/lvl.esize < 0:
                    return
                if lvl.lvl[(self.y + 2*rel_y*lvl.esize)/lvl.esize][(self.x + 2*rel_x*lvl.esize)/lvl.esize] == '_':
                    o[(self.y + 2*rel_y*lvl.esize)/lvl.esize][(self.x + 2*rel_x*lvl.esize)/lvl.esize].set_image(img['#'])
                    lvl.lvl[(self.y + 2*rel_y*lvl.esize)/lvl.esize][(self.x + 2*rel_x*lvl.esize)/lvl.esize] = '#'
                    o[(self.y + rel_y*lvl.esize)/lvl.esize][(self.x + rel_x*lvl.esize)/lvl.esize].set_image(img['_'])
                    lvl.lvl[(self.y + rel_y*lvl.esize)/lvl.esize][(self.x + rel_x*lvl.esize)/lvl.esize] = '_'
                    self.x = self.x + rel_x*lvl.esize
                    self.y = self.y + rel_y*lvl.esize
            self.moves += 1
            print lvl.tostring( self.x, self.y )
        
        except:
            import sys
            print sys.exc_info()[0]

