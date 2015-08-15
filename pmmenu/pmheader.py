import os
import pygame
from  pmutil import *
from pmlabel import *

class PMHeader(pygame.sprite.Sprite):
	def __init__(self, opts, logo_align=('center', 'top'), ip_align = ('right','top'), update_align = ('left', 'top')):
		pygame.sprite.Sprite.__init__(self)

		
		self.logo_align = logo_align
		self.ip_align = ip_align
		self.update_align = update_align
		self.opts = opts
		
		#Build Header Background
		header_width = pygame.display.Info().current_w
		header_height = self.opts.header_height
		self.image = pygame.Surface([header_width, header_height], pygame.SRCALPHA, 32).convert_alpha()
		background_image = self.opts.pre_loaded_background
		self.image.blit(background_image, (0,0))
		if self.opts.header_color.a:
			self.image.fill(self.opts.header_color)
		self.rect = self.image.get_rect()
		
		self.logo = self.get_logo()
		self.ip = self.get_ip()
		self.update = self.get_update()
		self.set_alignment_order()

		self.details = pygame.sprite.Group()
		self.details.add([self.logo, self.ip, self.update])
		
		self.details.draw(self.image)
		
	
	def set_alignment_order(self):
		
		for item in [(self.logo, self.logo_align), (self.ip, self.ip_align), (self.update, self.update_align)]:
			x, y = item[1]
		
			if x == 'left': item[0].rect.left = self.rect.left
			elif x == 'center': item[0].rect.centerx = self.rect.centerx
			elif x == 'right': item[0].rect.right = self.rect.right
			
			if y == 'top': item[0].rect.top = self.rect.top
			elif y == 'center': item[0].rect.centery = self.rect.centery
			elif y == 'bottom': item[0].rect.bottom = self.rect.bottom
		
		if self.ip.rect.colliderect(self.logo.rect): self.ip.rect.top = self.logo.rect.bottom
		if self.update.rect.colliderect(self.logo.rect): self.update.rect.top = self.logo.rect.bottom
		if self.update.rect.colliderect(self.ip.rect): self.update.rect.top = self.ip.rect.bottom
		
	def get_logo(self):
		logo_file_path = self.opts.theme_pack + self.opts.logo_image
		return PMSprite(self.opts.load_image(logo_file_path))
		
	def get_ip(self):
		displayString = ''

		if self.opts.show_ip:
			try:
				displayString = PMUtil.get_ip_addr()
			except:
				displayString = "No Network Connection"

			return PMLabel(displayString, self.opts.font, self.opts.default_font_color, self.opts.default_font_background_color, outline_color = self.opts.default_font_outline_color)
			
			
	def get_update(self):
		displayString = ''

		if self.opts.show_update:
			user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0"}
			try:
				import requests
				version_web = float( requests.get('http://www.piplay.org/version', headers = user_agent).text)
				version_current = float(open("../version", 'r').read())
				if version_current < version_web:
					displayString = "New Version Available"
			except:
				displayString = "Could not check for updates"

			return PMLabel(displayString, self.opts.font, self.opts.default_font_color, self.opts.default_font_background_color, outline_color = self.opts.default_font_outline_color)
			