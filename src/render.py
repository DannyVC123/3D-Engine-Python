from tkinter import *

from model import Model
from model_lib import Model_Lib
from obj_parser import Obj_Parser
from lin_alg import Lin_Alg

class Render:
    w, h = 800, 800

    def __init__(self, model):
        self.create_ui()

        self.model = model
        self.focal_length = 500
        model.draw(self.canvas, self.focal_length, Render.w, Render.h)

        self.window.mainloop()

    def create_ui(self):
        self.window = Tk()
        self.window.title("3D Render")
        self.window.geometry(f'{Render.w}x{Render.h}')

        self.create_canvas()
        
        param_frame = Frame(self.window)
        param_frame.pack(padx = 10, pady = 10)
        param_frame.place(relx = 1.0, rely = 1.0, anchor = SE, x = -20, y = -20)

        parameters = Label(param_frame, text = "Parameters")
        parameters.grid(row = 0, column = 0, columnspan = 2)

        self.create_scale('Focal Length', 500, 3000, 1, frame = param_frame)
        titles = ['X-Rotation', 'Y-Rotation', 'Z-Rotation']
        self.rotation_scales = []
        for i in range(3):
            _, v = self.create_scale(titles[i], 0, 360, i+2, i, frame = param_frame)
            self.rotation_scales.append([v, 0])
        
        self.img = PhotoImage(file = "./images/axes_reference_rh_small.png")
        label = Label(self.window, image = self.img)
        label.place(relx = 1.0, rely = 0.0, anchor = NE)

    def create_canvas(self):
        self.canvas = Canvas(self.window)
        self.canvas.pack(fill = BOTH, expand = 1)

        self.canvas.bind("<Button-1>", self.save_posn)
        self.canvas.bind("<B1-Motion>", self.complex_rotate)
    
    def create_scale(self, title, start, end, row, tag = -1, frame = None):
        if frame == None:
            frame = self.window
        
        title_label = Label(frame, text = title)
        title_label.grid(row = row, column = 0)

        v = DoubleVar()
        scale = Scale(
            frame,
            variable = v,
            from_ = start,
            to = end,
            length = 200,
            orient = HORIZONTAL,
            command = lambda value, tag = tag: self.simple_rotate(value, tag)
        )
        scale.grid(row = row, column = 1)

        return (scale, v)
    
    def save_posn(self, event):
        self.x0, self.y0 = event.x, event.y

    def simple_rotate(self, value_str, tag):
        value = float(value_str)

        if tag == -1:
            self.focal_length = value
        else:
            prev_theta = self.rotation_scales[tag][1]
            d_theta = value - prev_theta
            self.model.simple_rotate(tag, d_theta)
            self.rotation_scales[tag][1] = value
        
        self.model.draw(self.canvas, self.focal_length, Render.w, Render.h)

    def complex_rotate(self, event):
        x1, y1 = event.x, event.y
        new_rotations = self.model.complex_rotate(
            self.x0 - Render.w / 2,
            Render.h - self.y0 - Render.h / 2,
            x1 - Render.w / 2,
            Render.h - y1 - Render.h / 2
        )
        self.model.draw(self.canvas, self.focal_length, Render.w, Render.h)

        for i in range(len(new_rotations)):
            self.rotation_scales[i][0].set(new_rotations[i])
            self.rotation_scales[i][1] = new_rotations[i]

if __name__ == "__main__":
    # render = Render(Model_Lib.cube())
    # dog = Obj_Parser.parse_obj('./models/ORIGAM_CHIEN_Free.obj', scale_factor = 5, color = [205, 175, 135])
    wolf = Obj_Parser.parse_obj('./models/wolf_lp.obj', scale_factor = 2, color = [164, 159, 150], has_vn = False)
    # deer = Obj_Parser.parse_obj('./models/deer.obj', scale_factor = 0.5, color = [205, 175, 135], has_vn = False)

    # pikachu = Obj_Parser.parse_obj('./models/pokemon/pikachu.obj', scale_factor = 8, color = [242, 210, 71], outward_vn = False)
    # squirtle = Obj_Parser.parse_obj('./models/pokemon/squirtle.obj', scale_factor = 8, color = [131, 206, 232])
    render = Render(wolf)