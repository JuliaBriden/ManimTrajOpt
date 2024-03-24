from manim import *
import numpy as np

class IntroScene(Scene):
    
    def construct(self):
        # Define the path function for the curved path
        def curved_path_func(alpha):
            return utils.paths.path_along_circles(-PI/4, divert_center[0])(start_point[0], end_point[0], alpha)

        spacecraft_color = BLUE

        # Create a spacecraft shape or use an image
        spacecraft = Triangle(color=spacecraft_color).scale(0.25)  # Example shape
        #spacecraft = ImageMobject("spacecraft.png").scale(0.25)  # If using an image

        # Position the spacecraft at the starting point
        start_point = 2.5 * UP + 5 * LEFT
        spacecraft.move_to(start_point)

        # Define the end point of the divert
        divert_end_point = Dot(3 * DOWN)  # Now a Mobject

        intro = Text("To accomplish precision landing in uncertain planetary entry, descent,\nand landing scenarios, safe and autonomous guidance trajectories must\nbe computed on the order of milliseconds.", t2c={"milliseconds":BLUE}).to_edge(UP).scale(0.4).shift(UP)
        self.add(intro)

        # Add the spacecraft to the scene
        self.add(spacecraft)
        self.add(TracedPath(spacecraft.get_center, stroke_color=spacecraft_color, dissipating_time=0.5, stroke_opacity=[0, 1]))

        # Define a point to represent the center of the divert maneuver
        divert_center = Dot(2 * LEFT + 1 * DOWN)

        self.wait()
        self.play(
            Transform(
                spacecraft,
                divert_end_point,
                path_func=utils.paths.path_along_circles(
                    -PI/4,  # This angle can be adjusted to change the arc of the divert
                    divert_center.get_center()
                ),
                run_time=3,
            )
        )

        # Create a VMobject for the path
        # Define start, end, and center points for the path
        start_point = np.array([2.5 * UP + 5 * LEFT])
        end_point = np.array([3 * DOWN])
        divert_center = np.array([2 * LEFT + 1 * DOWN])
        path = VMobject()
        path.set_points_smoothly([curved_path_func(alpha) for alpha in np.linspace(0, 1, 100)])
        path.set_color(spacecraft_color)
        path.set_stroke(width=2)  # Match stroke width with the trace
        #self.add(path)
        self.wait(4)
        self.play(FadeOut(spacecraft))

        traj_description = Text("Trajectory generation problems are formulated as optimal control\nproblems. Where mission objectives determine the cost function\nand equations of motion are formulated as constraints,\nin addition to constraints for state and control requirements.", t2c={"cost function": BLUE, "constraints":GREEN}).to_edge(UP).scale(0.4).shift(UP)
        self.play(Transform(intro, traj_description))

        # Define colors for cost function and constraints
        cost_color = BLUE
        constraint_color = GREEN

        equation = MathTex(r"\min_x J(x) \\", r"\text{ s.t. }", r"x \in C").to_edge(RIGHT).scale(1)
        # Applying colors to specific parts of the equation
        equation.set_color_by_tex("J(x)", cost_color)
        equation.set_color_by_tex("x \in C", constraint_color)
        self.add(equation)
        self.wait(5)

        semiinf_description = Text("For the spacecraft guidance problem, this equation becomes a semi-infinite optimization problem.", t2c={"semi-infinite optimization problem": BLUE}).to_edge(UP).scale(0.4)
        self.play(Transform(intro, semiinf_description))

        transformed_eq = MathTex(
            r"\min_{t_f, \mathbf{u}} L_f(t_0, t_f, \mathbf{x}(t_0), \mathbf{x}(t_f)) + \int_{t_0}^{t_f} L(\mathbf{x}(\tau), \mathbf{u}(\tau), \tau) d\tau \\",
            r"\text{s.t. } \dot{\mathbf{x}} = \mathbf{f} (\mathbf{x}(t), \mathbf{u}(t), t), \forall t \in [t_0, t_f] \\",
            r"\mathbf{g}(\mathbf{x}, \mathbf{u}, t) \leq 0, \forall t \in [t_0, t_f] \\",
            r"\mathbf{b}(\mathbf{x}(t_0), \mathbf{x}(t_f), t_f) = 0"
        ).scale(0.6).to_edge(RIGHT)
                
        # Annotations for each constraint
        annotations = VGroup(
            Text("Cost function", font_size=20, color=BLUE).next_to(transformed_eq[0], LEFT),
            Text("Equation of motion", font_size=20, color=GRAY).next_to(transformed_eq[1], LEFT),
            Text("Inequality constraints", font_size=20, color=GRAY).next_to(transformed_eq[2], LEFT),
            Text("Boundary conditions", font_size=20, color=GRAY).next_to(transformed_eq[3], LEFT)
        )

        # Playing the transformations
        self.play(Transform(equation, transformed_eq))
        self.play(FadeIn(annotations))
        self.wait(5)

        annotations2 = VGroup(
            Text("Cost function", font_size=20, color=GRAY).next_to(transformed_eq[0], LEFT),
            Text("Equation of motion", font_size=20, color=YELLOW).next_to(transformed_eq[1], LEFT),
            Text("Inequality constraints", font_size=20, color=GRAY).next_to(transformed_eq[2], LEFT),
            Text("Boundary conditions", font_size=20, color=GRAY).next_to(transformed_eq[3], LEFT)
        )

        self.play(Transform(annotations, annotations2))
        self.wait(3)

        annotations3 = VGroup(
            Text("Cost function", font_size=20, color=GRAY).next_to(transformed_eq[0], LEFT),
            Text("Equation of motion", font_size=20, color=GRAY).next_to(transformed_eq[1], LEFT),
            Text("Inequality constraints", font_size=20, color=RED).next_to(transformed_eq[2], LEFT),
            Text("Boundary conditions", font_size=20, color=GRAY).next_to(transformed_eq[3], LEFT)
        )

        self.play(Transform(annotations, annotations3))  
        self.wait(3)      

        annotations4 = VGroup(
            Text("Cost function", font_size=20, color=GRAY).next_to(transformed_eq[0], LEFT),
            Text("Equation of motion", font_size=20, color=GRAY).next_to(transformed_eq[1], LEFT),
            Text("Inequality constraints", font_size=20, color=GRAY).next_to(transformed_eq[2], LEFT),
            Text("Boundary conditions", font_size=20, color=ORANGE).next_to(transformed_eq[3], LEFT)
        )

        self.play(Transform(annotations, annotations4))  
        self.wait(3) 

        #dof_description = Text("Since the mass of fuel, or wet mass, often represents the majority of the vehicle’s mass,\n"
                               #"an objective of fuel-optimality is desirable. When modeled in 3 DoF, the vehicle is\n"
                               #"treated as a point mass.", t2c={"fuel-optimality": BLUE, "3 DOF": GREEN}).to_edge(UP).scale(0.4).shift(UP)
        #self.play(Transform(intro, dof_description))

        #dof3_eq = MathTex(
            #r"\min_{t_f, \mathbf{T}_c, \mathbf{r}, \mathbf{v}, m} \int_{0}^{t_f} ||\mathbf{T}_c||^2 dt\\",
            #r"\text{s.t. } \dot{\mathbf{r}}(t) = \mathbf{v}(t), \forall t \in [0, t_f]\\",
            #r"\dot{\mathbf{v}}(t) = \mathbf{g}(t) + \frac{\mathbf{T}_c(t) + \mathbf{D}(t) + \mathbf{L}(t)}{m(t)} - \boldsymbol{\omega} \times \boldsymbol{\omega} \times \mathbf{r}(t) - 2\boldsymbol{\omega} \times \mathbf{v}(t), \forall t \in [0, t_f]\\",
            #r"\dot{m}(t) = -\alpha||\mathbf{T}_c(t)||^2, \forall t \in [0, t_f]\\",
            #r"\rho_{\min} \leq ||\mathbf{T}_c(t)||^2 \leq \rho_{\max}, \forall t \in [0, t_f]\\",
            #r"\mathbf{T}_c(t)^T \hat{\mathbf{e}}_z \geq ||\mathbf{T}_c(t)||^2 \cos(\gamma_p), \forall t \in [0, t_f]\\",
            #r"\mathbf{H}_{gs}\mathbf{r}(t) \leq h_{gs}, \forall t \in [0, t_f]\\",
            #r"||\mathbf{v}(t)||^2 \leq v_{\max}, \forall t \in [0, t_f]\\",
            #r"m_{\text{dry}} \leq m(t_f)\\",
            #r"\mathbf{r}(0) = \mathbf{r}_0, \mathbf{v}(0) = \mathbf{v}_0, m(0) = m_{\text{wet}}\\",
            #r"\mathbf{r}(t_f) = \mathbf{r}_f, \mathbf{v}(t_f) = 0"
        #).scale(0.6).to_edge(RIGHT)

        self.play(FadeOut(annotations))
        
        # Annotations for dof3_eq
        #dof3_annotations = VGroup(
            #Text("Minimum thrust cost function", font_size=20, color=BLUE).next_to(dof3_eq[0], LEFT),
            #Text("Kinematic relationship", font_size=20, color=GRAY).next_to(dof3_eq[1], LEFT),
            #Text("Dynamic equation", font_size=20, color=GRAY).next_to(dof3_eq[2], LEFT),
            #Text("Fuel consumption", font_size=20, color=GRAY).next_to(dof3_eq[3], LEFT),
            #Text("Thrust limits", font_size=20, color=GRAY).next_to(dof3_eq[4], LEFT),
            #Text("Attitude constraint", font_size=20, color=GRAY).next_to(dof3_eq[5], LEFT),
            #Text("Glideslope constraint", font_size=20, color=GRAY).next_to(dof3_eq[6], LEFT),
            #Text("Velocity limit", font_size=20, color=GRAY).next_to(dof3_eq[7], LEFT),
            #Text("Dry mass constraint", font_size=20, color=GRAY).next_to(dof3_eq[8], LEFT),
            #Text("Initial conditions", font_size=20, color=GRAY).next_to(dof3_eq[9], LEFT),
            #Text("Final conditions", font_size=20, color=GRAY).next_to(dof3_eq[10], LEFT)
        #)

        # Playing the transformations
        #self.play(Transform(equation, dof3_eq))
        #self.play(FadeIn(dof3_annotations))
        #self.wait(7)

        #dof3_annotations2 = VGroup(
            #Text("Minimum thrust cost function", font_size=20, color=GRAY).next_to(dof3_eq[0], LEFT),
            #Text("Kinematic relationship", font_size=20, color=YELLOW).next_to(dof3_eq[1], LEFT),
            #Text("Dynamic equation", font_size=20, color=YELLOW).next_to(dof3_eq[2], LEFT),
            #Text("Fuel consumption", font_size=20, color=YELLOW).next_to(dof3_eq[3], LEFT),
            #Text("Thrust limits", font_size=20, color=GRAY).next_to(dof3_eq[4], LEFT),
            #Text("Attitude constraint", font_size=20, color=GRAY).next_to(dof3_eq[5], LEFT),
            #Text("Glideslope constraint", font_size=20, color=GRAY).next_to(dof3_eq[6], LEFT),
            #Text("Velocity limit", font_size=20, color=GRAY).next_to(dof3_eq[7], LEFT),
            #Text("Dry mass constraint", font_size=20, color=GRAY).next_to(dof3_eq[8], LEFT),
            #Text("Initial conditions", font_size=20, color=GRAY).next_to(dof3_eq[9], LEFT),
            #Text("Final conditions", font_size=20, color=GRAY).next_to(dof3_eq[10], LEFT)
        #)

        #self.play(Transform(dof3_annotations, dof3_annotations2))
        #self.wait(5)

        # Annotations for dof3_eq
        #dof3_annotations3 = VGroup(
            #Text("Minimum thrust cost function", font_size=20, color=GRAY).next_to(dof3_eq[0], LEFT),
            #Text("Kinematic relationship", font_size=20, color=GRAY).next_to(dof3_eq[1], LEFT),
            #Text("Dynamic equation", font_size=20, color=GRAY).next_to(dof3_eq[2], LEFT),
            #Text("Fuel consumption", font_size=20, color=GRAY).next_to(dof3_eq[3], LEFT),
            #Text("Thrust limits", font_size=20, color=RED).next_to(dof3_eq[4], LEFT),
            #Text("Attitude constraint", font_size=20, color=RED).next_to(dof3_eq[5], LEFT),
            #Text("Glideslope constraint", font_size=20, color=RED).next_to(dof3_eq[6], LEFT),
            #Text("Velocity limit", font_size=20, color=RED).next_to(dof3_eq[7], LEFT),
            #Text("Dry mass constraint", font_size=20, color=RED).next_to(dof3_eq[8], LEFT),
            #Text("Initial conditions", font_size=20, color=GRAY).next_to(dof3_eq[9], LEFT),
            #Text("Final conditions", font_size=20, color=GRAY).next_to(dof3_eq[10], LEFT)
        #)

        #self.play(Transform(dof3_annotations,dof3_annotations3))
        #self.wait(5)

        # Annotations for dof3_eq
        #dof3_annotations4 = VGroup(
            #Text("Minimum thrust cost function", font_size=20, color=GRAY).next_to(dof3_eq[0], LEFT),
            #Text("Kinematic relationship", font_size=20, color=GRAY).next_to(dof3_eq[1], LEFT),
            #Text("Dynamic equation", font_size=20, color=GRAY).next_to(dof3_eq[2], LEFT),
            #Text("Fuel consumption", font_size=20, color=GRAY).next_to(dof3_eq[3], LEFT),
            #Text("Thrust limits", font_size=20, color=GRAY).next_to(dof3_eq[4], LEFT),
            #Text("Attitude constraint", font_size=20, color=GRAY).next_to(dof3_eq[5], LEFT),
            #Text("Glideslope constraint", font_size=20, color=GRAY).next_to(dof3_eq[6], LEFT),
            #Text("Velocity limit", font_size=20, color=GRAY).next_to(dof3_eq[7], LEFT),
            #Text("Dry mass constraint", font_size=20, color=GRAY).next_to(dof3_eq[8], LEFT),
            #Text("Initial conditions", font_size=20, color=ORANGE).next_to(dof3_eq[9], LEFT),
            #Text("Final conditions", font_size=20, color=ORANGE).next_to(dof3_eq[10], LEFT)
        #)

        #self.play(Transform(dof3_annotations, dof3_annotations4))
        #self.wait(5)


        lcvx_description = Text("By mapping the non-convex formulation to a second-order cone program (SOCP), through\nthe process of lossless convexification, convergence to a globally-optimal solution is guaranteed.", t2c={"second-order cone program (SOCP)": BLUE, "lossless convexification": GREEN}).to_edge(UP).scale(0.4).shift(UP*.8)

        self.play(Transform(intro, lcvx_description))

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

        self.play(FadeOut(annotations))

        lcvs_annotations = VGroup(
                Text("Minimum slack variable cost function", font_size=20, color=BLUE).next_to(lcvs_eq[0], LEFT),
                Text("Kinematic relationship", font_size=20, color=GRAY).next_to(lcvs_eq[1], LEFT),
                Text("Dynamic equation", font_size=20, color=GRAY).next_to(lcvs_eq[2], LEFT),
                Text("Mass dynamics", font_size=20, color=GRAY).next_to(lcvs_eq[3], LEFT),
                Text("Lower bound of thrust-to-weight ratio", font_size=20, color=GRAY).next_to(lcvs_eq[4], LEFT),
                Text("Upper bound of thrust-to-weight ratio", font_size=20, color=GRAY).next_to(lcvs_eq[5], LEFT),
                Text("Control vector magnitude constraint", font_size=20, color=GRAY).next_to(lcvs_eq[6], LEFT),
                Text("Tilt angle constraint", font_size=20, color=GRAY).next_to(lcvs_eq[7], LEFT),
                Text("Glideslope constraint", font_size=20, color=GRAY).next_to(lcvs_eq[8], LEFT),
                Text("Velocity limit", font_size=20, color=GRAY).next_to(lcvs_eq[9], LEFT),
                Text("Dry mass constraint", font_size=20, color=GRAY).next_to(lcvs_eq[10], LEFT),
                Text("Fuel rate constraint", font_size=20, color=GRAY).next_to(lcvs_eq[11], LEFT),
                Text("Initial conditions", font_size=20, color=GRAY).next_to(lcvs_eq[12], LEFT),
                Text("Final conditions", font_size=20, color=GRAY).next_to(lcvs_eq[13], LEFT)
            )

        # Playing the transformations
        self.play(Transform(equation, lcvs_eq))
        self.play(FadeIn(lcvs_annotations))
        self.wait(7)

        lcvs_annotations2 = VGroup(
                Text("Minimum slack variable cost function", font_size=20, color=GRAY).next_to(lcvs_eq[0], LEFT),
                Text("Kinematic relationship", font_size=20, color=YELLOW).next_to(lcvs_eq[1], LEFT),
                Text("Dynamic equation", font_size=20, color=YELLOW).next_to(lcvs_eq[2], LEFT),
                Text("Mass dynamics", font_size=20, color=YELLOW).next_to(lcvs_eq[3], LEFT),
                Text("Lower bound of thrust-to-weight ratio", font_size=20, color=GRAY).next_to(lcvs_eq[4], LEFT),
                Text("Upper bound of thrust-to-weight ratio", font_size=20, color=GRAY).next_to(lcvs_eq[5], LEFT),
                Text("Control vector magnitude constraint", font_size=20, color=GRAY).next_to(lcvs_eq[6], LEFT),
                Text("Tilt angle constraint", font_size=20, color=GRAY).next_to(lcvs_eq[7], LEFT),
                Text("Glideslope constraint", font_size=20, color=GRAY).next_to(lcvs_eq[8], LEFT),
                Text("Velocity limit", font_size=20, color=GRAY).next_to(lcvs_eq[9], LEFT),
                Text("Dry mass constraint", font_size=20, color=GRAY).next_to(lcvs_eq[10], LEFT),
                Text("Fuel rate constraint", font_size=20, color=GRAY).next_to(lcvs_eq[11], LEFT),
                Text("Initial conditions", font_size=20, color=GRAY).next_to(lcvs_eq[12], LEFT),
                Text("Final conditions", font_size=20, color=GRAY).next_to(lcvs_eq[13], LEFT)
            )
        
        self.play(Transform(lcvs_annotations,lcvs_annotations2))
        self.wait(5)

        lcvs_annotations3 = VGroup(
                Text("Minimum slack variable cost function", font_size=20, color=GRAY).next_to(lcvs_eq[0], LEFT),
                Text("Kinematic relationship", font_size=20, color=GRAY).next_to(lcvs_eq[1], LEFT),
                Text("Dynamic equation", font_size=20, color=GRAY).next_to(lcvs_eq[2], LEFT),
                Text("Mass dynamics", font_size=20, color=GRAY).next_to(lcvs_eq[3], LEFT),
                Text("Lower bound of thrust-to-weight ratio", font_size=20, color=RED).next_to(lcvs_eq[4], LEFT),
                Text("Upper bound of thrust-to-weight ratio", font_size=20, color=RED).next_to(lcvs_eq[5], LEFT),
                Text("Control vector magnitude constraint", font_size=20, color=RED).next_to(lcvs_eq[6], LEFT),
                Text("Tilt angle constraint", font_size=20, color=RED).next_to(lcvs_eq[7], LEFT),
                Text("Glideslope constraint", font_size=20, color=RED).next_to(lcvs_eq[8], LEFT),
                Text("Velocity limit", font_size=20, color=RED).next_to(lcvs_eq[9], LEFT),
                Text("Dry mass constraint", font_size=20, color=RED).next_to(lcvs_eq[10], LEFT),
                Text("Fuel rate constraint", font_size=20, color=RED).next_to(lcvs_eq[11], LEFT),
                Text("Initial conditions", font_size=20, color=GRAY).next_to(lcvs_eq[12], LEFT),
                Text("Final conditions", font_size=20, color=GRAY).next_to(lcvs_eq[13], LEFT)
            )
        
        self.play(Transform(lcvs_annotations,lcvs_annotations3))
        self.wait(5)

        lcvs_annotations4 = VGroup(
                Text("Minimum slack variable cost function", font_size=20, color=GRAY).next_to(lcvs_eq[0], LEFT),
                Text("Kinematic relationship", font_size=20, color=GRAY).next_to(lcvs_eq[1], LEFT),
                Text("Dynamic equation", font_size=20, color=GRAY).next_to(lcvs_eq[2], LEFT),
                Text("Mass dynamics", font_size=20, color=GRAY).next_to(lcvs_eq[3], LEFT),
                Text("Lower bound of thrust-to-weight ratio", font_size=20, color=GRAY).next_to(lcvs_eq[4], LEFT),
                Text("Upper bound of thrust-to-weight ratio", font_size=20, color=GRAY).next_to(lcvs_eq[5], LEFT),
                Text("Control vector magnitude constraint", font_size=20, color=GRAY).next_to(lcvs_eq[6], LEFT),
                Text("Tilt angle constraint", font_size=20, color=GRAY).next_to(lcvs_eq[7], LEFT),
                Text("Glideslope constraint", font_size=20, color=GRAY).next_to(lcvs_eq[8], LEFT),
                Text("Velocity limit", font_size=20, color=GRAY).next_to(lcvs_eq[9], LEFT),
                Text("Dry mass constraint", font_size=20, color=GRAY).next_to(lcvs_eq[10], LEFT),
                Text("Fuel rate constraint", font_size=20, color=GRAY).next_to(lcvs_eq[11], LEFT),
                Text("Initial conditions", font_size=20, color=ORANGE).next_to(lcvs_eq[12], LEFT),
                Text("Final conditions", font_size=20, color=ORANGE).next_to(lcvs_eq[13], LEFT)
            )
        
        self.play(Transform(lcvs_annotations,lcvs_annotations4))
        self.wait(7)

        discretization_description = Text("The continuous-time problem is discretized to solve with an Interior-Point Method (IPM) or alternative solver.").to_edge(UP).scale(0.4).shift(UP*.4)
        self.play(Transform(intro, discretization_description))
        self.play(FadeOut(lcvs_annotations))

        self.add(path)

        # Calculate and create dots along the curved path
        num_dots = 20
        dots = VGroup()
        for i in range(num_dots):
            alpha = i / num_dots
            dot_position = curved_path_func(alpha)
            dot = Dot(dot_position, color=WHITE, radius=0.05)
            dots.add(dot)

        # Add dots and spacecraft to the scene
        self.add(dots)

        self.wait(5)






