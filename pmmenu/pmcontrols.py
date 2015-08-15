import pygame
import yaml

class PMControls:
	#check out for key reference - http://www.pygame.org/docs/ref/key.html
	KEYBOARD = {}
	JOYSTICK = {}
	
	KEY_EVENT = [pygame.KEYDOWN, pygame.KEYUP]
	JOY_BUTTON_EVENT = [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP]
	MOUSE_BUTTON_EVENT = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]
	
	def __init__(self):
		pygame.key.set_repeat(300, 20)
		self.joystick_repeat = (300, 40)
		self.joystick_repeat_start = None
		
		pygame.joystick.init()
		self.js_count = pygame.joystick.get_count()
		self.js = []
		for i in range(self.js_count):
			self.js.append(pygame.joystick.Joystick(i))
			self.js[i].init()
		
		
		#load config file, use open() rather than file(), file() is deprecated in python 3.
		stream = open('/home/pi/pimame/pimame-menu/controller.yaml', 'r')
		contr = yaml.safe_load(stream)
		stream.close()
		
		#KICKSTARTER COMBO
		contr['KEYBOARD']['KICKSTARTER'] = ["[pygame.K_k, pygame.K_s]"]
		
		
		#KEYBOARD CONFIG
		for key, value in contr['KEYBOARD'].iteritems():
			for entry in value:
				#convert string to pygame.key
				try:
					entry = "entry = " + entry
					exec entry
				except:
					print "INVALID CONTROLLER CONFIG: {!r}: {!r}".format(key, value)
					
				#generate list of 'unpressed' keys
				key_list = ([0] * len(pygame.key.get_pressed()))
				try:
					test = entry + 1
					key_list[entry] = 1
					
				except:
					for item in entry:
						key_list[item] = 1

				self.KEYBOARD[str(tuple(key_list))] = key
		
		#JOYSTICK CONFIG
		
		#AXIS CONFIG
		for key, value in contr['JOYSTICK']['DIRECTIONAL'].iteritems():
			if key == "RIGHT" or key == "LEFT":
				value = str(contr['JOYSTICK']['HORIZONTAL_AXIS']) + "|" + str(value)
			elif key == "UP" or key == "DOWN":
				value = str(contr['JOYSTICK']['VERTICAL_AXIS'])  + "|" + str(value)
				
			self.JOYSTICK[str(value)] = key
		
		#BUTTON CONFIG
		for key, value in contr['JOYSTICK']['BUTTONS'].iteritems():
			button_count = 100
			button_list = ([0] * button_count)
			
			try:
				test = value + 1
				button_list[value] = 1
				
			except:
				for item in value:
					button_list[item] = 1
					
			value = button_list
			self.JOYSTICK[str(value)] = key
		
		self.AXIAL_DRIFT = contr['OPTIONS']['AXIS_DRIFT_TOLERANCE']
	
	def get_action(self, input_test = [pygame.KEYDOWN, pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION], events = None):
		if not events:
			events = pygame.event.get(input_test)
		action = None
		#JOYSTICK MOTION REPEATER
		try:
			if pygame.JOYAXISMOTION in input_test:
				if self.joystick_repeat_start and pygame.time.get_ticks() - self.joystick_repeat_start >= self.joystick_repeat[0]:
					for joy in self.js:
						for axis in range(joy.get_numaxes()):
							if abs(joy.get_axis(axis)) > self.AXIAL_DRIFT:
								self.joystick_repeat_start += self.joystick_repeat[1] #add repeat rate to start time
								action = self.JOYSTICK[str(axis) + "|" + str( int(joy.get_axis(axis) / abs(joy.get_axis(axis))))]
		except KeyError:
			pass
		
		#EVENTS
		for event in events:
			if event.type in input_test:
				try:
					#KEYBOARD
					if event.type in self.KEY_EVENT:
						#KEYDOWN
						if event.type == pygame.KEYDOWN:
							action = self.KEYBOARD[str(pygame.key.get_pressed())]
						else:
							#KEYUP -> check for combos
							keys_pressed = ([0] * len(pygame.key.get_pressed()))
							for test_event in events:
								if test_event.type == pygame.KEYUP:
									keys_pressed[test_event.key] = 1
							action = self.KEYBOARD[str(tuple(keys_pressed))]
						break
					#JOYSTICK MOVEMENT
					elif event.type == pygame.JOYAXISMOTION:
						if abs(event.value) > self.AXIAL_DRIFT:
							action = self.JOYSTICK[str(event.axis) + "|" + str( int(event.value / abs(event.value)))]
							self.joystick_repeat_start = pygame.time.get_ticks()
					#JOYSTICK BUTTONS
					elif event.type in self.JOY_BUTTON_EVENT:
						#JOY BUTTON DOWN
						if event.type == pygame.JOYBUTTONDOWN:
							joy_buttons = ([0] * 100)
							for i in xrange(0,self.js[event.joy].get_numbuttons()):
								button = self.js[event.joy].get_button( i )
								if button: joy_buttons[ i ] = 1
							action = self.JOYSTICK[str(joy_buttons)]
						else: #JOY BUTTON UP -> check for combos
							joy_buttons = ([0] * 100)
							for test_event in events:
								if test_event.type == pygame.JOYBUTTONUP: joy_buttons[ test_event.button ] = 1
							action = self.JOYSTICK[str(joy_buttons)]
					#MOUSE CLICK
					elif event.type in self.MOUSE_BUTTON_EVENT:
						action = "MOUSEBUTTON"
					#MOUSE MOVE
					elif event.type == pygame.MOUSEMOTION:
						action = "MOUSEMOVE"
				except KeyError:
					pass

		return action