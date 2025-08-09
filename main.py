import pygame
import random
import os

# Initialize
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Digital Egg Cracker 🥚")
clock = pygame.time.Clock()

# Asset folder
ASSETS = os.path.join(os.path.dirname(__file__), "assets")

# Target egg size
egg_width, egg_height = 400, 400

# Load main egg image
egg_img = pygame.image.load(os.path.join(ASSETS, "egg_uncracked.png")).convert_alpha()
egg_img = pygame.transform.smoothscale(egg_img, (egg_width, egg_height))

# Map messages to images
message_images = {
    "Well done, you cracked it.": "4770-removebg-preview.png",
    "That egg had a family.": "download__1_-removebg-preview.png",
    "No chicken today, sorry.": "4773-removebg-preview (2).png",
    "Oops… the egg just gave up.": "Illustration_design_of_a_freshly_hatched_chick_and_its_head_is_covered_with_egg_shells___Premium_Vector-removebg-preview.png"
}

# Preload images
loaded_images = {}
for msg, filename in message_images.items():
    img_path = os.path.join(ASSETS, filename)
    if os.path.exists(img_path):
        loaded_images[msg] = pygame.transform.smoothscale(
            pygame.image.load(img_path).convert_alpha(),
            (egg_width, egg_height)
        )

# Optional sound
try:
    crack_sound = pygame.mixer.Sound(os.path.join(ASSETS, "crack-sound.wav"))
except:
    crack_sound = None

# States
cracked = False
current_crack = None
font = pygame.font.SysFont(None, 28)
message = ""

funny_messages = list(message_images.keys())

# Button colors & sizes
button_color = (200, 200, 200)
button_text_color = (0, 0, 0)
button_height = 40
button_width = 100
button_spacing = 20

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if reset_button.collidepoint(mouse_pos):
                cracked = False
                message = ""
                current_crack = None
            elif exit_button.collidepoint(mouse_pos):
                running = False
            elif not cracked:
                cracked = True
                message = random.choice(funny_messages)
                current_crack = loaded_images.get(message, egg_img)
                if crack_sound:
                    crack_sound.play()

    # Center coordinates for egg
    egg_x = (screen.get_width() - egg_width) // 2
    egg_y = (screen.get_height() - egg_height) // 2 - 30  # shift up for text space

    # Draw egg or cracked image
    if cracked:
        screen.blit(current_crack, (egg_x, egg_y))
    else:
        screen.blit(egg_img, (egg_x, egg_y))

    # Draw message below the egg
    if message:
        text_surface = font.render(message, True, (0, 0, 0))
        text_x = (screen.get_width() - text_surface.get_width()) // 2
        text_y = egg_y + egg_height + 10
        screen.blit(text_surface, (text_x, text_y))

    # Button Y position
    button_y = screen.get_height() - button_height - 20

    # Reset button (left)
    reset_x = (screen.get_width() // 2) - button_width - (button_spacing // 2)
    reset_button = pygame.Rect(reset_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, button_color, reset_button)
    reset_text = font.render("Reset", True, button_text_color)
    screen.blit(reset_text, (reset_button.x + (button_width - reset_text.get_width()) // 2,
                              reset_button.y + (button_height - reset_text.get_height()) // 2))

    # Exit button (right)
    exit_x = (screen.get_width() // 2) + (button_spacing // 2)
    exit_button = pygame.Rect(exit_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, button_color, exit_button)
    exit_text = font.render("Exit", True, button_text_color)
    screen.blit(exit_text, (exit_button.x + (button_width - exit_text.get_width()) // 2,
                            exit_button.y + (button_height - exit_text.get_height()) // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
