import math
import cairo

def rounded(ct, x, y, lx, ly, p):
    lx = lx + x
    ly = ly + y
    ct.new_sub_path()
    ct.move_to(x+p, y)

    ct.line_to(lx-p, y)
    ct.curve_to(lx,y, lx, y+p, lx, y+p)
    ct.line_to(lx, ly-p)
    ct.curve_to(lx,ly, lx-p, ly, lx-p, ly)
    ct.line_to(x+p, ly)
    ct.curve_to(x,ly, x, ly-p, x, ly-p)
    ct.line_to(x, y+p)
    ct.curve_to(x,y, x+p, y, x+p, y)
    ct.close_path()
    return

def around(ct, x, y, lx, ly):
    fx = lx + x
    fy = ly + y
    ct.new_sub_path()
    ct.move_to(x, y)
    ct.line_to(x+(lx/2), y)
    ct.curve_to(x, y, x, y+(ly/2), x, y+(ly/2))
    ct.close_path()
    ct.new_sub_path()
    ct.move_to(fx, y)
    ct.line_to(x+(lx/2), y)
    ct.curve_to(fx, y, fx, y+(ly/2), fx, y+(ly/2))
    ct.close_path()
    ct.new_sub_path()
    ct.move_to(x, fy)
    ct.line_to(x+(lx/2), fy)
    ct.curve_to(x, fy, x, y+(ly/2), x, y+(ly/2))
    ct.close_path()
    ct.new_sub_path()
    ct.move_to(fx,fy)
    ct.line_to(x+(lx/2), fy)
    ct.curve_to(fx, fy, fx, y+(ly/2), fx, y+(ly/2))
    ct.close_path()
    ct.fill()
    return

