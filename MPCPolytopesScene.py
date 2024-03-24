from manim import *

class MPCPolytopesScene(Scene):
    CONFIG = {
        "camera_config": {
            "frame_height": 5.625,
            "frame_width": 7.5,
        }
    }
        
    def construct(self):
        empc_description = Text(
            "To understand interpretability, consider Explicit MPC.\n"
            "The state space is divided into polytopes and each\n"
            "polytope corresponds to a control region with specific \n"
            "piecewise affine function coefficients.", t2c={"Explicit MPC": BLUE}
        ).to_edge(UP).scale(0.5).shift(UP)

        self.add(empc_description)
        self.wait(3)

        # Interesting Convex Polytopes
        polytopes = [
            Polygon([-4, -3, 0], [-2, -4, 0], [0, -3, 0], [-3, -1, 0], color=BLUE),
            Polygon([1, -3, 0], [2, -4, 0], [3, -2, 0], [2.5, -1, 0], [2, -0.5, 0], color=GREEN),
            Polygon([-4, 0, 0], [-3, 1, 0], [0, 1, 0], [3, 0, 0], [0.5, -1, 0], color=RED)
        ]
        polytope_labels = [
            MathTex(r"F_1x + g_1", font_size=30).move_to(polytopes[0].get_center()),
            MathTex(r"F_2x + g_2", font_size=30).move_to(polytopes[1].get_center()),
            MathTex(r"F_3x + g_3", font_size=30).move_to(polytopes[2].get_center())
        ]

        for polytope, label in zip(polytopes, polytope_labels):
            self.play(Create(polytope), Write(label))
        self.wait(2)

        # Transition to t-SNE
        self.play(FadeOut(empc_description))

        # t-SNE Explanation
        tsne_description = Text(
            "Similarly, t-Distributed Stochastic Neighbor Embedding (t-SNE)\n"
            "projects clusters in Transformer NN embeddings down to two\n"
            "dimensions based on similarity.", t2c={"t-Distributed Stochastic Neighbor Embedding (t-SNE)": BLUE}
        ).to_edge(UP).scale(0.5).shift(UP)

        self.add(tsne_description)
        self.wait(3)

        three_d_axes = ThreeDAxes().shift(DOWN)
        three_d_axes.rotate_about_origin(np.pi/6, axis=RIGHT) # Adjust the angle as needed
        three_d_axes.rotate_about_origin(np.pi/4, axis=UP)    # Adjust the angle as needed

        self.add(three_d_axes)
        self.wait(1)

        blue_dots = VGroup(*[Dot(color=BLUE).move_to(np.random.uniform(-2.5, 2.5) * RIGHT + np.random.uniform(-2.5, 2.5) * UP) for _ in range(10)])
        green_dots = VGroup(*[Dot(color=GREEN).move_to(np.random.uniform(-2.5, 2.5) * RIGHT + np.random.uniform(-2.5, 2.5) * UP) for _ in range(10)])
        red_dots = VGroup(*[Dot(color=RED).move_to(np.random.uniform(-2.5, 2.5) * RIGHT + np.random.uniform(-2.5, 2.5) * UP) for _ in range(10)])
        nn_space_points = VGroup(blue_dots, green_dots, red_dots)
        self.play(Create(nn_space_points))
        self.wait(1)

        tsne_colors = [BLUE, GREEN, RED]
        two_d_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_tip": False}
        ).shift(DOWN)
        # Start transformation animation
        self.play(Transform(three_d_axes, two_d_axes))

        tsne_labels = [
            MathTex(r"C_1", font_size=30).move_to(polytopes[0].get_center()),
            MathTex(r"C_2", font_size=30).move_to(polytopes[1].get_center()),
            MathTex(r"C_3", font_size=30).move_to(polytopes[2].get_center())
        ]

        for polytope, color, color_dots in zip(polytopes, tsne_colors, [blue_dots, green_dots, red_dots]):
            # Get the center of the polytope
            polytope_center = polytope.get_center()

            # Corresponding t-SNE cluster around the polytope center
            tsne_cluster = VGroup(*[Dot(color=color).move_to(polytope_center + 0.6 * RIGHT*np.random.normal() + 0.6 * UP*np.random.normal()) for _ in range(10)])
            self.play(Transform(color_dots, tsne_cluster))
            self.play(FadeOut(polytope))
            self.play(Transform(polytope_labels[tsne_colors.index(color)], tsne_labels[tsne_colors.index(color)]))
            self.wait(1)

# To render this scene, use the following command in your terminal:
# manim -pql script_name.py MPCPolytopesScene
