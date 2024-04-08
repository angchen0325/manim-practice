from manim import *

class demo1(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
        
        