import pygame, random
from pygame.locals import *
# window creation =====================================
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()

win = pygame.display.set_mode((800, 800))
pygame.display.set_caption("snek gaem")


class Food(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        img = pygame.image.load("images/heart.png")
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
    snake_splash = pygame.image.load("images/snake_title_screen.png")
    button_unpressed = pygame.image.load("images/button_unpressed.png")
    button_pressed = pygame.image.load("images/button_pressed.png")

    button_width = button_unpressed.get_rect().width
    button_height = button_unpressed.get_rect().height

    running = True
    while running:
        win.fill("White")
        win.blit(snake_splash, (0, 0))

        # buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # button input ================================================
        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if keys[K_ESCAPE]:
            running = False

        # TODO: fix bug where if you keep the mouse unmoved on the button when scenes change
        # TODO: that it'll just press the button again
        # mouse hover left button
        # start
        if 150 <= mouse_x <= 150 + button_width and 700 <= mouse_y <= 700 + button_height:
            win.blit(button_pressed, (150, 700))
            if event.type == pygame.MOUSEBUTTONUP:
                # pygame.time.wait(200)
                main_game()
        else:
            win.blit(button_unpressed, (150, 700))
        
        # mouse hover right button
        # quit
        if 500 <= mouse_x <= 500 + button_width and 700 <= mouse_y <= 700 + button_height:
            win.blit(button_pressed, (500, 700))
            if event.type == pygame.MOUSEBUTTONUP:
                # pygame.time.wait(200)
                running = False
        else:
            win.blit(button_unpressed, (500, 700))

        # title_screen update ============================================
        clock.tick(60)
        pygame.display.update()

    return 

def main_game():
    head = Player("images/snake_32b.png", (win.get_rect().center[0] - 32 / 2), (win.get_rect().center[1] - 32 / 2))
    snake_list = []
    snake_list.append(head)
    food = Food(random.randint(1, 7) * 100, random.randint(1, 7) * 100)

    # move states
    left, right, up, down = False, False, False, False

    running = True
    while running:

        # TODO: fix bug where being a snake_list of snake_list[head, segment]
        # TODO: makes it so that you can go over each other because they "technically" never
        # TODO: touch each other, snake_list[segment] is always one step behind so ssnake_list[head]
        # TODO: can never touch snake_list[segment]
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
            food = Food(random.randint(1, 7) * 100, random.randint(1, 7) * 100)

            # if the food spawns on top of a body segment
            while pygame.sprite.spritecollideany(food, snake_list):
                food.kill()
                food = Food(random.randint(0, 7) * 100, random.randint(0, 7) * 100)

        # Handle player quit ===============================
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        # Snake movement ====================================
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