from manim import *
import numpy as np

# Manim Scene
class OptimizationScene(Scene):

    def construct(self):
        title = Text("Improving Computational Efficiency", color=WHITE).scale(0.75).to_edge(UP)

        # Displaying the optimization problem
        optimization_problem = MathTex(
            r"\text{Minimize: } & c^T x \\",
            r"\text{Subject to: } & Ax = b \\",
            r"& x \in \mathcal{K}"
        ).next_to(title, DOWN)

        # Displaying primal and dual formulations
        primal_dual_formulation = MathTex(
            r"\text{Primal: } & \begin{cases} \text{Minimize: } c^T x \\ Ax = b \\ x \in \mathcal{K} \end{cases}", 
            r"\text{Dual: } & \begin{cases} \text{Maximize: } b^T y \\ A^T y + s = c \\ s \in \mathcal{K}^* \end{cases}"
        ).next_to(optimization_problem, DOWN)

        # Apply different colors
        primal_dual_formulation.set_color_by_tex("Primal", BLUE)
        primal_dual_formulation.set_color_by_tex("Dual", RED)

        IPM_description = Text(
            "When solving the direct formulation of the spacecraft powered descent guidance problem,\n"
            "Primal-Dual Interior Point Methods (IPMs), such as ECOS, solve Second Order Cone Programs\n"
            "(SOCPs) by iteratively navigating through the interior of the feasible region, eventually\n"
            "converging to the boundary where the active constraints are located.", t2c={"Primal-Dual Interior Point Methods (IPMs)": BLUE}
        ).scale(0.5).to_edge(DOWN)

        # Axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": WHITE},
        ).to_edge(LEFT)

        # Labels for axes
        x_label = axes.get_x_axis_label("x_1")
        y_label = axes.get_y_axis_label("x_2")

        # Constraints as lines
        def SOC_constraint(x):
            return x**2 - 4
        
        def constraint_1(x):
            return -2 - x/2
        
        def constraint_2(x):
            return 4 - 2*x
        
        def constraint_3(x):
            return 5
        
        constraints = [
            axes.plot(SOC_constraint, color=RED),
            axes.plot(constraint_1, color=BLUE),
            axes.plot(constraint_2, color=YELLOW),
            axes.plot(constraint_3, color=GREEN)

        ]



        # Constraint labels
        constraint_labels = [
            Text("").next_to(constraints[0],  UP).scale(0.5),
            Text("").next_to(constraints[1], RIGHT).scale(0.5),
            Text("").next_to(constraints[2], RIGHT).scale(0.5),
            Text("").next_to(constraints[3], RIGHT).scale(0.5)
        ]

        # Optimal point
        optimal_point = Dot(axes.c2p(1.186, -2.593), color=GOLD)
        optimal_label = Text("Optimal Point", color=GOLD).next_to(optimal_point, LEFT).scale(0.4)

        # Group everything related to the graph
        graph_group = VGroup(axes, x_label, y_label, *constraints, *constraint_labels, optimal_point, optimal_label)

                # Feasible region
        feasible_region = Polygon(
            axes.c2p(-3, 5),  # Point 1 (modify as needed)
            axes.c2p(-1.686, -1.157),   # Point 2 (modify as needed)
            axes.c2p(1.186, -2.593),    # Point 3 (modify as needed)
            axes.c2p(2, 0),   # Point 4 (modify as needed)
            axes.c2p(-.5, 5),   # Point 5 (modify as needed)
            color=GREY,
            fill_opacity=0.3
        )

        # Animation
        self.add(title)
        self.wait(1)
        self.add(optimization_problem)
        self.wait(3)
        self.add(primal_dual_formulation)
        self.wait(3)
        self.add(IPM_description)
        self.wait(7)
        self.play(FadeOut(optimization_problem), FadeOut(primal_dual_formulation), FadeOut(IPM_description), FadeOut(title))
        # Gradient for cost function min x_2
        gradient_start = -5  # Start value of x_2
        gradient_end = 7     # End value of x_2
        num_rects = 100       # Number of rectangles to use for the gradient
        for i in range(num_rects):
            x2_val = gradient_start + (gradient_end - gradient_start) * i / num_rects
            color_val = interpolate_color(BLUE, ORANGE, i / num_rects)  # Gradation from RED to GREEN
            rect = Rectangle(
                width=6, height=(gradient_end - gradient_start) / num_rects,
                fill_color=color_val, fill_opacity=0.1, stroke_width=0
            )
            rect.move_to(axes.c2p(0, x2_val))
            self.add(rect)
        self.play(Create(axes), Write(x_label), Write(y_label))
        for constraint, label in zip(constraints, constraint_labels):
            self.play(Create(constraint), Write(label))
        
        feasible_lable = Text("Feasible Region", color=GREY).next_to(feasible_region, UP).scale(0.5)
        self.play(Write(feasible_region), Write(feasible_lable))
        self.wait(1)

        explanation = MathTex(
            r"\text{By formulating primal and dual barrier functions, the following} \\\\", r"\text{system of equations yields the Central Path of the IPM:} \\\\",
            r"\mu > 0 \text{ (barrier parameter)} \\\\",
            r"A \mathbf{x} = \mathbf{b} \text{ (primal feasibility)} \\\\",
            r"A^T \mathbf{y} + \mathbf{s} = \mathbf{c} \text{ (dual feasibility)} \\\\",
            r"x_j s_j = \mu \text{ for all } j=1,2,...,n \text{ (complementary slackness)} \\\\",
            r"x_{0i} - || \mathbf{x}_{(i)} ||_2 \geq 0 \text{ for all } i \text{ (interior of cone)}",
        ).to_edge(RIGHT).scale(0.5)
        explanation.shift(RIGHT*3.5)  # Adjust the value as needed
        explanation.shift(UP)  # Adjust the value as needed
        self.add(explanation)
        self.wait(5)
        explanation_1 = Text("The size of this system of equations\ndepends on the number of constraints.", color=RED).next_to(explanation, DOWN).scale(0.4)
        self.add(explanation_1)
        self.wait(4)

        # Solver's path
        path = VMobject(color=BLUE_B)
        path_start = axes.coords_to_point(0, 0)  # Starting point
        path_mid = axes.coords_to_point(1.25, 0)  # Midpoint
        path_end = axes.coords_to_point(1.186, -2.593)  # Ending point
        path.set_points_as_corners([path_start, path_mid, path_end])
        path_label = Text("Central Path", color=BLUE_B).next_to(path, RIGHT).scale(0.5)
        
        # Create dots for mu values
        dot_mu_greater_1 = Dot(path_start, color=YELLOW)
        dot_mu_0_to_1 = Dot(path_mid, color=ORANGE)
        dot_mu_0 = Dot(path_end, color=RED)
        
        # Labels for mu values
        label_mu_greater_1 = MathTex(r"\mu > 1", color=YELLOW).next_to(dot_mu_greater_1, UP+LEFT).scale(0.5)
        label_mu_0_to_1 = MathTex(r"0 \leq \mu \leq 1", color=ORANGE).next_to(dot_mu_0_to_1, UP).scale(0.5)
        label_mu_0 = MathTex(r"\mu = 0", color=RED).next_to(dot_mu_0, RIGHT).scale(0.5)
        
        # Add path and labels to scene
        self.play(Create(path), Write(path_label), run_time=4)
        self.add(dot_mu_greater_1, label_mu_greater_1)
        self.add(dot_mu_0_to_1, label_mu_0_to_1)
        self.add(dot_mu_0, label_mu_0)
        self.wait(1)

        self.play(Create(optimal_point), Write(optimal_label))

        # Focusing on tight constraints
        self.play(FadeOut(constraints[2]), FadeOut(constraint_labels[2]), FadeOut(constraints[3]), FadeOut(constraint_labels[3]), FadeOut(explanation_1), FadeOut(dot_mu_0_to_1), FadeOut(label_mu_0_to_1))
        self.wait(1)

        explanation_text_2 = Text(
            "If the set of tight constraints can be identified,\nthe size of the system of equations\ncan be significantly reduced and the IPM can\ntake a more direct path to the optimal solution.", t2c={"tight constraints": BLUE}
            ).to_edge(RIGHT).scale(0.4).shift(RIGHT*3.6)

        self.play(Transform(explanation, explanation_text_2))

        # New path of the solver
        new_path = VMobject(color=BLUE_B)
        new_path.set_points_as_corners([axes.coords_to_point(0, 0), axes.coords_to_point(1.186, -2.593)])
        self.play(Transform(path, new_path), run_time=4)


        self.wait(7)