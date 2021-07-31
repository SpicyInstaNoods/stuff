import pygame
from typing import Tuple, List, Dict
from Grid import Grid

class Game:
	def __init__(self) -> None:
		self.gameplay_size: Tuple[int, int] = (90 * 9, 90 * 9)
		self.display_surface: pygame.Surface = pygame.display.set_mode((600, 900))
		self.cell_background_rgb: Dict[str, Tuple[int, int, int, int]] = {
			"easy": (5, 15, 0, 255),
			"medium": (40, 30, 0, 255),
			"hard": (41, 7, 0, 255),
			"evil": (14, 0, 41, 255)
		}
		self.player_grid: Grid

	def draw_diff_select_screen(self) -> None:
		WHITE: Tuple[int, int, int, int] = (255, 255, 255, 255)
		select_panel: pygame.Surface = pygame.image.load("../assets/difficulty_select.png")
		self.display_surface.blit(select_panel, (0, 0))
		for y in range(4):
			pygame.draw.rect(self.display_surface, (0, y * 225, 600, 226), WHITE, 1)
		pygame.draw.rect(self.display_surface, (0, 899, 600, 1), WHITE, 0)
		pygame.display.update()

	def set_input_difficulty(self) -> None:
		def approx_mouse_pos() -> int:
			DIFF_SPRITE_SIZE: int = 150
			mouse_pos_y: int = pygame.mouse.get_pos()[1]
			return (mouse_pos_y - (mouse_pos_y % DIFF_SPRITE_SIZE)) // DIFF_SPRITE_SIZE
		
		self.draw_diff_select_screen()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit(0)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					difficulty_levels: Tuple[str, str, str, str] = ("easy", "medium", "hard", "evil")
					selected_diff_pos: int = approx_mouse_pos()
					self.player_grid = Grid(difficulty_levels[selected_diff_pos])
					return

	def draw_waiting_enter_keypress(self) -> None:
		enter_image: pygame.Surface = pygame.image.load("../assets/press_enter_signal.png")
		self.display_surface.blit(enter_image, (90 * 8, 90 * 7))
		pygame.display.update()

	def draw_playing_grid(self) -> None:
		for row in range(9):
			for column in range(9):
				COORDINATES: Tuple[int, int] = (row * 90, column * 90)
				self.display_surface.blit(self.player_grid.get_cell_asset(row, column), COORDINATES)

		mode_icon: pygame.Surface = pygame.image.load("../assets/mode_icon.png")
		