import pygame
from BoardRepresentation import Game
#defining some colors in RGB tuples
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,20,0)
GREEN = (0, 220,10)
BLUE = (50, 50, 150)
FPS = 10
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 450
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCALE = 40

import sys
import time
######################
    # FPS
class Chess_GUI(object):
	""" This class represents an instance of the game. If we need to
		reset the game we'd just need to create a new instance of this
		class. """
	def __init__(self, move_set=None):
		pygame.init()
		self.size = [SCREEN_WIDTH, SCREEN_HEIGHT]
		self.screen = pygame.display.set_mode(self.size)

		pygame.display.set_caption("Chess")
		pygame.mouse.set_visible(False)

		# Create our objects and set the data
		self.done = False
		self.clock = pygame.time.Clock()
		self.chess_game = Game()
		""" Constructor. Create all our attributes and initialize
		the game. """

		self.BackGround = Background('chess_board.jpg', [0, 0])
		self.score = 0
		self.game_over = False

		self.tiles = self.chess_game.board.tiles
		self.initialize_images()
		self.Move = 0

		self.move_set = move_set
		pygame.display.set_caption("Chess")
		pygame.mouse.set_visible(False)

	def initialize_images(self):
		self.white_king = pygame.image.load("images/white_king.gif").convert_alpha()
		self.white_king_rect = self.white_king.get_rect()

		self.white_bishop = pygame.image.load("images/white_bishop.gif").convert_alpha()
		self.white_bishop_rect = self.white_bishop.get_rect()

		self.white_queen = pygame.image.load("images/white_queen.gif").convert_alpha()
		self.white_queen_rect = self.white_queen.get_rect()

		self.white_rook = pygame.image.load("images/white_rook.gif").convert_alpha()
		self.white_rook_rect = self.white_rook.get_rect()

		self.white_pawn = pygame.image.load("images/white_pawn.gif").convert_alpha()
		self.white_pawn_rect = self.white_king.get_rect()

		self.white_knight = pygame.image.load("images/white_knight.gif").convert_alpha()
		self.white_king_rect = self.white_knight.get_rect()


		"""black"""
		self.black_king = pygame.image.load("images/black_king.gif").convert_alpha()
		self.black_king_rect = self.black_king.get_rect()

		self.black_queen = pygame.image.load("images/black_queen.gif").convert_alpha()
		self.black_queen_rect = self.white_queen.get_rect()

		self.black_bishop = pygame.image.load("images/black_bishop.gif").convert_alpha()
		self.black_bishop_rect = self.white_bishop.get_rect()

		self.black_rook = pygame.image.load("images/black_rook.gif").convert_alpha()
		self.black_rook_rect = self.white_rook.get_rect()

		self.black_pawn = pygame.image.load("images/black_pawn.gif").convert_alpha()
		self.black_pawn_rect = self.black_king.get_rect()

		self.black_knight = pygame.image.load("images/black_knight.gif").convert_alpha()
		self.black_king_rect = self.black_knight.get_rect()
		# # Create sprite lists
		# self.white_pieces = pygame.sprite.Group()
		# self.all_sprites_list = pygame.sprite.Group()
		#
		# # Create the block sprites
		# for i in range(50):
		# 	block = Block()
		#
		# 	block.rect.x = random.randrange(SCREEN_WIDTH)
		# 	block.rect.y = random.randrange(-300, SCREEN_HEIGHT)
		#
		# 	self.block_list.add(block)
		# 	self.all_sprites_list.add(block)

		# Create the player
		# self.player = Player()
		# self.all_sprites_list.add(self.player)
	def process_events(self):
		""" Process all of the events. Return a "True" if we need
			to close the window. """
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return True
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.game_over:
					self.__init__()

		return False

	def add_move(self, move):
		pass

	def step(self):
		if not self.game_over:
			# i = 0
			# while True:
				# while i <  len(self.move_set):

				# print([self.move_set[i]])
				self.done = self.process_events()
				self.display_frame(self.screen)
				self.clock.tick(10)
				input()

				# self.display_frame(self.screen)
				# self.clock.tick(10)
			# while i > len(self.move_set):
			# 	self.display_frame(self.screen)
			# 	self.clock.tick(10)
		if self.done == True:
			pygame.quit()

	def run_steps(self):
		i = 0
		while True:
			self.step()
			if i < len(self.move_set):
				self.chess_game.step(self.move_set[i])
				i += 1

	def run_random_step(self):
		if not self.game_over:
			i = 0
			x = ""
			while x != "x":

				# print([self.move_set[i]])
				self.done = self.process_events()
				self.display_frame(self.screen)
				self.clock.tick(1)
				# self.chess_game.board.evaluate_board()
				# self.chess_game.test_run_chess_notation([self.move_set[i]])
				# x = input()
				success = self.chess_game.random_step()
				self.chess_game.board.evaluate_board()

				# print(success)
				if success == False:
					time.sleep(100)
				i += 1
			if self.done == True:
				pygame.quit()
	def run_best_step(self):
		if not self.game_over:
			i = 0
			x = ""
			while x != "x":

				# print([self.move_set[i]])
				self.done = self.process_events()
				self.display_frame(self.screen)
				self.clock.tick(.5)
				# self.chess_game.board.evaluate_board()
				# self.chess_game.test_run_chess_notation([self.move_set[i]])
				# x = input()
				success = self.chess_game.best_step()
				self.chess_game.board.evaluate_board()

				# print(success)
				if success == False:
					time.sleep(100)
				i += 1
			if self.done == True:
				pygame.quit()
	def run_best_move(self):
		if not self.game_over:
			i = 0
			x = ""
			while x != "x":
				x = input()
				# print([self.move_set[i]])
				self.done = self.process_events()
				self.display_frame(self.screen)
				self.clock.tick(5)
				# self.chess_game.test_run_chess_notation([self.move_set[i]])
				self.chess_game.random_step()
				i += 1
			if self.done == True:
				pygame.quit()

	def display_frame(self, screen):
		""" Display everything to the screen for the game. """
		screen.fill([255, 255, 255])
		screen.blit(self.BackGround.image, self.BackGround.rect)
		i = 52
		for tile in self.tiles.items():
			index = tile[0]
			id = tile[1].get_piece_ID()
			xbuffer = 18
			ybuffer = 18
			# print(id)
			if id == 0:
				pass
			elif id == 1:
				screen.blit(self.white_king, [index[1] * i + xbuffer, index[0] * i + ybuffer])
			elif id == 2:
				screen.blit(self.white_queen, [index[1] * i + xbuffer, index[0] * i + ybuffer])
			elif id == 3:
				screen.blit(self.white_rook, [index[1] * i + xbuffer, index[0] * i + ybuffer])
			elif id == 4:
				screen.blit(self.white_bishop, [index[1] * i + xbuffer, index[0] * i + ybuffer])
			elif id == 5:
				screen.blit(self.white_knight, [index[1] * i + xbuffer, index[0] * i + ybuffer])
			elif id == 6:
				screen.blit(self.white_pawn, [index[1] * i + xbuffer, index[0] * i + ybuffer])
			elif id == -1:
				screen.blit(self.black_king, [index[1] * i + xbuffer, index[0] * i + ybuffer])
			elif id == -2:
				screen.blit(self.black_queen, [index[1] * i + xbuffer, index[0] * i + ybuffer])
			elif id == -3:
				screen.blit(self.black_rook, [index[1] * i + xbuffer, index[0] * i + ybuffer])
			elif id == -4:
				screen.blit(self.black_bishop, [index[1] * i + xbuffer, index[0] * i + ybuffer])
			elif id == -5:
				screen.blit(self.black_knight, [index[1] * i + xbuffer, index[0] * i + ybuffer])
			elif id == -6:
				screen.blit(self.black_pawn, [index[1] * i + xbuffer, index[0] * i + ybuffer])
		# if self.game_over:
		# 	font = pygame.font.SysFont("serif", 25)
		# 	text = font.render("Game Over, click to restart", True, BLACK)
		# 	center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
		# 	center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
		# 	screen.blit(text, [center_x, center_y])
		# if not self.game_over:
		# 	pass
		pygame.display.flip()


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location