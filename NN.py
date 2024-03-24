from manim import *
import numpy as np
from PIL import Image
from manim_ml.neural_network import NeuralNetwork, FeedForwardLayer, Convolutional2DLayer, ImageLayer

# Make nn
class NN(ThreeDScene):
    CONFIG = {
        "camera_config": {
            "frame_height": 5.625,
            "frame_width": 7.5,
            "disable_caching": True,
        }
    }

    def construct(self):
        def make_forward_pass_until_encoder(self, stop_at_layer_index, **kwargs):
            animations = []
            for i, layer in enumerate(self.input_layers):
                # Create animation for each layer
                layer_animation = layer.make_forward_pass_animation(**kwargs)
                animations.append(layer_animation)
                
                # Stop if we've reached the specified layer
                if i == stop_at_layer_index:
                    # Highlight the final layer and keep it highlighted
                    keep_highlighted = ApplyMethod(
                        layer.node_group.set_color, self.animation_dot_color, run_time=0.25
                    )
                    animations.append(keep_highlighted)
                    break

            return AnimationGroup(*animations, lag_ratio=0.2)
        
        # eMPC Explanation
        title = Text("Interpretability and Generalizability", color=WHITE).scale(0.5).to_edge(UP)
        self.add(title)
        self.wait(1)

        image = Image.open("multipleInputs.png") 
        numpy_image = np.asarray(image)

        nn = NeuralNetwork([
            ImageLayer(numpy_image, height=2.5),
            FeedForwardLayer(num_nodes=2),        # Input layer (equivalent to encoder input)
            FeedForwardLayer(num_nodes=5),      # Encoder output dimension
            FeedForwardLayer(num_nodes=15),     # TransformerEncoderLayer's internal dimension
            FeedForwardLayer(num_nodes=5),      # Dimension after TransformerEncoderLayer
            FeedForwardLayer(num_nodes=5)       # Output layer (equivalent to decoder output)
        ], layer_spacing=1)

        # Center the nn
        nn.move_to(ORIGIN)
        self.add(nn)

        encoder_label = Tex("Encoder").scale(0.5)
        embedding_label = Tex("Embedding Space").scale(0.5)
        decoder_label = Tex("Decoder").scale(0.5)

        # Assuming the encoder is the second layer and the decoder is the last layer
        encoder_label.next_to(nn.input_layers[2], UP, buff=0.1).shift(.5*UP)
        embedding_label.next_to(nn.input_layers[3], UP, buff=0.1)
        decoder_label.next_to(nn.input_layers[4], UP, buff=0.1).shift(.5*UP)

        self.add(encoder_label, embedding_label, decoder_label)


        self.wait(2)

        # Play animation up to the encoder
        encoder_index = 3  # Index of your encoder layer in the neural network
        forward_pass_animation = make_forward_pass_until_encoder(nn, encoder_index)
        self.play(forward_pass_animation)

        self.wait(2)

        # Position where the arrow will start (middle layer)
        end_point = nn.input_layers[encoder_index].get_center() - 2 * UP

        # Position where the arrow will end (some point below)
        start_point = end_point + DOWN + RIGHT

        # Create an arrow
        arrow = Arrow(start=start_point, end=end_point, buff=0.1).set_color(RED)

        # Create a text label
        label = Tex("The Transformer encoder provides a source of interpretability. Dimensionality\n"
                     "reduction techniques enable analysis of the high-dimensional embedding space.", font_size=30).next_to(arrow.get_start(), DOWN).shift(2*LEFT)

        # Set the z-index of the arrow and text to be higher than the neural network
        arrow.set_z_index(500)
        label.set_z_index(500)

        # Add the arrow and text to the scene
        self.add(arrow,label)

        self.wait(3)

