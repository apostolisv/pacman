import pygame
from maps import Node

clock = pygame.time.Clock()
animation_counter = 0
pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 30)


class Graphics:

    def __init__(self, player, ghosts, board, debug):
        self.player = player
        self.ghosts = ghosts
        self.board = board
        self.debug = debug
        self.background = board.get_background()
        pygame.init()
        pygame.display.set_caption("Pacman!")
        self.screen = pygame.display.set_mode((600, 700))
        self.game_over_text = font.render('GAME OVER! PRESS "SPACE" TO PLAY!', False, (237, 237, 237))
        self.score_text = font.render("SCORE 0", False, (237, 237, 237))

    def draw_blocks(self):
        s = pygame.Surface((20, 18))
        s.set_alpha(50)
        s.fill((255, 0, 255))
        for row in self.board.nodes:
            for b in row:
                if isinstance(b, Node):
                    self.screen.blit(s, (b.x, b.y))

    def draw_portals(self):
        s = pygame.Surface((50, 30))
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 320))
        self.screen.blit(s, (550, 320))

    def draw_points(self):
        for node_list in self.board.nodes:
            for b in node_list:
                if b and b.point:
                    self.screen.blit(b.point.image, (b.x, b.y))

    def draw_score(self):
        s = pygame.Surface((180, 30))
        s.fill((0, 0, 0))
        self.screen.blit(s, (95, 20))
        score_text = font.render(f'SCORE {self.player.points}', False, (237, 237, 237))
        self.screen.blit(score_text, (25, 15))

    def draw_entities(self):
        global animation_counter
        self.screen.blit(self.background, (0, 50))
        if self.debug:
            self.draw_blocks()
        self.draw_points()
        for enemy in self.ghosts:
            self.screen.blit(enemy.get_image(animation_counter), (enemy.x, enemy.y))

        self.screen.blit(self.player.get_image(animation_counter), (self.player.x, self.player.y))
        self.draw_portals()
        pygame.display.update()
        animation_counter += 1
        if animation_counter > 10:
            animation_counter = 0

    def game_over(self):
        return not self.player.alive or self.board.game_over()

    def draw_game_over(self):
        self.screen.blit(self.game_over_text, (15, 660))

    def start(self):

        while True:
            clock.tick(45)
            self.draw_entities()
            self.board.tick(self.screen)
            self.draw_score()
            if self.game_over():
                self.draw_game_over()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                    if not self.game_over():
                        if event.key == pygame.K_LEFT:
                            self.player.move_left()
                            self.player.direction = 0
                        if event.key == pygame.K_RIGHT:
                            self.player.move_right()
                            self.player.direction = 1
                        if event.key == pygame.K_UP:
                            self.player.move_up()
                            self.player.direction = 2
                        if event.key == pygame.K_DOWN:
                            self.player.move_down()
                            self.player.direction = 3
                if event.type == pygame.MOUSEBUTTONDOWN and self.debug:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    print((x, y))

            pygame.display.update()
