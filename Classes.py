import pygame
import sys


class Fighter:
    def __init__(
        self,
        x,
        y,
        sprite_paths,
        keys,
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
        HEIGHT,
    ):
        self.sprites = {
            action: pygame.image.load(path).convert_alpha()
            for action, path in sprite_paths.items()
        }

        self.state = "idle"
        self.image = pygame.transform.scale(self.sprites[self.state], (largura, altura))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y

        self.health = vida
        self.speed = velocidade
        self.attack_power = attackpower
        self.knockback = knockback
        self.keys = keys
        self.is_attacking = False
        self.state_timer = 0
        self.state_duration = 15

        # Novos atributos de movimento
        self.vel_y = 0
        self.jump_height = -18
        self.gravity = 1
        self.on_ground = True
        self.is_crouching = False

        self.largura = largura
        self.altura = altura
        self.largura_barra = largura_barra
        self.altura_barra = altura_barra
        self.BAR_Y_OFFSET = BAR_Y_OFFSET
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.is_hit_flash = False
        self.hit_flash_timer = 0
        self.hit_flash_duration = 5  # frames que o flash dura

    def move(self, keys_pressed):
        # Reset do estado
        if self.state_timer <= 0:
            self.state = "idle"

        # Movimento horizontal
        if keys_pressed[self.keys["left"]]:
            self.rect.x -= self.speed
            if self.on_ground:
                self.state = "move"
        if keys_pressed[self.keys["right"]]:
            self.rect.x += self.speed
            if self.on_ground:
                self.state = "move"

        # Pulo
        if keys_pressed[self.keys.get("jump", None)] and self.on_ground:
            self.vel_y = self.jump_height
            self.on_ground = False
            self.state = "jump"

        # Agachamento
        if keys_pressed[self.keys.get("crouch", None)] and self.on_ground:
            self.is_crouching = True
            self.state = "crouch"
        else:
            self.is_crouching = False

        # Aplicar gravidade
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Checar chão
        if self.rect.bottom >= self.HEIGHT - 100:  # 100 = altura do chão
            self.rect.bottom = self.HEIGHT - 100
            self.vel_y = 0
            self.on_ground = True

        # Limites da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.WIDTH:
            self.rect.right = self.WIDTH

    def attack(self, opponent, screen, distancia_ataque):
        if self.is_attacking:
            # Permitir ataque no ar ou agachado
            self.state = "attack_air" if not self.on_ground else "attack"
            self.state_timer = self.state_duration

            attack_rect = pygame.Rect(
                0, 0, int(self.largura * distancia_ataque), self.rect.height
            )
            if self.rect.centerx < opponent.rect.centerx:
                attack_rect.topleft = (self.rect.right, self.rect.top)
            else:
                attack_rect.topright = (self.rect.left, self.rect.top)

            if attack_rect.colliderect(opponent.rect):
                opponent.take_damage(self.attack_power, self)

            self.is_attacking = False
            pygame.draw.rect(screen, (255, 255, 0), attack_rect, 2)

    def draw(self, screen):
        # Redimensiona sprite
        image = pygame.transform.scale(
            self.sprites[self.state], (self.largura, self.altura)
        )

        # Flash vermelho se levou hit
        if self.is_hit_flash:
            flash_surface = pygame.Surface((self.largura, self.altura))
            flash_surface.fill((255, 0, 0))
            flash_surface.set_alpha(150)
            image.blit(flash_surface, (0, 0))
            self.hit_flash_timer -= 1
            if self.hit_flash_timer <= 0:
                self.is_hit_flash = False

        screen.blit(image, (self.rect.x, self.rect.y))

        # Barra de vida
        bar_x = self.rect.x + (self.rect.width - self.largura_barra) // 2
        bar_y = self.rect.y - self.BAR_Y_OFFSET

        if self.health > 70:
            bar_color = (0, 255, 0)
        elif self.health > 30:
            bar_color = (255, 255, 0)
        else:
            bar_color = (255, 0, 0)

        # Fundo da barra
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            (bar_x, bar_y, self.largura_barra, self.altura_barra),
        )
        # Vida atual
        pygame.draw.rect(
            screen,
            bar_color,
            (bar_x, bar_y, self.largura_barra * (self.health / 100), self.altura_barra),
        )

        # Indicador de defesa
        keys_pressed = pygame.key.get_pressed()
        defending = keys_pressed.get(self.keys.get("defend", None), False)
        if defending:
            pygame.draw.rect(
                screen,
                (0, 255, 255),
                (bar_x - 2, bar_y - 2, self.largura_barra + 4, self.altura_barra + 4),
                2,
            )


class GameUI:
    def __init__(self, screen, WIDTH, HEIGHT):
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 40)
        self.backgrounds = [
            r"C:\Users\Aluno 02\Repositórios\PYGAME\background1.png",
            r"C:\Users\Aluno 02\Repositórios\PYGAME\background2.png",
            r"C:\Users\Aluno 02\Repositórios\PYGAME\background3.png",
        ]

    def menu(self):
        selected = 0
        current_bg = 0
        running = True

        while running:
            self.screen.fill((50, 50, 50))
            preview_img = pygame.image.load(
                self.backgrounds[current_bg]
            ).convert_alpha()
            preview_img = pygame.transform.scale(preview_img, (self.WIDTH, self.HEIGHT))
            self.screen.blit(preview_img, (0, 0))

            overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

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
                            running = False
                        elif selected == 1:
                            current_bg = (current_bg + 1) % len(self.backgrounds)

            start_color = (255, 255, 0) if selected == 0 else (255, 255, 255)
            scene_color = (255, 255, 0) if selected == 1 else (255, 255, 255)

            start_text = self.font.render("Iniciar Jogo", True, start_color)
            scene_text = self.font.render(
                f"Cenário: {current_bg + 1}", True, scene_color
            )

            self.screen.blit(
                start_text,
                (self.WIDTH // 2 - start_text.get_width() // 2, self.HEIGHT // 3),
            )
            self.screen.blit(
                scene_text,
                (self.WIDTH // 2 - scene_text.get_width() // 2, self.HEIGHT // 2),
            )

            pygame.display.flip()
            self.clock.tick(60)

        return self.backgrounds[current_bg]

    def victory_screen(self, winner):
        font_big = pygame.font.SysFont("Arial", 60)
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            text = font_big.render(f"{winner} venceu!", True, (255, 255, 0))
            self.screen.blit(
                text,
                (
                    self.WIDTH // 2 - text.get_width() // 2,
                    self.HEIGHT // 2 - text.get_height() // 2,
                ),
            )

            info_text = font_big.render(
                "Pressione Enter para voltar ao menu", True, (255, 255, 255)
            )
            self.screen.blit(
                info_text,
                (self.WIDTH // 2 - info_text.get_width() // 2, self.HEIGHT // 2 + 50),
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    running = False

            pygame.display.flip()
            self.clock.tick(60)
