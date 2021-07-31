import pygame
from random import shuffle, randint
from copy import deepcopy
from typing import Optional, List, Dict, Tuple, Iterator

class Grid:
    def __init__(self, difficulty: str) -> None:
        self.DEFAULT_GRID: List[List[int]] = [[0 for _ in range(9)] for _ in range(9)]
        self.puzzle: List[List[int]] = deepcopy(self.DEFAULT_GRID)
        self.grid: List[List[int]] = deepcopy(self.DEFAULT_GRID)
        self.notes: List[List[List[int]]] = [deepcopy(self.DEFAULT_GRID) for _ in range(9)]

        self.known_cells_counts: Dict[str, Tuple[int, int]] = {
            "easy": (51, 59),
            "medium": (42, 50),
            "hard": (25, 41),
            "evil": (17, 24)
        }
        self.known_cells_count: int = randint(
            self.known_cells_counts[difficulty][0],
            self.known_cells_counts[difficulty][1]
        )
        self.filled: bool = False
        self.assign_mode: bool = True
        self.note_mode: bool = False

        self.number_assets: Dict[str, Dict[int, pygame.Surface]] = {}
        self.modes_assets: Dict[str, pygame.Surface] = {}
        
        self.initialize_assets()
        self.generate_puzzle(self.known_cells_count)

    def initialize_assets(self) -> None:
        master_input_mode_asset: pygame.Surface = pygame.image.load("../assets/input_modes.png")
        MODE_SPRITE_SIZE: Tuple[int, int] = (90, 90)
        for x, mode in enumerate(["note", "fill", "delete"]):
            COORDINATES: Tuple[int, int] = (x * 90, 0)
            self.modes_assets[mode] = master_input_mode_asset.subsurface(COORDINATES, MODE_SPRITE_SIZE)

        for x in range(1, 10):
            DIGIT_SIZE: Tuple[int, int] = (30, 30)
            SUB_COORDS: Tuple[int, int] = (x * 30, 0)
            self.number_assets["notes"][x] = (
                pygame.image.load("../assets/note_numbers.png").subsurface(SUB_COORDS, DIGIT_SIZE)
            )

        for y, category in enumerate(["known", "input", "invalid", "filled"]):
            for num in range(1, 10):
                DIGIT_SIZE: Tuple[int, int] = (90, 90)
                SUB_COORDS: Tuple[int, int] = ((num - 1) * 90, y * 90)
                self.number_assets[category][num] = (
                    pygame.image.load("../assets/numbers.png").subsurface(SUB_COORDS, DIGIT_SIZE)
                )

    def get_cell_asset(self, row, column) -> Optional[pygame.Surface]:
        num: int = self.grid[row][column]
        if num == 0:
            return
        
        if not self.cell_is_valid(row, column):
            return self.number_assets["invalid"][num]
        if self.grid_is_valid():
            return self.number_assets["filled"][num]

        if self.puzzle[row][column] == num:
            return self.number_assets["known"][num]
        elif self.puzzle[row][column] == 0:
            return self.number_assets["input"][num]

    def get_mode_asset(self, row, column) -> pygame.Surface:
    

    @staticmethod
    def shuffled_range(start: int, end: int) -> Iterator[int]:
        result: List[int] = [num for num in range(start, end)]
        shuffle(result)
        for num in result:
            yield num

    # Check duplicates in row at index.
    def row_is_valid(self, row_index: int) -> bool:
        seen: list = []
        for i in self.grid[row_index]:
            if i not in seen and i != 0:
                seen.append(i)
            elif i in seen:
                return False
        return True

    # Check duplicates in column at index.
    def column_is_valid(self, column_index: int) -> bool:
        column: list = [self.grid[i][column_index] for i in range(9)]
        seen: list = []
        for i in column:
            if i not in seen and i != 0:
                seen.append(i)
            elif i in seen:
                return False
        return True

    # Check duplicates in 3x3 subgrid at index.
    def subgrid_is_valid(self, row: int, column: int) -> bool:
        subgrid_x: int = 0 if row <= 2 else (3 if row <= 5 else 6)
        subgrid_y: int = 0 if column <= 2 else (3 if column <= 5 else 6)
        subgrid: list = [
            self.grid[y][x] for x in range(subgrid_x, subgrid_x + 3) for y in range(subgrid_y, subgrid_y + 3)
        ]
        seen: list = []
        for i in subgrid:
            if i not in seen and i != 0:
                seen.append(i)
            elif i in seen:
                return False
        return True

    # Wrapper function to check for a location and surrounding region's validity
    def cell_is_valid(self, row: int, column: int) -> bool:
        return (
            self.row_is_valid(row)
            and self.column_is_valid(column)
            and self.subgrid_is_valid(row, column)
        )

    # Function to check the validity of the whole player_grid
    def grid_is_valid(self) -> bool:
        for i in range(9):
            for j in range(9):
                if (
                    self.grid[i][j] == 0
                    or not self.row_is_valid(i)
                    or not self.column_is_valid(j)
                    or not self.subgrid_is_valid(i, j)
                ):
                    return False
        return True

    # Solve function using backtracking.
    def solve_grid(self) -> bool:
        for row in range(9):
            for column in range(9):
                if not self.cell_is_valid(row, column):
                    self.grid[row][column] = 0
                if self.grid[row][column] == 0:
                    for num in self.shuffled_range(1, 10):
                        self.grid[row][column] = num
                        if self.cell_is_valid(row, column) and self.solve_grid():
                            return True
                        self.grid[row][column] = 0
                    return False
        self.grid_filled = True
        return True

    def generate_puzzle(self, known_cells_count: int) -> None:
        self.solve_grid()
        self.puzzle = deepcopy(self.grid)
        coordinates: List[Tuple[int, int]] = [
            (y, x) for x in self.shuffled_range(0, 9) for y in self.shuffled_range(0, 9)
        ]
        shuffle(coordinates)
        for _ in range(81 - known_cells_count):
            remove_coord: Tuple[int, int] = coordinates.pop()
            self.grid[remove_coord[0]][remove_coord[1]] = 0
            self.puzzle[remove_coord[0]][remove_coord[1]] = 0

    def switch_input_mode(self) -> None:
        self.assign_mode = not self.assign_mode
        self.note_mode = not self.note_mode

    def assign_to_grid(self, row: int, column: int, num: int) -> None:
        if self.assign_mode:
            self.grid[row][column] = num
            self.notes[row][column].clear()
        elif self.note_mode:
            if not num in self.notes[row][column]:
                self.notes[row][column].append(num)
            self.grid[row][column] = 0

    def delete_from_grid(self, row: int, column: int) -> None:
        self.grid[row][column] = 0
        self.notes[row][column].clear()