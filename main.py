import pygame
import random
import os

class PicMan:
    def __init__(self):
        pygame.init()
        self.screen_width = 720
        self.screen_height = 720
        self.CELL_SIZE = 60
        self.FPS = 60
        self.character_x = 10
        self.character_y = 10
        self.points = 0
        self.running = True
        self.game_state = "running"

        self.enemy_move_counter = 0
        self.enemy_move_interval = 10
        self.enemies = [{"x": 1, "y": 1}, {"x": 7, "y": 5}]

        self.ROAD_COLOR = (201, 211, 189)
        self.WALL_COLOR = (123, 147, 164)
        self.TEXT_COLOR = (255, 255, 255)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.SysFont("Times New Roman", 24)
        pygame.display.set_caption("PIC-MAN")
        self.load_images()
        self.start_new_game()

    def start_new_game(self):
        self.map =  ["############",
                     "#..........#",
                     "#.##.###.#.#",
                     "#.#...#..#.#",
                     "#...#...##.#",
                     "#..##.#....#",
                     "#...#.##.#.#",
                     "#.#....#.#.#",
                     "#.#.##.....#",
                     "#.#.#..###.#",
                     "#.........0#",
                     "############",
                    ]
        
    def draw_map(self):
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == "#":
                    self.screen.blit(self.wall_image, (x * self.CELL_SIZE, y * self.CELL_SIZE))
                elif cell == ".":
                    self.screen.blit(self.path_image, (x * self.CELL_SIZE, y * self.CELL_SIZE))
                    coin_size = self.item_image.get_width()
                    offset = (self.CELL_SIZE - coin_size) // 2
                    self.screen.blit(self.item_image, (x * self.CELL_SIZE + offset, y * self.CELL_SIZE + offset))
                elif cell == "0":
                    self.screen.blit(self.path_image, (x * self.CELL_SIZE, y * self.CELL_SIZE))

    def load_images(self):
        character_scale = 0.9
        character_proportion = 1.1
        item_scale = 0.35
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        character_size = int(self.CELL_SIZE * character_scale)
        character_path = os.path.join(current_dir, "character.png")
        self.character_image = pygame.transform.scale(pygame.image.load(character_path), (character_size * character_proportion, character_size))
        
        enemy_path = os.path.join(current_dir, "enemy.png")
        self.enemy_image = self.scale_image(pygame.image.load(enemy_path))
        
        item_size = int(self.CELL_SIZE * item_scale)
        item_path = os.path.join(current_dir, "item.png")
        self.item_image = pygame.transform.scale(pygame.image.load(item_path), (item_size, item_size))
        
        self.wall_image = pygame.Surface((self.CELL_SIZE, self.CELL_SIZE))
        self.wall_image.fill(self.WALL_COLOR)
        self.path_image = pygame.Surface((self.CELL_SIZE, self.CELL_SIZE))
        self.path_image.fill(self.ROAD_COLOR)

    def scale_image(self, image):
        return pygame.transform.scale(image, (self.CELL_SIZE, self.CELL_SIZE))
    
    def draw_character(self):
        character_width = self.character_image.get_width()
        character_height = self.character_image.get_height()
        offset_x = (self.CELL_SIZE - character_width) // 2
        offset_y = (self.CELL_SIZE - character_height) // 2
        self.screen.blit(self.character_image, 
        (self.character_x * self.CELL_SIZE + offset_x, 
        self.character_y * self.CELL_SIZE + offset_y))

    def draw_enemies(self):
        for enemy in self.enemies:
            self.screen.blit(self.enemy_image, (enemy["x"] * self.CELL_SIZE, enemy["y"] * self.CELL_SIZE))

    def move_robot(self, dx, dy):
        new_x = self.character_x + dx
        new_y = self.character_y + dy

        if self.map[new_y][new_x] != "#":
            self.character_x = new_x
            self.character_y = new_y

            if self.map[self.character_y][self.character_x] == ".":
                self.points += 10
                self.map[self.character_y] = self.map[self.character_y][:self.character_x] + " " + self.map[self.character_y][self.character_x + 1:]

    def move_enemies(self):
        for enemy in self.enemies:
            direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            if direction == "UP" and self.map[enemy["y"] - 1][enemy["x"]] != "#":
                enemy["y"] -= 1
            elif direction == "DOWN" and self.map[enemy["y"] + 1][enemy["x"]] != "#":
                enemy["y"] += 1
            elif direction == "LEFT" and self.map[enemy["y"]][enemy["x"] - 1] != "#":
                enemy["x"] -= 1
            elif direction == "RIGHT" and self.map[enemy["y"]][enemy["x"] + 1] != "#":
                enemy["x"] += 1

    def collision_check(self):
        for enemy in self.enemies:
            if enemy["x"] == self.character_x and enemy["y"] == self.character_y:
                return True
        return False
    
    def all_coins_eated(self):
        for i in self.map:
            if "." in i:
                return False
        return True

    def show_end_screen(self):
        self.screen.fill(self.WALL_COLOR)
        if self.game_state == "win":
            end_text = self.game_font.render("WIN", True, (self.TEXT_COLOR))
            end_text_rect = end_text.get_rect(center = (self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(end_text, end_text_rect)
            pygame.display.flip()

        elif self.game_state == "game_over":
            end_text = self.game_font.render("GAME OVER", True, (self.TEXT_COLOR))
            end_text_rect = end_text.get_rect(center = (self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(end_text, end_text_rect)
            pygame.display.flip()
    
    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.move_robot(0, -1)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.move_robot(0, 1)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.move_robot(-1, 0)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.move_robot(1, 0)
            if self.game_state == "running":
                self.enemy_move_counter += 1
                if self.enemy_move_counter >= self.enemy_move_interval:
                    self.move_enemies()
                    self.enemy_move_counter = 0

                if self.collision_check():
                    self.game_state = "game_over"
                    self.show_end_screen()
                
                if self.all_coins_eated():
                    self.game_state = "win"
                    self.show_end_screen()

                self.screen.fill(self.ROAD_COLOR)
                self.draw_map()
                self.draw_enemies()
                self.draw_character()
                points_text = self.game_font.render(f"Points: {self.points}", True, (255, 255, 255))
                self.screen.blit(points_text, (550, 14))
                self.clock.tick(self.FPS)
                pygame.display.flip()

            else:
                self.show_end_screen()
        
if __name__ == "__main__":
    game = PicMan()
    game.main_loop()
