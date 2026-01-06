import pygame
from network import Network
from game import Game


def main():
    pygame.init()
    game = Game()
    level = game.level

    n = Network()
    initial = n.p
    if initial is None:
        print("Failed to get player state from server. Exiting client.")
        return

    # set local player position from server-provided dict
    try:
        x = initial.get('x', level.player.rect.centerx)
        y = initial.get('y', level.player.rect.centery)
        level.player.hitbox.center = (x, y)
        level.player.rect.center = (x, y)
    except Exception:
        pass

    clock = pygame.time.Clock()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # Level.run will call player.update() and draw sprites
        # Send local player state and receive remote state
        local = {
            'x': level.player.hitbox.centerx,
            'y': level.player.hitbox.centery,
            'width': level.player.rect.width,
            'height': level.player.rect.height,
            'vel': getattr(level.player, 'vel', 0)
        }

        other = n.send(local)
        if other:
            try:
                ox = other.get('x', level.player2.rect.centerx)
                oy = other.get('y', level.player2.rect.centery)
                level.player2.rect.center = (ox, oy)
            except Exception:
                pass

        level.run()
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()