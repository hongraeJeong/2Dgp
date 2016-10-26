# hero_controller.py : control hero move with left and right key

import random
from pico2d import *

running = None
hero = None

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)


class Hero:
    image = None

    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND, RUN_WHILE_RIGHT, RUN_WHILE_LEFT, PLY = 0, 1, 2, 3, 5, 4, 2
    HERO_UP = False
    HERO_DOWN = False
    HERO_UP_DOWN = False
    HERO_DOWN_UP = False


    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90
        self.frame = random.randint(0, 7)
        self.state = self.RIGHT_STAND
        self.Dash = 0
        if Hero.image == None:
            Hero.image = load_image('animation_sheet.png')

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                if self.state == self.LEFT_RUN:
                    self.state = self.RUN_WHILE_RIGHT
                else:
                    self.state = self.RIGHT_RUN
            elif event.key == SDLK_LEFT:
                if self.state == self.RIGHT_RUN:
                    self.state = self.RUN_WHILE_LEFT
                else:
                    self.state = self.LEFT_RUN
            if event.key == SDLK_UP:
                if self.HERO_DOWN == True:
                    self.HERO_DOWN_UP =True
                else:
                    self.HERO_UP = True
            elif event.key == SDLK_DOWN:
                if self.HERO_UP == True:
                    self.HERO_UP_DOWN = True
                else:
                    self.HERO_DOWN = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                if self.state == self.RIGHT_RUN:
                    self.state = self.RIGHT_STAND
                else:
                    self.state = self.LEFT_RUN
            elif event.key == SDLK_LEFT:
                if self.state == self.LEFT_RUN:
                    self.state = self.LEFT_STAND
                else:
                    self.state = self.RIGHT_RUN
            if event.key == SDLK_UP:
                if self.HERO_UP == True:
                    self.HERO_UP = False
                else:
                    self.HERO_DOWN = True
                    self.HERO_DOWN_UP = False
            elif event.key == SDLK_DOWN:
                if self.HERO_DOWN == True:
                    self.HERO_DOWN =False
                else:
                    self.HERO_UP = True
                    self.HERO_UP_DOWN = False
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            self.Dash = 12
        elif event.type == SDL_KEYUP and event.key == SDLK_SPACE:
            self.Dash = 0
        pass


    def update(self):
        self.frame = (self.frame +1) % 8
        if self.HERO_UP == True or self.HERO_DOWN_UP == True:
            self.y += 5
        elif self.HERO_DOWN == True or self.HERO_UP_DOWN == True:
            self.y -= 5
        if self.state == self.RIGHT_RUN or self.state == self.RUN_WHILE_RIGHT:
            self.x = min(800,self.x+5+self.Dash)
        elif self.state == self.LEFT_RUN or self.state == self.RUN_WHILE_LEFT:
            self.x = max(0, self.x -5 - self.Dash)

    def draw(self):
        if self.Dash == 12 and self.state%4 == 0:
            self.image.clip_draw((self.frame-1) * 100, self.state % 4 * 100, 100, 100, self.x+ 30 - (self.frame*5), self.y)
        elif self.Dash == 12 and self.state % 4 == 1:
            self.image.clip_draw((self.frame-1) * 100, self.state % 4 * 100, 100, 100, self.x - 30 + (self.frame*3), self.y)
        if self.state >2:
            if self.HERO_UP_DOWN == True or self.HERO_UP == True or self.HERO_DOWN == True or self.HERO_DOWN_UP == True:
                self.image.clip_draw(self.frame * 100, (self.state+2) % 4 * 100, 100, 100, self.x, self.y)
            else:
                self.image.clip_draw(self.frame * 100, self.state % 4 * 100, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, self.state%4 * 100, 100, 100, self.x, self.y)


def handle_events():
    global running
    global hero
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            hero.handle_event(event)


def main():

    open_canvas()

    global hero
    global running

    hero = Hero()
    grass = Grass()

    running = True
    while running:
        handle_events()

        hero.update()

        clear_canvas()
        grass.draw()
        hero.draw()
        update_canvas()

        delay(0.04)

    close_canvas()


if __name__ == '__main__':
    main()