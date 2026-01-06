import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
class Level():
    def __init__(self):
        
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()

    def create_map(self):

        map_layout = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'), 
            'grass': import_csv_layout('map/map_Grass.csv'),
            'objects': import_csv_layout('map/map_Objects.csv')
        }

        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects')
        }
        
        for style,layout in map_layout.items():
            for row_index,row in enumerate(layout):
                for col_index,col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites], 'invinsible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites], 'grass', random_grass_image)
                        if style == 'objects':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites], 'objects', surf)
        #             Tile((x,y),[self.visible_sprites, self.obstacle_sprites])
        #         if col == 'p':
        self.player = Player((1970,1430),[self.visible_sprites], self.obstacle_sprites)

        # placeholder for remote player (will be updated from network)
        import pygame
        self.player2 = pygame.sprite.Sprite()
        try:
            self.player2.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        except Exception:
            # fallback to a simple surface
            surf = pygame.Surface((32, 32), pygame.SRCALPHA)
            surf.fill((0, 0, 255))
            self.player2.image = surf
        self.player2.rect = self.player2.image.get_rect(topleft=(100, 100))
        self.visible_sprites.add(self.player2)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)