from manim import *
import numpy as np
import scipy.stats as stats

# Utility functions
def get_distribution_chart(distribution, axes_config, color=BLUE):
    """
    Creates a bar chart for the given distribution.
    """
    axes = Axes(**axes_config)
    bars = VGroup()
    for i, prob in enumerate(distribution):
        bar = Rectangle(
            width=0.6,
            height=prob * axes.y_length,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0
        )
        bar.stretch_to_fit_width(0.6)
        bar.next_to(axes.c2p(i + 1, 0), UP, buff=0)
        bars.add(bar)
    return VGroup(axes, bars)

def get_brick(color=GREEN, height=0.2, width=0.8):
    """
    Creates a brick representing a trajectory or data point.
    """
    return Rectangle(
        stroke_width=0,
        fill_color=color,
        fill_opacity=1,
        height=height,
        width=width
    )

class MSEVsGaussianMLEMultimodal(Scene):
    def construct(self):
        ### 1. INTRODUCTION: TITLE ###
        title = Text("MSE Loss for Multimodal Data", font_size=24)
        title.to_edge(UP)
        self.add(title)
        self.wait(1)

        # Create Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1, 5, 1],
            x_length=8,
            y_length=5,
            axis_config={"include_numbers": True},
            tips=False,
        )
        axes.to_edge(DOWN)
        self.play(Create(axes, run_time=2))
        self.wait()

        ### 9. INTRODUCE MULTIMODAL DISTRIBUTION ###
        # Show a bimodal distribution to contrast with Gaussian
        bimodal_mu1 = -2.0
        bimodal_mu2 = 2.0
        bimodal_sigma = 0.25
        bimodal_weights = [0.5, 0.5]

        # Define the bimodal probability density function
        def bimodal_pdf(x):
            return (stats.norm.pdf(x, loc=bimodal_mu1, scale=bimodal_sigma) * bimodal_weights[0] +
                    stats.norm.pdf(x, loc=bimodal_mu2, scale=bimodal_sigma) * bimodal_weights[1])

        # Plot the bimodal distribution
        bimodal_curve = axes.plot(
            bimodal_pdf        )

        # Animate the transformation
        self.play(FadeIn(bimodal_curve))
        self.wait(1)

        ### 10. SHOW HOW MSE FAILS WITH MULTIMODAL DISTRIBUTION ###
        # Recalculate sample mean for bimodal distribution
        n_samples = 100
        # Generate synthetic data: y = mu + Gaussian noise
        np.random.seed(42)
        n_samples = 100
        mu_true = 2.0
        sigma_true = 0.25
        X = np.linspace(-3, 3, n_samples)
        Y = mu_true + sigma_true * np.random.randn(n_samples)

        bimodal_Y = np.concatenate([
            bimodal_mu1 + sigma_true * np.random.randn(n_samples),
            bimodal_mu2 + sigma_true * np.random.randn(n_samples)
        ])
        bimodal_sample_mean = np.mean(bimodal_Y)


        ### 10. CREATE TWO BALLS ###
        # Center the balls at the means of the bimodal distribution
        # Gaussian distribution for centered and dissipating effect
        ball_1 = VGroup(*[
            Dot(
                point=axes.c2p(
                    -2 + np.random.normal(0, 0.3),  # Gaussian around -2 with std dev 0.3
                    1 + np.random.normal(0, 0.3)   # Gaussian around 1 with std dev 0.3
                ),
                color=BLUE
            )
            for _ in range(50)
        ])

        ball_2 = VGroup(*[
            Dot(
                point=axes.c2p(
                    2 + np.random.normal(0, 0.3),  # Gaussian around 2 with std dev 0.3
                    1 + np.random.normal(0, 0.3)  # Gaussian around 1 with std dev 0.3
                ),
                color=BLUE
            )
            for _ in range(50)
        ])


        # Animate the data
        self.play(FadeIn(ball_1, lag_ratio=0.1), FadeIn(ball_2, lag_ratio=0.1), run_time=2)
        self.wait(1)

        # Transition to new sample mean
        transition_text_new = Tex("The unimodal assumption no longer holds", font_size=32, color=RED)
        transition_text_new.to_corner(UP, buff=1.0)
        self.play(FadeIn(transition_text_new, run_time=2))
        self.wait(1)

        # Calculate new sample mean
        new_sample_mean = np.mean(bimodal_Y)
        new_mean_dot = Dot(point=axes.c2p(0, 1, 0), color=RED)
        self.play(FadeIn(new_mean_dot))
        self.wait(0.5)

        # Draw horizontal line at sample mean
        mean_line = axes.get_vertical_line(axes.c2p(new_sample_mean, 5, 0), color=RED)
        mean_label = MathTex("\\hat{\\mu} = \\frac{1}{n}\\sum x^i", font_size=28, color=RED)
        mean_label.next_to(mean_line, RIGHT, buff=0.1)
        mean_label.to_corner(UP + LEFT, buff=3.0)

        self.play(Create(mean_line), Write(mean_label))
        self.wait(1)


        # Highlight discrepancy between sample mean and modes
        mode1 = Dot(point=axes.c2p(-bimodal_mu2, 1, 0), color=ORANGE)
        mode2 = Dot(point=axes.c2p(bimodal_mu2, 1, 0), color=ORANGE)
        self.play(FadeIn(mode1), FadeIn(mode2))
        self.wait(1)

        # Draw arrows from mean to each mode
        arrow1 = Arrow(new_mean_dot.get_center(), mode1.get_center(), color=RED)
        arrow2 = Arrow(new_mean_dot.get_center(), mode2.get_center(), color=RED)
        self.play(GrowArrow(arrow1), GrowArrow(arrow2))
        self.wait(1)

        # Add labels to arrows
        arrow_label1 = Tex("Mode 1", color=ORANGE, font_size=24).next_to(mode1, UP, buff=1.0)
        arrow_label2 = Tex("Mode 2", color=ORANGE, font_size=24).next_to(mode2, UP, buff=1.0)
        self.play(Write(arrow_label1), Write(arrow_label2))
        self.wait(10)

        