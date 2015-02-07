import os
import pygame
from pmlabel import *

class PMSelection(pygame.sprite.Sprite):
	def __init__(self, global_opts):
		pygame.sprite.Sprite.__init__(self)

	def update(self, menu_item, global_opts):
		#pygame.sprite.Sprite.__init__(self)

		screen_width = pygame.display.Info().current_w
		item_width = ((screen_width - global_opts.padding) / global_opts.num_items_per_row) - global_opts.padding

		self.image = pygame.Surface([item_width, global_opts.item_height], pygame.SRCALPHA, 32).convert_alpha()

		
		item_rect = menu_item.rect
		if menu_item.icon_selected:
			icon = menu_item.pre_loaded_selected_icon.copy()
			
			# resize and center icon:
			icon_size = icon.get_size()
			text_align = icon_size[0]
			avail_icon_width = item_width - global_opts.padding * 2
			avail_icon_height = global_opts.item_height - global_opts.padding * 2
			while True:
				icon_width = icon_size[0]
				icon_height = icon_size[1]
				icon_ratio = float(icon_height) / float(icon_width)
				icon_width_diff = avail_icon_width - icon_width
				icon_height_diff = avail_icon_height - icon_height
				if icon_width_diff < icon_height_diff:
					diff = icon_width_diff
					icon_size = (icon_width + diff, icon_height + diff * icon_ratio)
				else:
					diff = icon_height_diff
					icon_size = (icon_width + diff / icon_ratio, icon_height + diff)

				icon_size = (int(icon_size[0]), int(icon_size[1]))

				if icon_size[0] <= avail_icon_width and icon_size[1] <= avail_icon_height:
					break


			
			#ReDraw label ontop of menu_item 
			if global_opts.display_labels:
				label = PMLabel(menu_item.label, global_opts.label_font, global_opts.label_font_selected_color, global_opts.label_background_selected_color, global_opts.label_font_selected_bold, global_opts.label_max_text_width)
				textpos = label.rect
				if global_opts.label_text_align == 'right': textpos.x = text_align - label.rect.w + global_opts.labels_offset[0]
				elif  global_opts.label_text_align == 'center': textpos.x = ((text_align - label.rect.w)/2) + global_opts.labels_offset[0]
				else: textpos.x = global_opts.labels_offset[0]
				textpos.y = global_opts.labels_offset[1]

				icon.blit(label.image, textpos)
			
			#ReDraw rom-count ontop of menu_item
			if global_opts.display_rom_count:
				if menu_item.rom_path and menu_item.num_roms != 0:

					label = PMLabel(str(menu_item.num_roms) + menu_item.warning, global_opts.rom_count_font, global_opts.rom_count_font_selected_color, global_opts.rom_count_background_selected_color, global_opts.rom_count_font_selected_bold, global_opts.rom_count_max_text_width)
					textpos = label.rect
					
					if global_opts.rom_count_text_align == 'right': textpos.x = text_align - label.rect.w + global_opts.rom_count_offset[0]
					elif  global_opts.rom_count_text_align == 'center': textpos.x = ((text_align - label.rect.w)/2) + global_opts.rom_count_offset[0]
					else: textpos.x = global_opts.rom_count_offset[0]
					textpos.y = global_opts.rom_count_offset[1]

					icon.blit(label.image, textpos)
						
			icon = pygame.transform.smoothscale(icon, icon_size)
			self.image.blit(icon, ((avail_icon_width - icon_size[0]) / 2 + global_opts.padding, (avail_icon_height - icon_size[1]) / 2 + global_opts.padding))
			
			self.rect = self.image.get_rect()
		self.rect.x = item_rect.x;
		self.rect.y = item_rect.y;
