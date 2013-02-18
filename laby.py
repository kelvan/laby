#!/usr/bin/env python

#import everything
import os, pygame, time, glob
from pygame.locals import *
from GameObject import GameObject
from player import player
from level import level
from save import save

def centered_txt(screen, lvl, txt, font_size):
	font = pygame.font.Font(None, font_size)
	text = font.render( txt, 1, ( 255, 255, 255 ), ( 0, 0, 0 ) )
	size = font.size( txt )
	text_pos = ( ( ( lvl.esize * len(lvl.lvl[0]) ) / 2) - size[0] / 2, ( ( lvl.esize * len(lvl.lvl) )/2 ) - size[1] / 2)
	screen.blit( text, text_pos )
	pygame.display.update()

#quick function to load an image
def load_image(name):
    path = os.path.join('data', name)
    return pygame.image.load( path ).convert()

def image(s):
	img={}
	img['player'] = load_image('player' + s + '.png')
	img['#'] = load_image('block' + s + '.png')
	img['S'] = load_image('start' + s + '.png')
	img['E'] = load_image('end' + s + '.png')
	img['_'] = load_image('space' + s + '.png')
	img['$'] = load_image('dollar' + s + '.png')
	return img

def main():

	esize = 16
	lvl = level("level0.lvl", esize)
	
	l = glob.glob("data/*.lvl")
	lvl_anz = len(l)

	try:
		pygame.mixer.init()
		music=pygame.mixer.Sound(os.path.join('data', "music.ogg"))
	except:
		print "No Sound avaiable"
	pygame.init()
	screen = pygame.display.set_mode((lvl.esize*len(lvl.lvl[0]), lvl.esize*len(lvl.lvl)))
	
	img = image(str(esize))

	try:
		music.play(1)
	except:
		pass

	pygame.key.set_repeat(80, 50)
	for i in range(lvl_anz):
		play=player()
		lvl = level("level" + str(i) + ".lvl", esize)
		objects = []
		screen = pygame.display.set_mode((lvl.esize*len(lvl.lvl[0]), lvl.esize*len(lvl.lvl)))
		for y in range(len(lvl.lvl)):
			objects.append([])
			for x in range(len(lvl.lvl[0])):
				o = GameObject(img[lvl.lvl[y][x]], x*lvl.esize, y*lvl.esize, screen)
				objects[y].append(o)
				if lvl.lvl[y][x] == 'S':
					pl = GameObject(img['player'], x*lvl.esize, y*lvl.esize, screen)

		btime = time.time()

		while not play.finish:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						txt = "Closing ..."
						centered_txt(screen, lvl, txt, 50)
						music.fadeout(2100)
						time.sleep(2)
						return
					if event.key == pygame.K_DOWN:
						pl.move(0, 1, lvl, img, objects, play)
					if event.key == pygame.K_UP:
						pl.move(0, -1, lvl, img, objects, play)
					if event.key == pygame.K_RIGHT:
						pl.move(1, 0, lvl, img, objects, play)
					if event.key == pygame.K_LEFT:
						pl.move(-1, 0, lvl, img, objects, play)
					if event.key == pygame.K_n:
						pass
						play.finish = 1
						
			for j in range(len(objects)):
				for o in objects[j]:
					o.draw()
				pl.draw()
			time.sleep(0.08)
			pygame.display.update()

		dtime = time.time() - btime			
		sav = save("User")
		sav.write(play.points, pl.moves, dtime)
		print "Ziel erreicht:", play.points, "gesammelt"
		print "Moves:", pl.moves
		print dtime

		won = 1

		try:
			if lvl.conf['moves'] > 0:
				if pl.moves < lvl.conf['moves']:
					print "moves OK"
				else:
					print "too many steps"
					won = 0
		except:
			print "Maximal moves not given"
			
		try:	
			if lvl.conf['time'] > 0:
				if dtime < lvl.conf['time']:
					print "time OK"
				else:
					print "too slow"
					won = 0
		except:
			print "Maximal time not given"

		try:
			if lvl.conf['points'] > 0:
				if play.points > lvl.conf['points']:
					print "points OK"
				else:
					print "not enought points"
					won = 0
		except:
			print "Minimal points not given"

		if won == 1:
			print "You finished this level"

		if i < lvl_anz - 1:
			txt = "Next level ..."
			centered_txt(screen, lvl, txt, 50)
			time.sleep(1)


	txt = "Finished ..."
	centered_txt(screen, lvl, txt, 50)
	music.fadeout(2100)
	time.sleep(2)


if __name__ == '__main__':
    main()
