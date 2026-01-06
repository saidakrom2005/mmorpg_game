import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.direction = pygame.math.Vector2()
        self.vel = 5

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def move(self, vel):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            
        self.hitbox.x += self.direction.x * vel
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * vel
        self.collision('vertical') 
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for spite in self.obstacle_sprites:
                if spite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = spite.hitbox.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = spite.hitbox.right

        if direction == 'vertical':    
            for spite in self.obstacle_sprites:
                if spite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = spite.hitbox.top
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = spite.hitbox.bottom

    def update(self):
        self.input()
        self.move(self.vel)