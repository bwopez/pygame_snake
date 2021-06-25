import pygame, random
from pygame.locals import *
# window creation =====================================
pygame.init()
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

def main_game():
    head = Player("images/snake_32b.png")
    snake_list = []
    snake_list.append(head)
    food = Food(random.randint(0, 7) * 100, random.randint(0, 7) * 100)

    # movement
    left, right, up, down = False, False, False, False

    running = True

    while running:

        # Lose condition handling ==========================
        # if the head collides with the body
        if pygame.sprite.spritecollideany(head, snake_list[2:]):
            # TODO: make a cool losing screen
            running = False

        # Eating the food ==================================
        if head.rect.colliderect(food.rect):
            food.kill()
            if len(snake_list) % 2 == 0:
                snake_list.append(Player("images/snake_32b.png", snake_list[-1].rect.x, snake_list[-1].rect.y))
            else:
                snake_list.append(Player("images/snake_32.png", snake_list[-1].rect.x, snake_list[-1].rect.y))
            food = Food(random.randint(0, 7) * 100, random.randint(0, 7) * 100)

            # if the food spawns on top of a body segment
            while pygame.sprite.spritecollideany(food, snake_list):
                food.kill()
                food = Food(random.randint(0, 7) * 100, random.randint(0, 7) * 100)

        # Handle player quit ===============================
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            running = False
        
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

        clock.tick(15)
        pygame.display.update()


if __name__ == '__main__':
    main_game()
    pygame.quit()