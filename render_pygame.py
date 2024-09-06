import pygame as pg
import sys
from model import Model
from model_lib import Model_Lib
from obj_parser import Obj_Parser
from lin_alg import Lin_Alg

class Render:
    w, h = 800, 800

    def __init__(self, model):
        self.window = pg.display.set_mode((Render.w, Render.h))
        pg.display.set_caption("3D Render")

        self.model = model
        self.focal_length = 3000

        self.run()

    def run(self):
        self.model.draw(self.window, self.focal_length)
        pg.display.flip()

        clock = pg.time.Clock()
        mouse_down = False
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if not mouse_down and event.button == 1:  # Left mouse button
                        self.x0, self.y0 = event.pos
                        mouse_down = True
                elif event.type == pg.MOUSEBUTTONUP:
                    mouse_down = False
                elif event.type == pg.MOUSEMOTION:
                    if mouse_down:  # Left mouse button pressed
                        self.complex_rotate(event.pos)

            clock.tick(60)  # Limit to 60 FPS

    def complex_rotate(self, pos):
        x1, y1 = pos
        new_rotations = self.model.complex_rotate(
            self.x0 - Render.w / 2,
            Render.h - self.y0 - Render.h / 2,
            x1 - Render.w / 2,
            Render.h - y1 - Render.h / 2
        )
        self.model.draw(self.window, self.focal_length)
        pg.display.flip()

if __name__ == "__main__":
    # dog = Obj_Parser.parse_obj('./models/ORIGAM_CHIEN_Free.obj', scale_factor = 5, color = [205, 175, 135])
    # wolf = Obj_Parser.parse_obj('./models/wolf_lp.obj', scale_factor=2, color=[164, 159, 150], has_vn=False)
    deer = Obj_Parser.parse_obj('./models/deer.obj', scale_factor = 0.5, color = [205, 175, 135], has_vn = False)
    
    # pikachu = Obj_Parser.parse_obj('./models/pokemon/pikachu.obj', scale_factor = 8, color = [242, 210, 71], outward_vn = False)
    # squirtle = Obj_Parser.parse_obj('./models/pokemon/squirtle.obj', scale_factor = 8, color = [131, 206, 232])
    
    render = Render(deer)
