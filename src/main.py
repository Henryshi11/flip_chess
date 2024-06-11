import pygame
import sys
from game import play_game

# Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flip Chess')

def main():
    """
    Main function to choose AI type and start the game.
    """
    run = True
    selected_ai = None

    while run:
        WIN.fill((255, 255, 255))

        font = pygame.font.Font(None, 36)
        qlearning_text = font.render("Play against Q-Learning AI", True, (0, 0, 0))
        minmax_text = font.render("Play against MinMax AI", True, (0, 0, 0))

        qlearning_rect = qlearning_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        minmax_rect = minmax_text.get_rect(center=(WIDTH // 2, 2 * HEIGHT // 3))

        WIN.blit(qlearning_text, qlearning_rect)
        WIN.blit(minmax_text, minmax_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if qlearning_rect.collidepoint(mouse_pos):
                    selected_ai = 'qlearning'
                    run = False
                elif minmax_rect.collidepoint(mouse_pos):
                    selected_ai = 'minmax'
                    run = False

    play_game(WIN, selected_ai)

if __name__ == "__main__":
    main()
