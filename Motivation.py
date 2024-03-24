from manim import *

class Motivation(Scene):
    def construct(self):
        # Define the path function for the curved path
        def curved_path_func(alpha):
            return utils.paths.path_along_circles(-PI/4, divert_center[0])(start_point[0], end_point[0], alpha)
        def discretize(num_dots):
            # Calculate and create dots along the curved path
            dots = VGroup()
            for i in range(num_dots):
                alpha = i / num_dots
                dot_position = curved_path_func(alpha)
                dot = Dot(dot_position, color=WHITE, radius=0.05)
                dots.add(dot)
            return dots
        def calculate_num_dots(n):
            """
            Calculate the number of dots to be used for a given value of n.
            This function returns fewer dots as n increases.
            """
            if n <= 10:
                return n  # Use n dots for small values of n
            else:
                return max(10, 1000 // n)  # Decrease number of dots for large n
        
        # Define start, end, and center points for the path
        start_point = np.array([3 * UP + 1.75*RIGHT])
        end_point = np.array([2 * UP + 2 * RIGHT])
        divert_center = np.array([2 * RIGHT])
        path = VMobject()
        path.set_points_smoothly([curved_path_func(alpha) for alpha in np.linspace(0, 1, 100)])
        path.set_color(BLUE)
        path.set_stroke(width=2)  # Match stroke width with the trace

        lcvs_eq = MathTex(
            r"\min_{\xi, \mathbf{u}, t_f} \int_{0}^{t_f} \xi(t) dt\\",
            r"\text{s.t. } \dot{\mathbf{r}}(t) = \mathbf{v}(t)\\",
            r"\dot{\mathbf{v}}(t) = \mathbf{g} + \mathbf{u}(t) - \boldsymbol{\omega} \times \boldsymbol{\omega} \times \mathbf{r}(t) - 2\boldsymbol{\omega} \times \mathbf{v}(t)\\",
            r"\dot{z}(t) = -\alpha \xi (t)\\",
            r"\mu_{\min}(t) [1 - \delta z(t) + \frac{1}{2} \delta z(t)^2] \leq \xi (t)\\",
            r"\mu_{\max}(t) [1 - \delta z(t)] \geq \xi (t)\\",
            r"||\mathbf{u}(t)||^2 \leq \xi (t)\\",
            r"\mathbf{u}(t)^T \hat{\mathbf{e}}_z \geq \xi \cos(\gamma_p)\\",
            r"\mathbf{H}_{gs}\mathbf{r}(t) \leq h_{gs}\\",
            r"||\mathbf{v}(t)||^2 \leq v_{\max}\\",
            r"\ln(m_{\text{dry}}) \leq z(t_f)\\",
            r"z_0(t) \leq z(t) \leq \ln(m_{\text{wet}} - \alpha \rho_{\min} t)\\",
            r"\mathbf{r}(0) = \mathbf{r}_0, \mathbf{v}(0) = \mathbf{v}_0, z(0) = \ln(m_{\text{wet}})\\",
            r"\mathbf{r}(t_f) = \mathbf{v}(t_f) = 0"
        ).scale(0.6).to_edge(RIGHT)

        lcvs_annotations = VGroup(
                Text("15N + 9 total constraints", font_size=20, color=BLUE).next_to(lcvs_eq[0], LEFT),
                Text("3N", font_size=20, color=YELLOW).next_to(lcvs_eq[1], LEFT),
                Text("3N", font_size=20, color=YELLOW).next_to(lcvs_eq[2], LEFT),
                Text("N", font_size=20, color=YELLOW).next_to(lcvs_eq[3], LEFT),
                Text("N-1", font_size=20, color=RED).next_to(lcvs_eq[4], LEFT),
                Text("N-1", font_size=20, color=RED).next_to(lcvs_eq[5], LEFT),
                Text("N-1", font_size=20, color=RED).next_to(lcvs_eq[6], LEFT),
                Text("N-1", font_size=20, color=RED).next_to(lcvs_eq[7], LEFT),
                Text("N", font_size=20, color=RED).next_to(lcvs_eq[8], LEFT),
                Text("N", font_size=20, color=RED).next_to(lcvs_eq[9], LEFT),
                Text("N", font_size=20, color=RED).next_to(lcvs_eq[10], LEFT),
                Text("N", font_size=20, color=RED).next_to(lcvs_eq[11], LEFT),
                Text("7", font_size=20, color=ORANGE).next_to(lcvs_eq[12], LEFT),
                Text("6", font_size=20, color=ORANGE).next_to(lcvs_eq[13], LEFT)
            )

        # Playing the transformations
        self.add(lcvs_eq)
        self.play(FadeIn(lcvs_annotations))

        self.wait(6)
        
        self.play(FadeOut(lcvs_annotations), FadeOut(lcvs_eq))

        traj_label = Text("Discretized trajectory").next_to(start_point, UP + RIGHT).scale(0.5)

        # Add dots and spacecraft to the scene
        dots = discretize(1)
        self.add(path, traj_label, dots)

        # Define the Axes for the Graph
        axes = Axes(
            x_range=[0, 500, 50],  # N values from 10 to 100
            y_range=[0, 7500, 500],  # Constraint range, considering the maximum for the original problem
            x_length=7,
            y_length=5,
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": np.arange(0, 500, 50)},
            y_axis_config={"numbers_to_include": np.arange(0, 7500, 500)}
        ).to_edge(LEFT)

        labels = axes.get_axis_labels(
            x_label=Tex("N (Number of Discretization Nodes)").scale(0.4), y_label=Tex("Number of Constraints").scale(0.4)
        )
        axes.add(labels)

        # Functions for Constraints
        original_constraints = axes.plot(lambda x: 15*x + 9, color=RED, x_range=[0, 500])
        optimal_constraints = axes.plot(lambda x: 7*x + 13, color=GREEN, x_range=[0, 500])

        # Labels for the Curves
        original_label = axes.get_graph_label(original_constraints, label="15N + 9", x_val=50, direction=UP).shift(UP).scale(0.5)
        optimal_label = axes.get_graph_label(optimal_constraints, label="7N + 13", x_val=50, direction=DOWN).scale(0.5).shift(UP+RIGHT)

        # Creating a Group of All Graph Elements
        graph = VGroup(axes, original_constraints, optimal_constraints, original_label, optimal_label)

        self.play(Create(graph))


        a = ValueTracker(10)
        moving_dot = Dot(color=ORANGE)

        constraints_label = Variable(0, "Constraints ", num_decimal_places=0).next_to(moving_dot, UP + LEFT).shift(UP).scale(0.5)
        N_label = Variable(0, "N ", num_decimal_places=0).next_to(constraints_label, UP).scale(0.5)


        constraints_label.add_updater(lambda v: v.tracker.set_value(15 * a.get_value() + 9))
        N_label.add_updater(lambda v: v.tracker.set_value(a.get_value()))

        self.add(constraints_label, N_label)
        for n in [5, 10, 15, 20, 30, 50, 100, 200, 500]:
            original_constraints_val = 15 * n + 9

            end_point = np.array([2 * RIGHT + 2 * UP + 0.01 * n *( RIGHT + DOWN)])
            divert_center = np.array([2 * RIGHT + 0.01 * n * (RIGHT + DOWN)])
    
            new_path = VMobject()
            new_path.set_points_smoothly([curved_path_func(alpha) for alpha in np.linspace(0, 1, 100)])
            new_path.set_color(BLUE)
            new_path.set_stroke(width=2)  # Match stroke width with the trace

            # Add dots and spacecraft to the scene
            new_dots = discretize(calculate_num_dots(n))

            self.play(
                moving_dot.animate.move_to(axes.c2p(n, original_constraints_val)),
                run_time=.25
            )
            self.play(a.animate.set_value(n), Transform(path,new_path), Transform(dots, new_dots))
            self.wait(.25)

        # Create a Moving Dot and Label
        label = MathTex("", color=ORANGE).next_to(moving_dot, UP + RIGHT)


        self.wait(5)

