from manim import *
import numpy as np
from pit_helpers import *

DARK_BLUE = "#063B63"
TEAL = "#00A8C8"
LIGHT_TEAL = "#3ECDE3"
SAMPLE_YELLOW = "#F4C542"
AXIS_WHITE = "#FFFFFF"

PDF_COLOR =  "#C77DFF"     
CDF_COLOR =   "#F4A261"  
SAMPLE_COLOR = SAMPLE_YELLOW   # yellow highlight
UNIFORM_COLOR = "#00A8C8"

# configurations
config.background_color = DARK_BLUE
config.frame_height = 16
config.frame_width = 9
config.pixel_height = 1920
config.pixel_width = 1080


class Summary(Scene):

    def construct(self):
        title = Text("Probability Integral Transform", color=TEAL)

        shadow = title.copy().set_color("#7A3E00").set_opacity(0.55)
        shadow.shift(RIGHT * 0.04 + DOWN * 0.04)

        title_group = VGroup(shadow, title)
        title_group.move_to([0,7.5,0])

        self.play(Write(title_group), run_time=2)
        self.wait(1)

        summary_title = Text(
            "Mathematically...",
            font_size=36,
            color=TEAL
        ).to_edge(UP, buff=1.1)

        line1 = Text(
            "For any continuous random variable X,",
            font_size=25,
            color=WHITE
        )

        formula = MathTex(
            r"U = F(X) \sim \mathrm{Uniform}(0,1)",
            font_size=42,
            color=YELLOW
        )

        line2 = Text(
            "as long as F is the CDF of X.",
            font_size=25,
            color=WHITE
        )

        line3 = Text(
            "Different distributions go in...",
            font_size=24,
            color=WHITE
        )

        line4 = Text(
            "but the transformed values come out uniform.",
            font_size=23,
            color=YELLOW
        )

        summary_group = VGroup(
            summary_title,
            line1,
            formula,
            line2,
            line3,
            line4
        ).arrange(DOWN, buff=0.35)

        summary_group.set_max_width(config.frame_width - 0.7)
        summary_group.move_to(ORIGIN)

        self.play(Write(summary_title))
        self.play(FadeIn(line1, shift=UP * 0.2))
        self.play(Write(formula))
        self.play(FadeIn(line2, shift=UP * 0.2))
        self.wait(0.5)
        self.play(FadeIn(line3, shift=UP * 0.2))
        self.play(FadeIn(line4, shift=UP * 0.2))

        self.wait(2)



class OneSampleScene(Scene):
    def construct(self):
        lam = 1
        cdf_axes, uniform_axes = setup_pit_layout(self, lam)

        animate_one_pit_sample(
            self,
            lam,
            cdf_axes,
            uniform_axes
        )

        self.wait(1)

class TenSampleScene(Scene):
    def construct(self):
        lam = 1
        cdf_axes, uniform_axes = setup_pit_layout(self, lam)

        uniform_dots = VGroup()

        for _ in range(10):
            dot = animate_one_pit_sample(
                self,
                lam,
                cdf_axes,
                uniform_axes
            )
            uniform_dots.add(dot)

        self.wait(1)
        

class TimeLapseToHistogramScene(Scene):
    def construct(self):
        lam = 1
        cdf_axes, uniform_axes = setup_pit_layout(self, lam)

        uniform_dots = VGroup()

        for _ in range(10):
            dot = animate_one_pit_sample(
                self,
                lam,
                cdf_axes,
                uniform_axes
            )
            uniform_dots.add(dot)

        self.wait(1)

        all_dots = animate_pit_timelapse(
            self,
            uniform_axes,
            uniform_dots
        )

        self.wait(0.5)

        result_text = Paragraph(
            "With many repetitions,",
            "the transformed values become Uniform(0,1)",
            font_size=24,
            color="#27AE60",
            line_spacing=0.8,
            alignment="center"
        ).next_to(uniform_axes, DOWN, buff=0.25)

        self.play(Write(result_text))
        self.wait(2)
