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

class MSEVsGaussianMLE(Scene):
    def construct(self):
        ### 1. INTRODUCTION: TITLE ###
        title = Text("MSE Loss as Gaussian Maximum Likelihood", font_size=24)
        title.to_edge(UP)
        self.add(title)
        self.wait(1)

        ### 2. GENERATE AND DISPLAY DATA POINTS ###
        # Generate synthetic data: y = mu + Gaussian noise
        np.random.seed(42)
        n_samples = 100
        mu_true = 0.0
        sigma_true = 0.4
        X = mu_true + sigma_true * np.random.randn(n_samples)
        Y = mu_true + sigma_true * np.random.randn(n_samples)+1

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

        # Plot Data Points
        data_dots = VGroup()
        for x, y in zip(X, Y):
            dot = Dot(point=axes.c2p(x, y, 0), color=BLUE)
            data_dots.add(dot)
        self.play(LaggedStartMap(FadeIn, data_dots, lag_ratio=0.1, run_time=2))
        self.wait(1)

        ### 3. PRESENT MSE LOSS FUNCTION ###
        mse_title = Tex("Mean Squared Error (MSE) Loss", font_size=36)
        mse_title.to_corner(UP + RIGHT, buff=1.0)
        self.play(Write(mse_title))
        self.wait(0.5)

        mse_eq = MathTex(
            "L(\\hat{x}) = \\frac{1}{n} \\sum_{i=1}^n ||x^i - \\hat{x}^i||^2",
            font_size=32
        )
        mse_eq.next_to(mse_title, DOWN, buff=0.5)
        self.play(Write(mse_eq))
        self.wait(1)

        ### 4. LINK MSE TO GAUSSIAN MLE ###
        # Explain that MSE corresponds to Gaussian MLE with fixed variance
        explanation = Tex(
            "Assume $x^i \\sim \\mathcal{N}(\\mu, \\sigma^2)$ with fixed $\\sigma^2$",
            font_size=32
        )
        explanation.next_to(mse_eq, DOWN, buff=1.0)
        self.play(FadeIn(explanation, run_time=2))
        self.wait(1)

        # Show the negative log-likelihood for Gaussian
        neg_log_likelihood = MathTex(
            "-\\sum_{i=1}^n \\log p(x^i | \\hat{x}^i; \\theta) = \\text{const} + \\text{const} \\sum_{i=1}^n ||x^i - \\hat{x}^i||^2",
            font_size=25
        )
        neg_log_likelihood.next_to(explanation, DOWN, buff=0.5)
        self.play(Write(neg_log_likelihood))
        self.wait(1)

        ### 5. TRANSITION TO SAMPLE MEAN ###
        transition_text = Tex("Minimizing MSE is equivalent to maximizing the likelihood", font_size=32)
        transition_text.to_corner(DOWN)
        self.play(FadeIn(transition_text, run_time=2))
        self.wait(1)

        # Highlight that the solution is the sample mean
        self.play(
            Indicate(mse_eq, color=YELLOW, scale_factor=1.2),
            Indicate(neg_log_likelihood, color=YELLOW, scale_factor=1.2)
        )
        self.wait(1)

        ### 6. CALCULATE AND DISPLAY SAMPLE MEAN ###
        sample_mean = 0
        mean_dot = Dot(point=axes.c2p(0, 1, 0), color=RED)
        self.play(FadeIn(mean_dot))
        self.wait(0.5)

        # Draw horizontal line at sample mean
        mean_line = axes.get_vertical_line(axes.c2p(sample_mean, 5, 0), color=RED)
        mean_label = MathTex("\\hat{\\mu} = \\frac{1}{n}\\sum x^i", font_size=28, color=RED)
        mean_label.next_to(mean_line, RIGHT, buff=0.1)
        mean_label.to_corner(UP + LEFT, buff=3.0)

        self.play(Create(mean_line), Write(mean_label))
        self.wait(1)

        ### 7. HIGHLIGHT SAMPLE MEAN AS MSE MINIMIZER ###
        minimizer_text = Tex("MSE Minimizer: Sample Mean", color=RED, font_size=32)
        minimizer_text.next_to(mean_label, DOWN, buff=0.5)
        self.play(Write(minimizer_text))
        self.wait(1)

        ### 8. EXPLORE MSE'S UNIMODALITY ###
        # Display a bell curve centered at sample mean
        def gaussian_pdf(x):
            return stats.norm.pdf(x, loc=sample_mean, scale=sigma_true)
        bell_curve = axes.plot(
            gaussian_pdf
        )


        self.play(Create(bell_curve))
        self.wait(1)

        # Emphasize unimodal nature
        unimodal_text = Tex("Accurate for Datasets with a", font_size=25, color=GREEN)
        unimodal_text.next_to(minimizer_text, DOWN, buff=0.5)
        unimodal_text_2 = Tex("Unimodal Gaussian Distribution", font_size=25, color=GREEN)
        unimodal_text_2.next_to(unimodal_text, DOWN, buff=0.2)
        self.play(Write(unimodal_text), Write(unimodal_text_2))
        self.wait(10)

        