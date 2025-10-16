import pygame
from Classes import Fighter, GameUI
from Funcoes import carregar_chao


def main():
    pygame.init()
    WIDTH, HEIGHT = 1180, 620
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Street Fighter Mini")
    clock = pygame.time.Clock()
    FPS = 60

    largura, altura = 250, 220
    distancia_ataque = 0.5
    vida = 100
    velocidade = 8
    attackpower = 10
    knockback = 20
    largura_barra = 90
    altura_barra = 7
    BAR_Y_OFFSET = 25
    GROUND_HEIGHT = 100

    ground_img = carregar_chao(
        r"C:\Users\Aluno 02\Repositórios\PYGAME\chao.png", WIDTH, GROUND_HEIGHT, pygame
    )
    ui = GameUI(screen, WIDTH, HEIGHT)
    background_path = ui.menu()

    background_img = pygame.image.load(background_path).convert_alpha()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    keys_p1 = {
        "left": pygame.K_a,
        "right": pygame.K_d,
        "attack": pygame.K_s,
        "defend": pygame.K_w,
    }
    keys_p2 = {
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "attack": pygame.K_DOWN,
        "defend": pygame.K_UP,
    }

    sprites_p1 = {
        "idle": r"C:\Users\Aluno 02\Repositórios\PYGAME\P1\p1_idle1.png",
        "move": r"C:\Users\Aluno 02\Repositórios\PYGAME\P1\p1_move1.png",
        "attack": r"C:\Users\Aluno 02\Repositórios\PYGAME\P1\p1_attack1.png",
        "hit": r"C:\Users\Aluno 02\Repositórios\PYGAME\P1\p1_hit1.png",
    }

    sprites_p2 = {
        "idle": r"C:\Users\Aluno 02\Repositórios\PYGAME\P2\p2_idle1.png",
        "move": r"C:\Users\Aluno 02\Repositórios\PYGAME\P2\p2_move1.png",
        "attack": r"C:\Users\Aluno 02\Repositórios\PYGAME\P2\p2_attack1.png",
        "hit": r"C:\Users\Aluno 02\Repositórios\PYGAME\P2\p2_hit1.png",
    }

    player1 = Fighter(
        100,
        HEIGHT - GROUND_HEIGHT,
        sprites_p1,
        keys_p1,
        largura,
        altura,
        vida,
        velocidade,
        attackpower,
        knockback,
        largura_barra,
        altura_barra,
        BAR_Y_OFFSET,
        WIDTH,
    )
    player2 = Fighter(
        600,
        HEIGHT - GROUND_HEIGHT,
        sprites_p2,
        keys_p2,
        largura,
        altura,
        vida,
        velocidade,
        attackpower,
        knockback,
        largura_barra,
        altura_barra,
        BAR_Y_OFFSET,
        WIDTH,
    )

    running = True
    while running:
        clock.tick(FPS)
        screen.blit(background_img, (0, 0))
        screen.blit(ground_img, (0, HEIGHT - GROUND_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == player1.keys["attack"]:
                    player1.is_attacking = True
                if event.key == player2.keys["attack"]:
                    player2.is_attacking = True

        keys_pressed = pygame.key.get_pressed()
        player1.move(keys_pressed)
        player2.move(keys_pressed)

        player1.collide_with(player2)
        player2.collide_with(player1)

        player1.attack(player2, screen, distancia_ataque)
        player2.attack(player1, screen, distancia_ataque)

        player1.draw(screen)
        player2.draw(screen)

        if player1.health <= 0:
            ui.victory_screen("Jogador 2")
            main()
            break
        if player2.health <= 0:
            ui.victory_screen("Jogador 1")
            main()
            break

        pygame.display.flip()


if __name__ == "__main__":
    main()
