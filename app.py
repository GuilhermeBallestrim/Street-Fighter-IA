import pygame
import sys


def main():
    pygame.init()
    WIDTH, HEIGHT = 1180, 620
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Street Fighter Mini")
    clock = pygame.time.Clock()
    FPS = 60

    largura = 250
    altura = 220
    distancia_ataque = 0.5
    vida = 100
    velocidade = 8
    attackpower = 10
    knockback = 20
    largura_barra = 90  # largura da barra de vida
    altura_barra = 7  # altura da barra
    BAR_Y_OFFSET = 25

    # Cores
    WHITE = (245, 245, 245)

    # Chão
    GROUND_HEIGHT = 100
    ground_img = pygame.image.load(
        r"C:\Users\Aluno 02\Repositórios\PYGAME\chao.png"
    ).convert_alpha()
    ground_img = pygame.transform.scale(ground_img, (WIDTH, GROUND_HEIGHT))

    def menu(screen):
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Arial", 40)
        selected = 0
        backgrounds = [
            r"C:\Users\Aluno 02\Repositórios\PYGAME\background1.png",
            r"C:\Users\Aluno 02\Repositórios\PYGAME\background2.png",
            r"C:\Users\Aluno 02\Repositórios\PYGAME\background3.png",
        ]
        current_bg = 0
        running = True

        while running:
            screen.fill((50, 50, 50))
            # preview do cenário
            preview_img = pygame.image.load(backgrounds[current_bg]).convert_alpha()
            preview_img = pygame.transform.scale(preview_img, (WIDTH, HEIGHT))
            screen.blit(preview_img, (0, 0))

            # overlay semitransparente para legibilidade do menu
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % 2
                    if event.key == pygame.K_DOWN:
                        selected = (selected + 1) % 2
                    if event.key == pygame.K_RETURN:
                        if selected == 0:
                            running = False  # iniciar jogo
                        elif selected == 1:
                            current_bg = (current_bg + 1) % len(backgrounds)

            start_color = (255, 255, 0) if selected == 0 else (255, 255, 255)
            scene_color = (255, 255, 0) if selected == 1 else (255, 255, 255)

            start_text = font.render("Iniciar Jogo", True, start_color)
            scene_text = font.render(f"Cenário: {current_bg + 1}", True, scene_color)

            screen.blit(
                start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 3)
            )
            screen.blit(
                scene_text, (WIDTH // 2 - scene_text.get_width() // 2, HEIGHT // 2)
            )

            pygame.display.flip()
            clock.tick(60)

        return backgrounds[current_bg]

    def victory_screen(screen, winner):
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Arial", 60)
        running = True
        while running:
            screen.fill((0, 0, 0))  # fundo preto
            text = font.render(f"{winner} venceu!", True, (255, 255, 0))
            screen.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 2 - text.get_height() // 2,
                ),
            )

            info_text = font.render(
                "Pressione Enter para voltar ao menu", True, (255, 255, 255)
            )
            screen.blit(
                info_text, (WIDTH // 2 - info_text.get_width() // 2, HEIGHT // 2 + 50)
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    running = False  # volta ao menu

            pygame.display.flip()
            clock.tick(60)

    # Fighter com sprites
    class Fighter:
        def __init__(self, x, y, sprite_paths, keys):
            # Carrega sprites
            self.sprites = {
                action: pygame.image.load(path).convert_alpha()
                for action, path in sprite_paths.items()
            }

            # Estado inicial
            self.state = "idle"
            self.image = self.sprites[self.state]

            # Redimensiona sprite
            self.image = pygame.transform.scale(self.image, (largura, altura))

            # Rect baseado na imagem
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = y

            # Atributos
            self.health = vida
            self.speed = velocidade
            self.attack_power = attackpower
            self.knockback = knockback
            self.keys = keys
            self.is_attacking = False
            self.state_timer = 0
            self.state_duration = 15  # frames que ataque/hit dura

        def move(self, keys_pressed):
            # Só muda para move se não estiver atacando ou hit
            if self.state_timer <= 0:
                self.state = "idle"
                if keys_pressed[self.keys["left"]] and self.rect.left > 0:
                    self.rect.x -= self.speed
                    self.state = "move"
                if keys_pressed[self.keys["right"]] and self.rect.right < WIDTH:
                    self.rect.x += self.speed
                    self.state = "move"
            else:
                self.state_timer -= 1  # decrementa timer do estado atual

        def attack(self, opponent):
            if self.is_attacking:
                self.state = "attack"
                self.state_timer = self.state_duration

                attack_rect = pygame.Rect(
                    0, 0, int(largura * distancia_ataque), self.rect.height
                )
                if self.rect.centerx < opponent.rect.centerx:
                    attack_rect.topleft = (self.rect.right, self.rect.top)
                else:
                    attack_rect.topright = (self.rect.left, self.rect.top)

                if attack_rect.colliderect(opponent.rect):
                    opponent.take_damage(self.attack_power, self)

                self.is_attacking = False
                pygame.draw.rect(
                    screen, (255, 255, 0), attack_rect, 2
                )  # contorno visual para debug

        def draw(self, screen):
            self.image = self.sprites[self.state]
            self.image = pygame.transform.scale(self.image, (largura, altura))
            screen.blit(self.image, (self.rect.x, self.rect.y))

            # Calcula posição da barra
            bar_x = self.rect.x + (self.rect.width - largura_barra) // 2
            bar_y = self.rect.y - BAR_Y_OFFSET

            # Barra vermelha de fundo
            pygame.draw.rect(
                screen, (255, 0, 0), (bar_x, bar_y, largura_barra, altura_barra)
            )
            # Barra azul proporcional à vida
            pygame.draw.rect(
                screen,
                (0, 0, 255),
                (bar_x, bar_y, largura_barra * (self.health / 100), altura_barra),
            )

        def collide_with(self, opponent):
            if self.rect.colliderect(opponent.rect):
                overlap = self.rect.clip(opponent.rect)  # área de sobreposição
                if self.rect.centerx < opponent.rect.centerx:
                    self.rect.right -= overlap.width // 2
                    opponent.rect.left += overlap.width // 2
                else:
                    self.rect.left += overlap.width // 2
                    opponent.rect.right -= overlap.width // 2

        def take_damage(self, amount, opponent):
            defending = False
            keys_pressed = pygame.key.get_pressed()

            if self.rect.centerx < opponent.rect.centerx:
                if keys_pressed[self.keys["left"]]:
                    defending = True
            else:
                if keys_pressed[self.keys["right"]]:
                    defending = True

            # Defesa manual
            if keys_pressed[self.keys["defend"]]:
                defending = True

            # Aplica redução de dano e knockback
            if defending:
                amount *= 0.25
                knockback = self.knockback // 4
            else:
                knockback = self.knockback

            self.health -= amount
            self.state = "hit"
            self.state_timer = self.state_duration

            # Aplica knockback
            if self.rect.centerx < opponent.rect.centerx:
                self.rect.x -= knockback
            else:
                self.rect.x += knockback

            # Limites da tela
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH

    # Teclas
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

    # Sprites dos jogadores
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

    # Chama menu
    background_path = menu(screen)
    background_img = pygame.image.load(background_path).convert_alpha()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    player1 = Fighter(100, HEIGHT - GROUND_HEIGHT, sprites_p1, keys_p1)
    player2 = Fighter(600, HEIGHT - GROUND_HEIGHT, sprites_p2, keys_p2)

    # Loop principal
    running = True
    while running:
        clock.tick(FPS)
        screen.blit(background_img, (0, 0))  # desenha o cenário
        screen.blit(ground_img, (0, HEIGHT - GROUND_HEIGHT))  # desenha o chão

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

        # Colisão
        player1.collide_with(player2)
        player2.collide_with(player1)

        # Ataque
        player1.attack(player2)
        player2.attack(player1)

        # Desenha personagens
        player1.draw(screen)
        player2.draw(screen)

        if player1.health <= 0:
            victory_screen(screen, "Jogador 2")
            main()  # reinicia o menu e o jogo
            break
        if player2.health <= 0:
            victory_screen(screen, "Jogador 1")
            main()  # reinicia o menu e o jogo
            break

        pygame.display.flip()


if __name__ == "__main__":
    main()
