from manim import *
import numpy as np
from scipy.stats import norm, gamma


TEAL = "#00A8C8"
PDF_COLOR = "#FF9F1C"
CDF_COLOR = "#C77DFF"
UNIFORM_COLOR = "#27AE60"
SAMPLE_YELLOW = "#F4C542"

def setup_pit_layout(scene, lam=1):
    alpha = 5
    theta = 1
    title = Text("Probability Integral Transform", color=TEAL)

    shadow = title.copy().set_color("#7A3E00").set_opacity(0.55)
    shadow.shift(RIGHT * 0.04 + DOWN * 0.04)

    title_group = VGroup(shadow, title)
    title_group.move_to([0,7.5,0])

    scene.play(Write(title_group), run_time=2)
    scene.wait(1)

    cdf_axes = Axes(
        x_range=[0, 10, 1],
        y_range=[0, 1.2, 0.2],
        x_length=6,
        y_length=4,
        tips=True,
        axis_config={"include_numbers": True}
    ).scale(0.8)
    cdf_axes.next_to(title_group, DOWN, buff=0.81).shift(DOWN * 0.8)

    uniform_axes = Axes(
        x_range=[0, 1.2, 0.2],
        y_range=[0, 1.2, 1],
        x_length=4,
        y_length=4,
        tips=True,
         axis_config={"include_numbers": False},
        x_axis_config={
            "include_numbers": True,
            "numbers_to_include": [0, 1],
        },
        y_axis_config={
            "include_numbers": True,
            "numbers_to_include": [0, 1],
        },
    ).scale(0.8)
    uniform_axes.move_to(ORIGIN).shift(DOWN * 2.0)

    cdf_title = Text("1. CDF (Gamma(5,1) Distribution)", font_size=24, color=CDF_COLOR).next_to(cdf_axes, UP, buff=0.15)
    uniform_title = Text("2. Uniform(0,1)", font_size=24, color="#27AE60").next_to(uniform_axes, UP)

    scene.play(Create(cdf_axes), Write(cdf_title))
    scene.play(Create(uniform_axes), Write(uniform_title))


    cdf_curve = cdf_axes.plot(
        lambda x: gamma.cdf(x, a=alpha, scale=theta),
        x_range=[0, 10],
        color=CDF_COLOR,
        stroke_width=3
    )
    scene.play(Create(cdf_curve))


    cdf_axis_labels = cdf_axes.get_axis_labels(
        x_label=MathTex("x").scale(0.7),
        y_label=MathTex("")
    ).shift(DOWN * 0.5)

    scene.play(
        Write(cdf_axis_labels)
    )

    return cdf_axes, uniform_axes

def animate_one_pit_sample(scene, lam, cdf_axes, uniform_axes):
    alpha = 5
    theta = 1

    x_sample = np.random.gamma(shape=alpha, scale=theta)

    while x_sample > 10:
        x_sample = np.random.gamma(shape=alpha, scale=theta)

    u_sample = gamma.cdf(x_sample, a=alpha, scale=theta)

    SAMPLE_COLOR = YELLOW

    cdf_sample_dot = Dot(
        cdf_axes.c2p(x_sample, 0),
        color=SAMPLE_COLOR,
        radius=0.07
    )

    cdf_sample_label = MathTex(
        f"x = {x_sample:.2f}"
    ).scale(0.6).set_color(SAMPLE_COLOR)
    cdf_sample_label.next_to(cdf_sample_dot, DOWN, buff=0.1)

    cdf_curve_dot = Dot(
        cdf_axes.c2p(x_sample, u_sample),
        color=SAMPLE_COLOR,
        radius=0.07
    )

    vertical_to_cdf = DashedLine(
        cdf_axes.c2p(x_sample, 0),
        cdf_axes.c2p(x_sample, u_sample),
        color=SAMPLE_COLOR,
        stroke_width=3
    )

    horizontal_to_yaxis = DashedLine(
        cdf_axes.c2p(x_sample, u_sample),
        cdf_axes.c2p(0, u_sample),
        color=SAMPLE_COLOR,
        stroke_width=3
    )

    u_label = MathTex(
        f"F({x_sample:.2f}) = {u_sample:.2f}"
    ).scale(0.6).set_color(SAMPLE_COLOR)
    u_label.next_to(cdf_axes.c2p(0, u_sample), LEFT, buff=0.35)

    scene.play(
        FadeIn(cdf_sample_dot),
        Write(cdf_sample_label),
        run_time=0.5
    )

    scene.play(
        Create(vertical_to_cdf),
        TransformFromCopy(cdf_sample_dot, cdf_curve_dot),
        run_time=0.6
    )

    scene.play(
        Create(horizontal_to_yaxis),
        Write(u_label),
        run_time=0.6
    )

    u_output_dot = Dot(
        cdf_axes.c2p(0, u_sample),
        color=SAMPLE_COLOR,
        radius=0.08
    )

    uniform_dot = Dot(
        uniform_axes.c2p(u_sample, 0),
        color=SAMPLE_COLOR,
        radius=0.08
    )

    uniform_label = MathTex(
        f"u = {u_sample:.2f}"
    ).scale(0.6).set_color(SAMPLE_COLOR)
    uniform_label.next_to(uniform_dot, DOWN, buff=0.1)

    scene.play(FadeIn(u_output_dot), run_time=0.3)

    scene.play(
        TransformFromCopy(u_output_dot, uniform_dot),
        Write(uniform_label),
        run_time=0.6
    )

    scene.play(
        FadeOut(cdf_sample_label),
        FadeOut(u_label),
        FadeOut(uniform_label),
        FadeOut(vertical_to_cdf),
        FadeOut(horizontal_to_yaxis),
        FadeOut(u_output_dot),
        FadeOut(cdf_sample_dot),
        FadeOut(cdf_curve_dot),
        run_time=0.25
    )

    return uniform_dot


def animate_pit_timelapse(scene, uniform_axes, existing_uniform_object):
    moved_dots = VGroup()
    move_animations = []


    # -------------------------
    # Stage 1: dots move from CDF to Uniform axis
    # -------------------------
    # for _ in range(n_move):
    #     x_sample = np.random.exponential(scale=1/lam)

    #     while x_sample > 5:
    #         x_sample = np.random.exponential(scale=1/lam)

    #     u_sample = 1 - np.exp(-lam * x_sample)

    #     start_dot = Dot(
    #         cdf_axes.c2p(x_sample, u_sample),
    #         color=YELLOW,
    #         radius=0.08
    #     )

    #     end_dot = Dot(
    #         uniform_axes.c2p(u_sample, 0),
    #         color=YELLOW,
    #         radius=0.08
    #     )

    #     moved_dots.add(end_dot)
    #     move_animations.append(TransformFromCopy(start_dot, end_dot))

    # scene.play(
    #     LaggedStart(*move_animations, lag_ratio=0.03),
    #     run_time=4
    # )

    all_dots = VGroup()

    x_count = 55
    y_count = 35
    dot_radius = 0.02

    prefill_height = 0.1

    # -------------------------
    # Stage 1: prefill y < 0.1
    # -------------------------
    prefilled_dots = VGroup()

    for j in range(y_count):
        y_value = j / (y_count - 1)

        if y_value < prefill_height:
            for i in range(x_count):
                x_value = i / (x_count - 1)

                dot = Dot(
                    uniform_axes.c2p(x_value, y_value),
                    color=YELLOW,
                    radius=dot_radius
                )

                prefilled_dots.add(dot)

    scene.play(Transform(existing_uniform_object, prefilled_dots))
    all_dots.add(prefilled_dots)

     # -------------------------
    # Stage 2: grow from y = 0.1 to y = 1
    # -------------------------
    for j in range(y_count):
        y_value = j / (y_count - 1)

        if y_value >= prefill_height:
            layer_dots = VGroup()
            layer_animations = []

            for i in range(x_count):
                x_value = i / (x_count - 1)

                dot = Dot(
                    uniform_axes.c2p(x_value, y_value),
                    color=YELLOW,
                    radius=dot_radius
                )

                layer_dots.add(dot)
                layer_animations.append(FadeIn(dot, scale=0.4))

            all_dots.add(layer_dots)

            scene.play(
                LaggedStart(*layer_animations, lag_ratio=0.002),
                run_time=0.18
            )

    return all_dots


# def show_uniform_histogram(scene, lam, uniform_axes, n=10000, bins=50):
#     samples = np.random.exponential(scale=1/lam, size=n)
#     u_values = 1 - np.exp(-lam * samples)

#     hist, bin_edges = np.histogram(
#         u_values,
#         bins=bins,
#         range=(0, 1),
#         density=True
#     )

#     bars = VGroup()

#     for h, left, right in zip(hist, bin_edges[:-1], bin_edges[1:]):
#         bar_width = uniform_axes.x_axis.unit_size * (right - left)
#         bar_height = uniform_axes.y_axis.unit_size * h

#         bar = Rectangle(
#             width=bar_width,
#             height=bar_height,
#             fill_color=YELLOW,
#             fill_opacity=0.65,
#             stroke_color=WHITE,
#             stroke_width=1
#         )

#         bar.move_to(
#             uniform_axes.c2p((left + right) / 2, h / 2)
#         )

#         bars.add(bar)

#     scene.play(
#         LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.04),
#         run_time=2
#     )

#     return bars


def create_uniform_histogram_bars(lam, uniform_axes, n=10000, bins=20):
    samples = np.random.exponential(scale=1/lam, size=n)
    u_values = 1 - np.exp(-lam * samples)

    hist, bin_edges = np.histogram(
        u_values,
        bins=bins,
        range=(0, 1),
        density=True
    )

    bars = VGroup()

    for h, left, right in zip(hist, bin_edges[:-1], bin_edges[1:]):

        bar_height_value = 1  # flat uniform density height

        bar = Rectangle(
            width=uniform_axes.x_axis.unit_size * (right - left),
            height=uniform_axes.y_axis.unit_size * bar_height_value,
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=0
        )

        bar.move_to(
            uniform_axes.c2p((left + right) / 2, h / 2)
        )

        bars.add(bar)

    return bars


def animate_flat_uniform_histogram(scene, uniform_axes, bins=20):
    bars = VGroup()
    trackers = []

    bar_height_value = 1.0
    bin_edges = np.linspace(0.009, 0.97, bins + 1)

    for left, right in zip(bin_edges[:-1], bin_edges[1:]):
        tracker = ValueTracker(0)
        trackers.append(tracker)

        bin_width = right - left
        mid = (left + right) / 2

        def make_bar(tracker=tracker, mid=mid, bin_width=bin_width):
            current_height = tracker.get_value()

            bar = Rectangle(
                width=uniform_axes.x_axis.unit_size * bin_width * 1,  # slight overlap
                height=uniform_axes.y_axis.unit_size * current_height,
                fill_color=YELLOW,
                fill_opacity=1,
                stroke_width=0
            )

            # IMPORTANT: center at height/2 so bottom sits on x-axis
            Y_OFFSET = 0.1
            bar.move_to(
                uniform_axes.c2p(mid, current_height / 2 + Y_OFFSET)
            )

            return bar

        bar = always_redraw(make_bar)
        bars.add(bar)

    scene.add(bars)

    scene.play(
        *[tracker.animate.set_value(bar_height_value) for tracker in trackers],
        run_time=2
    )

    return bars