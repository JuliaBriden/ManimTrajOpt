# Manim Trajectory Optimization

ManimTrajOpt is a project that provides animations and visualizations of trajectory optimization and machine learning concepts with the [Manim Community Library](https://www.manim.community/).

## Getting Started 

### Installation

First you will want to [install manim](https://docs.manim.community/en/stable/installation.html). Make sure it is the Manim Community edition, and not the original 3Blue1Brown Manim version. 

Then optionally [install ManimML](https://github.com/helblazer811/ManimML/tree/main) if using NN animations.
`pip install manim_ml`. Note: some recent features may only available if you install from source. 

You can generate a video from any file by running the following in your command line (assuming everything is installed properly):

```bash
$ manim -pql filename.py
```
The above generates a low resolution rendering, you can improve the resolution (at the cost of slowing down rendering speed) by running: 

```bash
$ manim -pqh filename.py
```

## Scenes

1. IntroScene.py: Introduction to constrained optimization and powered descent guidance.
   
![](https://github.com/JuliaBriden/ManimTrajOpt/blob/master/media/gifs/IntroScene.gif)

2. MPCPolytopesScene.py: Introduction to t-SNE as viewed through the lens of explicit MPC.

![](https://github.com/JuliaBriden/ManimTrajOpt/blob/master/media/gifs/MPCPolytopesScene.gif)

3. Motivation.py: Visualize the increasing number of constraints as the number of discretization nodes increases.

![](https://github.com/JuliaBriden/ManimTrajOpt/blob/master/media/gifs/Motivation.gif)

4. NN.py: Visualize a forward pass of a DNN and show the embedding space.

![](https://github.com/JuliaBriden/ManimTrajOpt/blob/master/media/gifs/NN.gif)

5. PrimalDualScene.py: Visualize converging to an optimal solution using an IPM solver.

![](https://github.com/JuliaBriden/ManimTrajOpt/blob/master/media/gifs/PrimalDualScene.gif)

## Citation

If you found ManimTrajOpt useful, please cite it below!

```
@misc{briden2024manimtrajopt,
      title={ManimTrajOpt}, 
      author={Julia Briden},
      year={2024}
}
```

