from pico2d import*
import random

class Eri:
    image = None

    LEFT_RUN , RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 0, 1, 2, 3
    KEY_UP , KEY_DOWN = False , False

    def handle_gun_shot(self):
        if self.shot_frames < 3:
            self.gun_resource_x = self.shot_frames*145
            if self.shot_frames == 0:
                self.gun_resource_x += 5
        elif self.shot_frames == 3:
            self.gun_shot_width = 90
            self.gun_resource_x = 443
        elif self.shot_frames == 10:
            self.gun_shot = False
        else:
            self.gun_resource_x += 103
        self.shot_frames += 1

    def handle_look_up(self):
        pass

    def handle_Jump(self):
        if self.Jump_frames < 7:
            self.y += 35 - self.Jump_frames*5
            if self.Jump_frames < 14:
                self.Jump_frames += 1
        elif self.Jump_frames == 7 and self.frame < 3.5:
            pass
        else:
            self.y -= (self.Jump_frames - 7) * 4
            if self.Jump_frames < 14:
                self.Jump_frames += 1

    def handle_left_run(self):
        self.x -= 10
        self.run_frames = (self.run_frames + 1) % 12
        if self.x <= 40:
            self.x = 40


    def handle_left_stand(self):
        if self.frame == 4:
            self.stand_frames = (self.stand_frames + 1) % 4
        if self.x > 610 and self.Open_Next_Map is True:
            self.x -= 10
            self.MapX += 10

    def handle_right_run(self):
        self.run_frames = (self.run_frames + 1) % 12
        if self.x >= 760 and self.Open_Next_Map is False:
            self.x = 760
        elif self.x > 460 and self.Open_Next_Map is True:
            self.x -= 10
            self.MapX += 10
        elif self.x >= 450 and self.Open_Next_Map is True:
            self.x = 450
            self.MapX += 10
        else:
            self.x += 10

    def handle_right_stand(self):
        if self.frame == 4:
            if self.stand_frames < 3:
                self.stand_frames += 1
            self.stand_frames = (self.stand_frames + 1) % 8
        if self.x > 610 and self.Open_Next_Map is True:
            self.x -= 10
            self.MapX += 10

    handle_state = {
        LEFT_RUN: handle_left_run,
        RIGHT_RUN: handle_right_run,
        LEFT_STAND: handle_left_stand,
        RIGHT_STAND: handle_right_stand
    }

    def __init__(self):
        self.x, self.y ,self.MapX = 100, 150, 0
        self.frame = random.randint(0,7)
        self.Jump_frames = 0
        self.state = 3
        self.stand_frames = 0
        self.run_frames = 0
        self.shot_frames = 0
        self.gun_resource_x = 0
        self.gun_shot_width = 0
        self.gun_shot = False
        self.Open_Next_Map = False
        self.jump = False
        if self.image is None:
            self.image = load_image('Tarma_PistolX250.png')

    def update(self):
        self.frame = (self.frame + 1) % 5
        self.handle_state[self.state](self)
        if self.jump is True:
            self.handle_Jump()
        if self.gun_shot is True:
            self.handle_gun_shot()

    def draw(self):
        if self.state == 0 or self.state == 1:
            self.image.clip_draw(self.run_frames * 97, 3325, 95, 70, self.x, self.y - 45)
            if self.gun_shot is False:
                self.image.clip_draw(self.run_frames*97, 3400, 95,87,self.x,self.y)
            else:
                if self.shot_frames < 3:
                    self.image.clip_draw(self.gun_resource_x, 2525, self.gun_shot_width, 87, self.x+28, self.y)
                else:
                    self.image.clip_draw(self.gun_resource_x, 2525, self.gun_shot_width, 87, self.x+28 , self.y)
        else:
            #self.image.clip_draw(self.stand_frames * 100, 4090, 100, 95, self.x, self.y-8)
            if self.stand_frames > 3:
                if self.gun_shot is False:
                    self.image.clip_draw(390, 4180, 95, 70, self.x - (7 - self.stand_frames) * 3, self.y - 55)
                    self.image.clip_draw((7-self.stand_frames) * 95, 4185, 95, 95, self.x, self.y-12)
                else:
                    self.image.clip_draw(390, 4180, 95, 70, self.x , self.y - 55)
                    if self.shot_frames < 3:
                        self.image.clip_draw(self.gun_resource_x, 2525, self.gun_shot_width, 87, self.x + 15, self.y-12)
                    else:
                        self.image.clip_draw(self.gun_resource_x, 2525, self.gun_shot_width, 87, self.x+15, self.y-12)
            else:
                if self.gun_shot is False:
                    self.image.clip_draw(390, 4180, 95, 70, self.x - self.stand_frames * 3, self.y - 55)
                    self.image.clip_draw(self.stand_frames * 95, 4185, 95, 95, self.x, self.y - 12)
                else:
                    self.image.clip_draw(390, 4180, 95, 70, self.x , self.y - 55)
                    if self.shot_frames < 3:
                        self.image.clip_draw(self.gun_resource_x, 2525, self.gun_shot_width, 87, self.x + 15,self.y - 12)
                    else:
                        self.image.clip_draw(self.gun_resource_x, 2525, self.gun_shot_width, 87, self.x+15, self.y - 12)

def handle_events():
    global running
    global boy
    global MapX
    global Open_next_Map

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                boy.state = boy.RIGHT_RUN
            elif event.key == SDLK_LEFT:
                boy.state = boy.LEFT_RUN
            elif event.key == SDLK_m:
                if Open_next_Map is False:
                    Open_next_Map = True
                    boy.Open_Next_Map = Open_next_Map
                else:
                    Open_next_Map = False
                    boy.Open_Next_Map = Open_next_Map
            elif event.key == SDLK_s:
                if boy.jump == False:
                    boy.frame = 0
                    boy.Jump_frames = 0
                    boy.jump = True
            elif event.key == SDLK_a:
                boy.shot_frames = 0
                boy.gun_resource_x = 0
                boy.gun_shot_width = 130
                boy.gun_shot = True


        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                boy.frame = 0
                boy.state = boy.RIGHT_STAND
            elif event.key == SDLK_LEFT:
                boy.frame = 0
                boy.state = boy.LEFT_STAND

def main():
    open_canvas()

    global boy
    global Open_next_Map

    Open_next_Map = False
    boy = Eri()

    Mission01_Map = load_image('Mission01_Map.png')

    global running
    running = True

    while running:
        handle_events()

        boy.update()

        clear_canvas()
        Mission01_Map.clip_draw(boy.MapX, 1743, 800, 600, 400, 300)
        boy.draw()
        update_canvas()

        delay(0.04)

    close_canvas()


if __name__ == '__main__':
    main()