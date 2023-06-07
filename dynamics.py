import numpy as np

class Robot():
    def __init__(self, x, y,phi):
        self.x = x
        self.y = y
        self.phi = phi

    def move(self):
        if(self.x > 0 and self.x < 1 and self.y > 0 and self.y < 2):
            wdd

    def ()


while True:     
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    P1.update()
    E1.move()
     
    DISPLAYSURF.fill(WHITE)
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)
         
    pygame.display.update()
    FramePerSec.tick(FPS)