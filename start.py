from manimlib import *


class SquareToCircle(Scene):
    def construct(self) -> None:
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)

        # self.add(circle)
        square = Square()  # create a square
        square.set_fill(RED, opacity=0.5)  # set the color and transparency
        square.set_stroke(RED_E, width=4)  # set the color and transparency

        # show the creation of square on screen
        self.play(ShowCreation(square))
        self.wait(0.5)  # wait for 1 second
        # transform square into circle
        self.play(ReplacementTransform(square, circle))
        self.wait()  # wait for 1 second

        self.play(circle.animate.stretch(4, dim=0))
        self.play(Rotate(circle, TAU / 4))
        self.play(circle.animate.shift(2 * RIGHT).scale(0.25))
        circle.insert_n_curves(10)
        self.play(circle.animate.apply_complex_function(lambda z: z**2))

        text = Text("""
            In general, using the interactive shell
            is very helpful when developing new scenes
            """)

        self.play(Write(text))

        # always(circle.move_to, self.mouse_point)


class AnimatingMethods(Scene):
    def construct(self) -> None:
        grid = Tex(r"\pi").get_grid(10, 10, height=4)
        self.add(grid)

        self.play(grid.animate.shift(LEFT))

        self.play(grid.animate.set_color(YELLOW))
        self.wait()

        self.play(grid.animate.set_submobject_colors_by_gradient(BLUE, GREEN))
        self.wait()

        self.play(grid.animate.set_height(TAU - MED_SMALL_BUFF))
        self.wait()

        self.play(grid.animate.apply_complex_function(np.exp), run_time=5)
        self.wait()

        self.play(
            grid.animate.apply_function(
                lambda p: [
                    p[0] + 0.5 * math.sin(p[1]),
                    p[1] + 0.5 * math.sin(p[0]),
                    p[2]
                ]
            ),
            run_time=5,
        )
        self.wait()


class TextExample(Scene):
    def construct(self) -> None:
        text = Text("Here is a text", font="Consolas", font_size=90)
        difference = Text(
            """
            The most important difference between Text and TexText is that\n
            you can change the font more easily, but can't use the LaTeX grammar
            """,
            font="Arial", font_size=24,
            # t2c是一个由 文本-颜色 键值对组成的字典
            t2c={"Text": BLUE, "TexText": BLUE, "LaTeX": ORANGE, "difference": GREEN}
        )
        
        VGroup(text, difference).arrange(DOWN, buff=1)
        self.play(Write(text))
        self.play(FadeIn(difference, UP))
        self.wait(1)
        
        fonts = Text(
            "And you can also set the font according to different words",
            font="Arial",
            t2f={"font": "Consolas", "words": "Consolas"},
            t2c={"font": BLUE, "words": GREEN}
        )
        fonts.set_width(FRAME_WIDTH - 1)
        slant = Text(
            "And the same as slant and weight",
            font="Times New Roman",
            t2s={"slant": ITALIC},
            t2w={"weight": BOLD, "and": BOLD},
            t2c={"slant": ORANGE, "weight": RED, "and": BLUE}
        )
        VGroup(fonts, slant).arrange(DOWN, buff=0.8)
        
        self.play(FadeOut(text), FadeOut(difference, shift=DOWN))
        self.play(Write(fonts))
        self.wait()
        self.play(Write(slant))
        self.wait()
        self.play(FadeOut(fonts, shift=LEFT), FadeOut(slant, shift=RIGHT))


class TexTransformExample(Scene):
    def construct(self):
        to_isolate = ["B", "C", "=", "(", ")"]
        lines = VGroup(
            Tex("A^2", "+", "B^2", "=", "C^2"),
            Tex("A^2", "=", "C^2", "-", "B^2"),
            Tex("A^2 = (C + B)(C - B)", isolate=["A^2", *to_isolate]),
            # Tex("A^2", "=", "(", "C", "+", "B", ")", "(", "C", "-", "B", ")"),
            Tex("A = \\sqrt{(C + B)(C - B)}", isolate=["A", *to_isolate])
        )
        lines.arrange(DOWN, buff=LARGE_BUFF)
        for line in lines:
            line.set_color_by_tex_to_color_map({
                "A": BLUE, "A^2": BLUE,
                "B": TEAL, "B^2": TEAL,
                "C": GREEN, "C^2": GREEN,
            })

        play_kw = {"run_time": 2}
        self.add(lines[0])
        self.play(
            TransformMatchingTex(
                lines[0].copy(), lines[1],
                path_arc=90 * DEGREES,
            ),
            **play_kw
        )
        self.wait()

        self.play(
            TransformMatchingTex(lines[1].copy(), lines[2]),
            **play_kw
        )
        self.wait()
        # …这看起来很好，但由于在lines[2]中没有匹配"C^2"或"B^2"的tex，这些子物件会淡出
        # 而C和B两个子物件会淡入，如果我们希望C^2转到C，而B^2转到B，我们可以用key_map来指定
        self.play(FadeOut(lines[2]))
        self.play(
            TransformMatchingTex(
                lines[1].copy(), lines[2],
                key_map={
                    "C^2": "C",
                    "B^2": "B",
                }
            ),
            **play_kw
        )
        self.wait()
        
        new_line2 = Tex("A^2 = (C + B)(C - B)", isolate=["A", *to_isolate])
        new_line2.replace(lines[2])
        new_line2.match_style(lines[2])

        self.play(
            TransformMatchingTex(
                new_line2, lines[3],
                # transform_mismatches=True,
            ),
            **play_kw
        )
        self.wait(1.5)
        self.play(FadeOut(lines, RIGHT))


class SurfaceExample(Scene):
    CONFIG = {
        "camera_class": ThreeDCamera,
    }

    def construct(self) -> None:
        surface_text = Text("For 3d scenes, try using surfaces")
        surface_text.fix_in_frame()
        surface_text.to_edge(UP)
        self.add(surface_text)
        self.wait(0.1)

        torus1 = Torus(r1=1, r2=1)
        torus2 = Torus(r1=3, r2=1)
        sphere = Sphere(radius=3, resolution=torus1.resolution)

        day_texture = "EarthTextureMap.jpg"
        night_texture = "NightEarthTextureMap.jpg"

        surfaces = [
            TexturedSurface(surface, day_texture, night_texture)
            for surface in [sphere, torus1, torus2]
        ]

        for mob in surfaces:
            mob.shift(IN)
            mob.mesh = SurfaceMesh(mob)
            mob.mesh.set_stroke(BLUE, 1, opacity=0.5)

        # 设置视角
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=-30 * DEGREES,
            phi=70 * DEGREES,
        )

        surface = surfaces[0]

        self.play(
            FadeIn(surface),
            ShowCreation(surface.mesh, lag_ratio=0.01, run_time=3),
        )
        for mob in surfaces:
            mob.add(mob.mesh)
        surface.save_state()
        self.play(Rotate(surface, PI / 2), run_time=2)
        for mob in surfaces[1:]:
            mob.rotate(PI / 2)

        self.play(
            Transform(surface, surfaces[1]),
            run_time=3
        )

        self.play(
            Transform(surface, surfaces[2]),
            # 在过渡期间移动相机帧
            # frame.increment_phi, -10 * DEGREES,
            # frame.increment_theta, -20 * DEGREES,
            run_time=3
        )

        # 添加自动旋转相机帧
        frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))

        # 移动光源
        light_text = Text("You can move around the light source")
        light_text.move_to(surface_text)
        light_text.fix_in_frame()

        self.play(FadeTransform(surface_text, light_text))
        light = self.camera.light_source
        self.add(light)
        light.save_state()
        # self.play(light.move_to, 3 * IN, run_time=5)
        # self.play(light.shift, 10 * OUT, run_time=5)

        drag_text = Text("Try moving the mouse while pressing d or s")
        drag_text.move_to(light_text)
        drag_text.fix_in_frame()

        self.play(FadeTransform(light_text, drag_text))
        self.wait()
