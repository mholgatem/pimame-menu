import pygame
import subprocess
import re
import sys
import time
from os import system, remove, close, execl
from tempfile import mkstemp
from shutil import move

class PMUtil:
	@staticmethod
	def get_ip_addr():
		#wlan = subprocess.check_output("/sbin/ifconfig wlan0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'", shell=True)	#2>/dev/null
		#ether = subprocess.check_output("/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'", shell=True)
		
		# i like this better : it won't complain if the interface doesn't exist
		wlan = subprocess.check_output("ip addr show wlan0 2>/dev/null | awk '/inet/ {print $2}' | cut -d/ -f1", shell=True)
		ether = subprocess.check_output("ip addr show eth0 2>/dev/null | awk '/inet/ {print $2}' | cut -d/ -f1", shell=True)
		
		myip = ''
		if wlan != '':
			myip += wlan
		if ether != '':
			myip += ' ' + ether

		m = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", myip)
		myip = m.group(0)

		return "IP: "+myip

	@staticmethod
	def run_command_and_continue(command):
		pygame.quit()
		time.sleep(1)
		command = command.split("%%")
		if command[0] == "QUIT":
			pygame.quit()
			sys.exit()
			
		system(command[0] + " && export LD_LIBRARY_PATH= ")
		
		#restart piplay
		python = sys.executable
		sys.argv = [sys.argv[0]]
		if len(command) > 1:
			sys.argv.append("--quicklaunch")
			sys.argv.append(command[1])
			
			
		execl(python, python, * sys.argv)
		
		#not used?
		sys.exit()
	
	@staticmethod
	def replace(file_path, pattern, subst, prefix = None):
		#rewrite config.yaml file
		#Create temp file
		file_number, abs_path = mkstemp()
		new_file = open(abs_path,'wb')
		old_file = open(file_path)
		
		pattern = str(pattern)
		subst = str(subst)
		
		pattern = pattern.replace('True', 'Yes')
		pattern = pattern.replace('False', 'No')
		subst = subst.replace('True', 'Yes')
		subst = subst.replace('False','No')
		
		for line in old_file:
			line = line.replace(':"', ': "')
			if prefix and prefix in line:
				line = (line.split(prefix)[0] + prefix.strip() + " " + subst + '\n')
			elif prefix == None:
				line = (line.replace(pattern, subst))
			new_file.write(line)
		#close temp file
		new_file.close()
		close(file_number)
		old_file.close()
		#Remove original file
		remove(file_path)
		#Move new file
		move(abs_path, file_path)
	
	@staticmethod
	def fade_out(self, run_effect = True):
		if run_effect:
			background = pygame.Surface([self.screen.get_width(), self.screen.get_height()]).convert()
			background.fill((0,0,0))
			background.set_alpha(80)
			#background.convert()
			for x in xrange(1,6):
				self.screen.blit(background, (0,0))
				pygame.display.update()
			return "fade_out"
		pygame.display.update()
		return "no_effect"
		
	@staticmethod
	def fade_in(self, run_effect = True):
		if run_effect:
			backup = pygame.Surface.copy(self.screen).convert()
			self.screen.fill((0,0,0))
			backup.set_alpha(80)
			for x in xrange(1,6):
				self.screen.blit(backup, (0,0))
				pygame.display.update()
			backup.set_alpha(None)
			self.screen.blit(backup, (0,0))
			pygame.display.update()
			return "fade_in"
		pygame.display.update()
		return "no_effect"
		
	@staticmethod
	def fade_into(self, prev_screen, run_effect = True):
		if run_effect:
			backup = pygame.Surface.copy(self.screen).convert()
			self.screen.blit(prev_screen, (0,0))
			backup.set_alpha(80)
			for x in xrange(1,6):
				self.screen.blit(backup, (0,0))
				pygame.display.update()
			backup.set_alpha(None)
			self.screen.blit(backup, (0,0))
			pygame.display.update()
			return "fade_into"
		pygame.display.update()
		return "no_effect"
			
	@staticmethod
	def offset_fade_into(self, prev_screen, offset, run_effect = True, duration = 6):
		if run_effect:
			backup = pygame.Surface.copy(self.screen).convert()
			self.screen.blit(prev_screen, (0,0))
			backup.set_alpha(255 / (duration/2))
			if len(offset) > 2:
				kwargs = {'dest': offset, 'area': offset}
			for x in xrange(1, duration):
				self.screen.blit(backup, **kwargs)
				pygame.display.update(offset)
			backup.set_alpha(None)
			self.screen.blit(backup, **kwargs)
			pygame.display.update()
			return "fade_into"
		pygame.display.update(offset)
		return "no_effect"
	
	@staticmethod
	def blurSurf(surface, amt):
		if amt < 1.0:
			raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt)
		scale = 1.0/float(amt)
		surf_size = surface.get_size()
		scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
		surf = pygame.transform.smoothscale(surface, scale_size)
		surf = pygame.transform.smoothscale(surf, surf_size)
		return surf
	
	@staticmethod
	def glass(surface, color, rect):
		if len(color) > 3 and (0 < color[3] < 255):
			amt = 20
			scale = 1.0/float(amt)
			
			backup = pygame.Surface((rect.w,rect.h), pygame.SRCALPHA, 32).convert_alpha()
			backup.blit(surface, (0,0), rect)
			
			backup_size = backup.get_size()
			scale_size = (int(backup_size[0]*scale), int(backup_size[1]*scale))
			
			backup = pygame.transform.smoothscale(backup, scale_size)
			backup = pygame.transform.smoothscale(backup, backup_size)
			
			temp = pygame.Surface((rect.w,rect.h), pygame.SRCALPHA, 32).convert_alpha()

			temp.fill(color)
			backup.blit(temp,(0,0))
			return backup
				
		backup = pygame.Surface((rect.w,rect.h)).convert_alpha()
		backup.blit(surface, rect, rect)
		backup.fill(color)
		return backup
