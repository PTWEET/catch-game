import pygame
import random

def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Doctor!")

    background = pygame.image.load("dark.jpg")
    background = background.convert()

    cardinal = pygame.image.load("comet.png")
    cardinal = cardinal.convert_alpha()
    cardinal = pygame.transform.scale(cardinal, (100, 100))

    cardinal_x = random.randint(0, screen.get_width()-100)
    cardinal_y = random.randint(0, screen.get_height()-100)

    clock = pygame.time.Clock()
    keepGoing = True


    while keepGoing:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        cardinal_y += 5
        if cardinal_y > screen.get_height():
            cardinal_y = random.randint(-100,0)
            cardinal_x = random.randint(0, screen.get_width()-100)
        cardinal_x += 5
        if cardinal_x > screen.get_width():
            cardinal_x = random.randint(-100,0)
            cardinal_y = random.randint(0, screen.get_height()-100)
        screen.blit(background, (0, 0))
        screen.blit(cardinal, (cardinal_x, cardinal_y))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
