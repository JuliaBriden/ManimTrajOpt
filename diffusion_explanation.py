from manim import *
import numpy as np
import random
from scipy.stats import gaussian_kde  # for kernel density estimation

class Motivation(Scene):
    def construct(self):
        #################################################################
        # 1. Color-coded Forward Diffusion Equation at the Top
        #################################################################
        eq_colored = MathTex(
            r"\mathbf{x}_t = ",
            r"\sqrt{1-\beta}\,\mathbf{x}_{t-1}",
            r" + ",
            r"\sqrt{\beta}\,\boldsymbol{\epsilon},",
            r"\quad \boldsymbol{\epsilon}\,\sim \mathcal{N}(0,\mathbf{I})"
        ).scale(0.7).to_edge(UP)

        # Color the scale term (green) and the noise term (red).
        eq_colored[1].set_color(GREEN)
        eq_colored[3].set_color(RED)
        self.add(eq_colored)
        self.wait(1)

        #################################################################
        # 2. Original Trajectory Setup
        #################################################################
        def curved_path_func(alpha):
            """
            Parametric curve.
            """
            return utils.paths.path_along_circles(-PI/4, divert_center[0])(
                start_point[0], end_point[0], alpha
            )

        def discretize(num_dots):
            dots_vg = VGroup()
            for i in range(num_dots):
                alpha = i / num_dots
                dot_position = curved_path_func(alpha)
                dot = Dot(dot_position, color=WHITE, radius=0.05)
                dots_vg.add(dot)
            return dots_vg

        # Path parameters
        start_point   = np.array([2.25 * UP + 1 * LEFT])
        end_point     = np.array([2     * UP + 2 * RIGHT])
        divert_center = np.array([2     * RIGHT])

        n = 400
        end_point     = np.array([2 * RIGHT + 2 * UP + 0.01 * n * (RIGHT + DOWN)])
        divert_center = np.array([2 * RIGHT + 0.01 * n * (RIGHT + DOWN)])
        num_dots = 30

        dots_vg = discretize(num_dots)
        self.add(dots_vg)

        # Connect them with a line
        line = VMobject(color=YELLOW, stroke_width=3)
        line.set_points_as_corners([dot.get_center() for dot in dots_vg])
        self.add(line)
        self.wait(2)

        #################################################################
        # 3. Show an Initial Distribution (Histogram + KDE)
        #################################################################
        positions_pre = [dot.get_center() for dot in dots_vg]
        initial_x = np.array([p[0] for p in positions_pre])  # x-coords

        hist_axes_init = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 10, 2],
            x_length=5,
            y_length=3,
            tips=False,
        ).to_edge(LEFT, buff=1.0)
        # Label for the desired distribution
        hist_label_init = MathTex(r"q(x_0)", font_size=24)
        hist_label_description = Text("Desired Trajectory Distribution", font_size=20).next_to(hist_label_init, UP)

        # Arrange the label and description vertically
        hist_label = VGroup(hist_label_description, hist_label_init).next_to(hist_axes_init, UP, buff=0.2)
        self.play(FadeIn(hist_axes_init), FadeIn(hist_label))

        bin_count = 10
        hist_vals_init, bin_edges_init = np.histogram(initial_x, bins=bin_count, range=(-4,4))

        bar_chart_init = BarChart(
            values=hist_vals_init,
            bar_names=[f"{(bin_edges_init[i]+bin_edges_init[i+1]) / 2:.1f}" for i in range(bin_count)],
            y_range=[0, max(hist_vals_init)+1, 1],
            y_length=3,
            x_length=5,
            bar_colors=[BLUE],
        )
        bar_chart_init.move_to(hist_axes_init.c2p(0,4.5))

        self.play(Create(bar_chart_init))
        self.wait(2)

        # Kernel Density Estimation
        kde_init = gaussian_kde(initial_x)
        def kde_init_pdf(x):
            return kde_init.evaluate(x)[0]

        pdf_graph_init = hist_axes_init.plot(
            lambda x: len(initial_x) * kde_init_pdf([x]),
            x_range=[-4, 4],
            color=RED
        )
        self.play(Create(pdf_graph_init))
        self.wait(2)

        text_mm = Text(
            "Goal: learn to generate trajectories from the Multi-Modal Distribution",
            font_size=20, color=BLUE
        )
        text_mm.next_to(hist_axes_init, DOWN, buff=1.5).shift(RIGHT * 2)

        self.play(Write(text_mm))
        self.wait(2)


        # Fade out the initial histogram
        self.play(
            FadeOut(bar_chart_init), FadeOut(hist_label_init),
            FadeOut(hist_axes_init),
            FadeOut(pdf_graph_init), FadeOut(text_mm), FadeOut(hist_label), FadeOut(hist_label_description)
        )
        self.wait(0.5)

        #################################################################
        # 4. Forward Diffusion Setup
        #################################################################
        T = 1000
        beta = 0.03
        animate_steps = {1, 2, 3, 10, 50, 100, 500, 1000}  # only animate these
        scale_factor = np.sqrt(1 - beta)
        noise_factor = np.sqrt(beta)
        positions = np.array([dot.get_center() for dot in dots_vg])

        # Convert Dot positions to array
        self.forward_trajectories = []
        self.forward_trajectories.append(positions.copy())  # store x_0

        #################################################################
        # 5. Forward Diffusion Loop
        #    Animate some steps, storing each state
        #################################################################
        info_box = VGroup().to_edge(RIGHT, buff=1.0)
        self.add(info_box)

        rep_dot_index = 0
        for t in range(1, T+1):
            old_positions = positions.copy()

            # Scale step
            scaled_positions = old_positions.copy()
            scaled_positions[:, 0:2] *= scale_factor

            # Then noise step => final
            eps = np.random.normal(0.0, 1.0, size=(num_dots, 2))
            final_positions = scaled_positions.copy()
            final_positions[:, 0:2] += noise_factor * eps

            # Update 'positions'
            positions = final_positions
            self.forward_trajectories.append(positions.copy())  # store x_t

            if t in animate_steps:
                # Info Box
                step_text = Text(f"Forward Step: t={t}", font_size=24)
                info_box_new = VGroup(step_text).arrange(UP, aligned_edge=RIGHT)
                info_box_new.to_corner(UP + RIGHT, buff=1.0)

                self.remove(info_box)
                self.add(info_box_new)
                info_box = info_box_new

                old_rep = old_positions[rep_dot_index]
                scaled_rep = scaled_positions[rep_dot_index]

                arrow_noise = Arrow(
                    start=scaled_rep,
                    end=final_positions[rep_dot_index]*1.2,
                    buff=0,
                    stroke_width=3,
                    color=RED
                )
                self.add(arrow_noise)
                arrow_scale_label = Text(
                    f"Scale Δ=({(scaled_rep[0]-old_rep[0]):.2f}, {(scaled_rep[1]-old_rep[1]):.2f})",
                    font_size=20, color=GREEN
                ).next_to(info_box_new, DOWN)
                self.add(arrow_scale_label)

                anims_scale = []
                for i, dot in enumerate(dots_vg):
                    anims_scale.append(dot.animate(run_time=1.0).move_to(scaled_positions[i]))

                scaled_line = line.copy()
                scaled_line.set_points_as_corners(scaled_positions)
                self.play(*anims_scale, line.animate().become(scaled_line), run_time=1.0)

                arrow_noise_label = Text(
                    f"Noise Δ=({(final_positions[rep_dot_index,0]-scaled_rep[0]):.2f}, "
                    f"{(final_positions[rep_dot_index,1]-scaled_rep[1]):.2f})",
                    font_size=20, color=RED
                ).next_to(arrow_scale_label, DOWN)
                self.add(arrow_noise_label)

                anims_noise = []
                for i, dot in enumerate(dots_vg):
                    anims_noise.append(dot.animate(run_time=1.0).move_to(final_positions[i]))

                final_line = line.copy()
                final_line.set_points_as_corners(final_positions)
                self.play(*anims_noise, line.animate().become(final_line), run_time=1.0)

                self.wait(0.2)
                self.remove(arrow_scale_label, arrow_noise, arrow_noise_label)

        self.remove(line, eq_colored)

        #################################################################
        # 6. Show 1D Histogram of final x + Normal PDF
        #################################################################
        final_x = positions[:, 0]
        hist_axes_final = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 10, 2],
            x_length=5,
            y_length=3,
            tips=False,
        ).to_edge(LEFT, buff=1.0)

        final_label = MathTex(r"p(x_T)", font_size=24)
        hist_label_description = Text("Final Distribution", font_size=20)
        hist_label_final = VGroup(hist_label_description, final_label).arrange(DOWN, buff=0.3)
        hist_label_final.next_to(hist_axes_final, UP)

        self.play(FadeIn(hist_axes_final), FadeIn(hist_label_final))

        hist_vals_final, bin_edges_final = np.histogram(final_x, bins=10, range=(-3,3))
        bar_chart_final = BarChart(
            values=hist_vals_final,
            bar_names=[f"{(bin_edges_final[i]+bin_edges_final[i+1]) / 2:.1f}" for i in range(10)],
            y_range=[0, max(hist_vals_final)+1, 1],
            y_length=3,
            x_length=5,
            bar_colors=[BLUE],
        )
        bar_chart_final.move_to(hist_axes_final.c2p(0,4.5))
        self.play(Create(bar_chart_final))
        self.wait(1)

        sample_mean = float(np.mean(final_x))
        sample_std  = float(np.std(final_x)) + 1e-8

        def normal_pdf(x):
            return (1.0/(sample_std*np.sqrt(2*np.pi))) * np.exp(-0.5*((x-sample_mean)/sample_std)**2)

        pdf_graph = hist_axes_final.plot(
            lambda x: len(final_x)*normal_pdf(x),
            color=GREEN,
            x_range=[-3,3],
        )

        self.play(Create(pdf_graph))
        self.wait(2)

        concluding = Text(
            "As t→∞, samples converge to N(0,I).",
            font_size=26, color=YELLOW
        ).next_to(pdf_graph, DOWN, buff=1.0)
        self.play(Write(concluding))
        self.wait(3)
        self.remove(pdf_graph, bar_chart_final, hist_label_final, hist_axes_final, step_text)

        ############  <<<<  CONTINUATION: BACKWARD PROCESS  >>>>  ############
        ######################################################################
        # 7. Reverse Process: p(x_{t-1} | x_t). We'll just replay stored states
        ######################################################################
        eq_reverse = MathTex(
        r"x_{t-1} = \mu_\theta(\mathbf{x}_t, t) + \tilde{\beta}_t \boldsymbol{\epsilon},"
        r"\quad \text{where } \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})",
        font_size=32
    ).to_edge(UP).set_color(BLUE)


        self.play(FadeOut(concluding), FadeIn(eq_reverse))
        self.wait(1)

        reverse_title = Text(
            "The reverse process recovers the original distribution from a standard normal sample",
            font_size=24, color=BLUE
        ).to_edge(DOWN)

        self.play(Write(reverse_title))
        self.wait(1)

        # We'll define a new line for the backward animation
        line_rev = VMobject(color=YELLOW, stroke_width=3)
        line_rev.set_points_as_corners(self.forward_trajectories[-1])  # x_T
        self.add(line_rev)

        # Move all dots to x_T if not already
        # (they should already be at final_positions, but just to be safe)
        for i, dot in enumerate(dots_vg):
            dot.move_to(self.forward_trajectories[-1][i])

        self.wait(0.5)

        # Replay from t=T down to t=0
        # self.forward_trajectories[t] is the array for step t
        # We'll do a small annotation for each step
        for t_rev in range(T, 0, -1):
            old_pos = self.forward_trajectories[t_rev]
            new_pos = self.forward_trajectories[t_rev - 1]

            if t_rev in animate_steps:

                # Animate
                anims = []
                for i, dot in enumerate(dots_vg):
                    anims.append(dot.animate(run_time=1.0).move_to(new_pos[i]))

                updated_line = line_rev.copy()
                updated_line.set_points_as_corners(new_pos)
                self.play(*anims, line_rev.animate().become(updated_line), run_time=1.0)

                step_lbl = Text(f"Backward Step: t={t_rev-1}", font_size=20, color=BLUE)
                info_box_new = VGroup(step_lbl).arrange(UP, aligned_edge=RIGHT)
                info_box_new.to_corner(UP + RIGHT, buff=1.0)

                self.remove(info_box)
                self.add(info_box_new)
                info_box = info_box_new
                self.wait(0.4)

        self.wait(10)
        self.remove(reverse_title)


