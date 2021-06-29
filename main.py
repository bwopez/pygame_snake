import pygame, random
from pygame.locals import *

# window creation =====================================
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()

win = pygame.display.set_mode((800, 800))
pygame.display.set_caption("snek gaem")


# TODO: make a transition screen from title screen to play game state
# TODO: make a losing screen
class Static_image(pygame.sprite.Sprite):
    def __init__(self, img_url, x=0, y=0):
        super().__init__()
        # img = pygame.image.load("images/heart.png")
        img = pygame.image.load(img_url)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Player(pygame.sprite.Sprite):
    def __init__(self, imported_img_url, x=0, y=0):
        super().__init__()
        img = pygame.image.load(imported_img_url)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 

        self.step = self.rect.width
    
    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
    
    def move(self, direction, your_leader=0):

        if your_leader:
            self.rect.x, self.rect.y = your_leader.rect.x, your_leader.rect.y
        else:
            if direction == "left":
                self.rect.x += -self.step
                if self.rect.left <= 0:
                    self.rect.left = 0
            elif direction == "right":
                self.rect.x += self.step
                if self.rect.right >= win.get_width():
                    self.rect.right = win.get_width()
            elif direction == "up":
                self.rect.y += -self.step
                if self.rect.top <= 0:
                    self.rect.top = 0
            elif direction == "down":
                self.rect.y += self.step
                if self.rect.bottom >= win.get_height():
                    self.rect.bottom = win.get_height()

def title_screen():
    snake_splash = Static_image("images/snake_title_screen.png", 0, 0)
    start_button_unpressed = Static_image("images/button_unpressed.png", 150, 700)
    start_button_pressed = Static_image("images/button_pressed.png", 150, 700)
    quit_button_unpressed = Static_image("images/button_unpressed.png", 500, 700)
    quit_button_pressed = Static_image("images/button_pressed.png", 500, 700)

    button_width = start_button_unpressed.rect.width
    button_height = start_button_unpressed.rect.height

    running = True
    while running:
        win.fill("White")
        snake_splash.draw(win)
        start_surface = myfont.render("Start", True, ("Green"))
        quit_surface = myfont.render("Quit", True, ("Green"))

        # quit conditions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # button input ================================================
        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # clicks[left_click, middle_click, right_click]
        clicks = pygame.mouse.get_pressed()
        if keys[K_ESCAPE]:
            running = False

        # mouse hover left button
        # start
        if 150 <= mouse_x <= 150 + button_width and 700 <= mouse_y <= 700 + button_height:
            start_button_pressed.draw(win)
            win.blit(start_surface, (155, 705))
            if clicks[0]:
                main_game()
        else:
            start_button_unpressed.draw(win)
            win.blit(start_surface, (150, 700))
        
        # mouse hover right button
        # quit
        if 500 <= mouse_x <= 500 + button_width and 700 <= mouse_y <= 700 + button_height:
            quit_button_pressed.draw(win)
            win.blit(quit_surface, (505, 705))
            if clicks[0]:
                running = False
        else:
            quit_button_unpressed.draw(win)
            win.blit(quit_surface, (500, 700))

        # title_screen update ============================================
        clock.tick(60)
        pygame.display.update()

    return 

def main_game():
    head = Player("images/snake_32b.png", (win.get_rect().center[0] - 32 / 2), (win.get_rect().center[1] - 32 / 2))
    snake_list = []
    snake_list.append(head)
    food = Static_image("images/heart.png", random.randint(1, 7) * 100, random.randint(1, 7) * 100)

    # move states
    left, right, up, down = False, False, False, False

    running = True
    game_paused = True
    while running:

        # Lose condition handling ==========================
        # if the head collides with the body
        if pygame.sprite.spritecollideany(head, snake_list[1:]):
            # TODO: make a cool losing screen
            running = False

        # Eating the food ==================================
        if head.rect.colliderect(food.rect):
            food.kill()
            if len(snake_list) % 2 == 0:
                snake_list.append(Player("images/snake_32b.png", snake_list[-1].rect.x, snake_list[-1].rect.y))
            else:
                snake_list.append(Player("images/snake_32.png", snake_list[-1].rect.x, snake_list[-1].rect.y))
            food = Static_image("images/heart.png", random.randint(1, 7) * 100, random.randint(1, 7) * 100)

            # if the food spawns on top of a body segment
            while pygame.sprite.spritecollideany(food, snake_list):
                food.kill()
                food = Static_image("images/heart.png", random.randint(0, 7) * 100, random.randint(0, 7) * 100)

        # Handle player quit ===============================
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if game_paused:
            if keys[K_a]:
                left = True
                game_paused = False
            elif keys[K_d]:
                right = True
                game_paused = False
            elif keys[K_w]:
                up = True
                game_paused = False
            elif keys[K_s]:
                down = True
                game_paused = False
        # Snake movement ====================================
        else:
            if left:
                if keys[K_a]:
                    left = True
                    right = False
                    up = False
                    down = False
                if keys[K_w]:
                    left = False
                    right = False
                    up = True
                    down = False
                if keys[K_s]:
                    left = False
                    right = False
                    up = False
                    down = True
            if right:
                if keys[K_d]:
                    left = False
                    right = True
                    up = False
                    down = False
                if keys[K_w]:
                    left = False
                    right = False
                    up = True
                    down = False
                if keys[K_s]:
                    left = False
                    right = False
                    up = False
                    down = True
            if up:
                if keys[K_a]:
                    left = True
                    right = False
                    up = False
                    down = False
                if keys[K_d]:
                    left = False
                    right = True
                    up = False
                    down = False
                if keys[K_w]:
                    left = False
                    right = False
                    up = True
                    down = False
            if down:
                if keys[K_a]:
                    left = True
                    right = False
                    up = False
                    down = False
                if keys[K_d]:
                    left = False
                    right = True
                    up = False
                    down = False
                if keys[K_s]:
                    left = False
                    right = False
                    up = False
                    down = True
        
        if left:
            for segment in reversed(snake_list):
                if snake_list.index(segment) == 0:
                    segment.move("left")
                else:
                    segment.move("left", snake_list[snake_list.index(segment) - 1])
        elif right:
            for segment in reversed(snake_list):
                if snake_list.index(segment) == 0:
                    segment.move("right")
                else:
                    segment.move("right", snake_list[snake_list.index(segment) - 1])
        elif up:
            for segment in reversed(snake_list):
                if snake_list.index(segment) == 0:
                    segment.move("up")
                else:
                    segment.move("up", snake_list[snake_list.index(segment) - 1])
        elif down:
            for segment in reversed(snake_list):
                if snake_list.index(segment) == 0:
                    segment.move("down")
                else:
                    segment.move("down", snake_list[snake_list.index(segment) - 1])

        # Update window ===================================
        win.fill("White")
        for segment in reversed(snake_list):
            segment.draw(win)
        food.draw(win)
        # High score ======================================
        text_surface = myfont.render(str(len(snake_list) - 1), False, ("Black"))
        win.blit(text_surface, (win.get_rect().center[0] - text_surface.get_rect().width / 2, 30))

        clock.tick(15)
        pygame.display.update()
    
    return


if __name__ == '__main__':
    title_screen()
    pygame.quit()