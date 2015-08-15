import argparse
import pygame
import os
from pmmenu import pmmenu
from pmmenu.pmconfig import *
from pmmenu.scenemanager import *
from pmmenu.mainscene import *
from pmmenu.romlistscene import *


parser = argparse.ArgumentParser(description='PiPlay')
parser.add_argument("--quicklaunch", metavar="integer", help="Which platform to skip to", type=int)
parser.add_argument("--auto_exec", metavar="command", default=None, help="auto execute command on launch, use [--auto_exec select] to choose the command to auto run", type=str)
parser.add_argument('--clear', dest='clear', help="Clear console on PiPlay launch", action='store_true')
parser.add_argument('--no_clear', dest='clear', help="Don't clear console on PiPlay launch", action='store_false')
parser.set_defaults(clear=True)
args = parser.parse_args()

#cd to path that this file resides in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def main(args):
	if args.clear:
		system('clear')
	cfg = PMCfg()
	controls = PMControls()
	pygame.event.get()
	if args.auto_exec and args.auto_exec.lower() != 'select' and not pygame.key.get_pressed()[pygame.K_LSHIFT]:
		cfg.close_database_connections()
		PMUtil.run_command_and_continue(args.auto_exec)
	
	pygame.display.set_caption('PiPlay')
	
	timer = pygame.time.Clock()
	running = True
	full_screen_refresh_timer = 0
	full_screen_refresh_rate= cfg.options.max_fps * 5
	
	if args.quicklaunch:
		manager = SceneManager(cfg, MainScene(), False)
		for sprite in manager.scene.menu_style:
			if sprite.id == args.quicklaunch:
				print "Relaunch", sprite.label
				manager.go_to(RomListScene(sprite.get_rom_list(), sprite.id))
	else:
		manager = SceneManager(cfg, MainScene())
	
	while running:
		timer.tick(cfg.options.max_fps)
		action = controls.get_action()
		
		if action == 'QUIT':
			pygame.quit()
			sys.exit()
		
		update_display = []
		if action: 
			update_display = manager.scene.handle_events(action)
			if update_display: 
				pygame.display.update(update_display)
				manager.scene.update_display = []
			
		full_screen_refresh_timer += 1
		if full_screen_refresh_timer >= full_screen_refresh_rate:
			full_screen_refresh_timer = 0
			pygame.display.flip()
		pygame.event.clear()
		
		

if __name__ == "__main__":
	main(args)
