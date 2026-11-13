
import pygame
import random
import os
import sys

# -----------------------------
# INITIALIZATION
# -----------------------------

pygame.init()

WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730
FPS = 60

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

CLOCK = pygame.time.Clock()

STAT_FONT = pygame.font.SysFont("comicsans", 40)
END_FONT = pygame.font.SysFont("comicsans", 60)

# Load original game images
IMG_DIR = os.path.join(os.path.dirname(__file__), "imgs")

PIPE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join(IMG_DIR, "pipe.png")).convert_alpha()
)

BG_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_DIR, "bg.png")).convert_alpha(),
    (WIN_WIDTH, 900)
)

BIRD_IMGS = [
    pygame.transform.scale2x(
        pygame.image.load(
            os.path.join(IMG_DIR, f"bird{i}.png")
        ).convert_alpha()
    )
    for i in range(1, 4)
]

BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join(IMG_DIR, "base.png")).convert_alpha()
)


# -----------------------------
# BIRD CLASS
# -----------------------------

class Bird:

    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y

        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):

        self.vel = -8.5
        self.tick_count = 0
        self.height = self.y

    def move(self):

        self.tick_count += 1

        displacement = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        displacement = min(displacement, 16)
        displacement = max(displacement, -16)

        if displacement < 0:
            displacement -= 2

        self.y += displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION

        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):

        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]

        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]

        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]

        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]

        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)

        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(
                topleft=(self.x, self.y)
            ).center
        )

        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):

        return pygame.mask.from_surface(self.img)


# -----------------------------
# PIPE CLASS
# -----------------------------

class Pipe:

    GAP = 200
    VEL = 5

    def __init__(self, x):

        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(
            PIPE_IMG, False, True
        )

        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False

        self.set_height()

    def set_height(self):

        self.height = random.randrange(50, 450)

        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):

        self.x -= self.VEL

    def draw(self, win):

        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):

        bird_mask = bird.get_mask()

        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (
            self.x - bird.x,
            self.top - round(bird.y)
        )

        bottom_offset = (
            self.x - bird.x,
            self.bottom - round(bird.y)
        )

        top_collision = bird_mask.overlap(
            top_mask, top_offset
        )

        bottom_collision = bird_mask.overlap(
            bottom_mask, bottom_offset
        )

        return top_collision or bottom_collision


# -----------------------------
# BASE CLASS
# -----------------------------

class Base:

    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):

        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):

        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):

        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


# -----------------------------
# DRAW GAME WINDOW
# -----------------------------

def draw_window(win, bird, pipes, base, score):

    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    bird.draw(win)

    score_label = STAT_FONT.render(
        f"Score: {score}",
        1,
        (255, 255, 255)
    )

    win.blit(
        score_label,
        (WIN_WIDTH - score_label.get_width() - 15, 10)
    )

    pygame.display.update()


# -----------------------------
# GAME OVER SCREEN
# -----------------------------

def game_over_screen(score):

    WIN.blit(BG_IMG, (0, 0))

    title = END_FONT.render(
        "GAME OVER",
        True,
        (255, 255, 255)
    )

    final_score = STAT_FONT.render(
        f"Score: {score}",
        True,
        (255, 255, 255)
    )

    restart = STAT_FONT.render(
        "Press R to Restart",
        True,
        (255, 255, 255)
    )

    quit_text = STAT_FONT.render(
        "Press Q to Quit",
        True,
        (255, 255, 255)
    )

    WIN.blit(title, title.get_rect(center=(300, 280)))
    WIN.blit(final_score, final_score.get_rect(center=(300, 360)))
    WIN.blit(restart, restart.get_rect(center=(300, 450)))
    WIN.blit(quit_text, quit_text.get_rect(center=(300, 510)))

    pygame.display.update()


# -----------------------------
# MAIN GAME LOOP
# -----------------------------

def main():

    bird = Bird(230, 350)

    pipes = [Pipe(700)]

    base = Base(FLOOR)

    score = 0
    running = True
    game_active = True

    while running:

        CLOCK.tick(FPS)

        # Handle keyboard events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if game_active:

                    if event.key == pygame.K_SPACE:
                        bird.jump()

                else:

                    if event.key == pygame.K_r:
                        main()
                        return

                    elif event.key == pygame.K_q:
                        running = False

        if game_active:

            bird.move()

            base.move()

            # Move pipes
            for pipe in pipes:
                pipe.move()

            # Check collision
            for pipe in pipes:

                if pipe.collide(bird):
                    game_active = False

                if not pipe.passed and pipe.x < bird.x:

                    pipe.passed = True
                    score += 1

            # Remove pipes outside the screen
            pipes = [
                pipe for pipe in pipes
                if pipe.x + pipe.PIPE_TOP.get_width() > 0
            ]

            # Generate new pipes
            if len(pipes) == 0 or pipes[-1].x < 350:
                pipes.append(Pipe(600))

            # Check floor and ceiling collision
            if bird.y + bird.img.get_height() >= FLOOR:
                game_active = False

            if bird.y < 0:
                game_active = False

            draw_window(
                WIN,
                bird,
                pipes,
                base,
                score
            )

        else:

            game_over_screen(score)

    pygame.quit()
    sys.exit()


# -----------------------------
# START GAME
# -----------------------------

if __name__ == "__main__":
    main()
