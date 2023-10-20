import time, pygame
from threading import Timer
from datetime import datetime

from retrieveMail import updateAttachments
from dependencies import retrieveExistingFNames, chooseFile

def main():
    print(f'\n\nLaunching Application: {datetime.now()}')
    i = 0
    sleepInterval = 2
    pygame.init()
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    while True:
        # Only call to get new images from email every 240 image cycles to prevent using all
        # email requests too quickly
        if i%240 == 0:
            t = Timer(0, updateAttachments)
            t.start()
            i = 0
        fNames = retrieveExistingFNames()
        img = pygame.image.load(chooseFile(fNames))
        img = pygame.transform.scale(img, (pygame.display.Info().current_w,pygame.display.Info().current_h))
        screen.fill((0,0,0))
        screen.blit(img,(0,0))
        pygame.display.update()
        i+=1
        time.sleep(sleepInterval)

if __name__ == '__main__':
    main()