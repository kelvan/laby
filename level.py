import os

class level:
    def __init__(self,filename,esize):
        filename = os.path.join( 'data', filename )
        f = open( filename, "r" )
        self.lvl = []
        i=0
        lines = f.read().split( '\n' )
        self.esize = esize
        self.conf = {}
        
        for line in lines[:-1]:
            if line == "// Config":
                # End of level part
                print "comment found"
                # loading configs
                self.load_config( lines[i+2:] )
                break
            self.lvl.append( [] )
            for char in line:
                self.lvl[i].append( char )
            i+=1

    def load_config(self, config):
        for line in config:
            equ_pos = line.rfind("=")
            if equ_pos >= 1:
                if line[equ_pos+1:].isdigit():
                    self.conf[ line[ :equ_pos ] ] = int( line[ equ_pos + 1: ] )
                else:
                    print "[WARNING] config value not a number, setting to zero"
                    self.conf[ line[ :equ_pos ] ] = 0
        print self.conf
    
    def tostring(self, plx, ply):
        s = ''
        lvl = self.lvl
        if len( lvl ) < plx or len( lvl[0] ) < ply:
            lvl[ plx, ply ] = 'P'
        for line in lvl:
            for char in line:
                s += char
            s += '\n'
        return s
        
    def __str__(self):
        s = ''
        for line in self.lvl:
            for char in line:
                s += char
            s += '\n'
        return s
