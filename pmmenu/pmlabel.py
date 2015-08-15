import pygame


class PMLabel(pygame.sprite.Sprite):
	def __init__(self, label_text, font, color_fg, color_bg = (0,0,0,0), font_bold = False, max_text_width = False, outline_color = pygame.Color(0,0,0,0), emboss = False):
		pygame.sprite.Sprite.__init__(self)

		
		self.text = label_text
		self.color_fg = color_fg
		self.font = font
		
		#pygame faux bold font
		font.set_bold(font_bold)
		if outline_color.a:
			text = self.outline(label_text, font, color_fg, outline_color, emboss)
		else:
			text = font.render(label_text, 1, color_fg).convert_alpha()
		text_rect = text.get_rect()
		
		if max_text_width and text_rect.w > max_text_width:
			scale = float(max_text_width) / text_rect.w
			text = pygame.transform.smoothscale(text, (int(max_text_width), int(text_rect.h * scale)))
			text_rect = text.get_rect()
		#make text smoother
		text.blit(text, text_rect)

			
		if label_text == '': text_rect.w = 0
		self.image = pygame.Surface([text_rect.w, text_rect.h]).convert_alpha()
		self.image.fill(color_bg, text_rect)
		
		if color_fg.a:
			self.image.blit(text, (0,0))
		
		self.rect = self.image.get_rect()
	
	# Do a simple drop-shadow on text, with a darker color offset by a certain
	# number of pixels.
	def outline(self, text, font, color, color2, emboss):
		# Allow integers or fonts for 'font'.
		offset = font.get_linesize() / 20
		if isinstance(font, int): font = pygame.font.Font(None, font)
		if color2 == None: color2 = [c / 7 for c in color]
		t1 = font.render(text, True, color)
		t2 = font.render(text, True, color2)
		s = pygame.Surface([i + (offset * 2) for i in t1.get_size()], pygame.SRCALPHA, t1)
		for x in (0, offset + (offset * (not emboss))):
			for y in (0, offset + (offset * (not emboss))):
				s.blit(t2, [x,y])
		s.blit(t1, (offset, offset))
		return s
		
class PMSprite(pygame.sprite.Sprite):
	def __init__(self, image_surface):
		pygame.sprite.Sprite.__init__(self)
		
		self.image = image_surface
		self.rect = self.image.get_rect()
		