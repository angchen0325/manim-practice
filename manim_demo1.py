from manim import *

class demo1(Scene):
    def construct(self):
        circle = Square()
        self.play(Create(circle))
        
        