# Training one hexapod leg

This section gives some example of training and draws some conclusions about
the training of a single robot leg.

The environment resets the leg to a random position.
The agent has to command each servomotors
to move the endcap to the objective (visualized by the cross).

```Python
# Reset all joint using normal distribution
for j in self.joint_list:
    p.resetJointState(self.robot_id, j,
                      np.random.uniform(low=-np.pi/4, high=np.pi/4))
```

![One leg environment](img/one_leg_env.png)

The initial observation vector used is:

| Num | Observation                                 |
| --- | ------------------------------------------- |
| 0   | position (first joint)                      |
| 1   | velocity (first joint)                      |
| 2   | torque (first joint)                        |
| 3   | position (first joint)                      |
| 4   | velocity (first joint)                      |
| 5   | torque (first joint)                        |
| 6   | position (first joint)                      |
| 7   | velocity (first joint)                      |
| 8   | torque (first joint)                        |
| 9   | the x-axis component of the endcap position |
| 10  | the y-axis component of the endcap position |
| 11  | the z-axis component of the endcap position |

!!! Note

    Some early tests were done on StableBaselines3
    but as the library is currently being developed,
    the training was failing and the average episode reward was constant.

## First tests with pytorch-a2c-ppo-acktr-gail

The defaults hyperparameters given in the
[README](https://github.com/ikostrikov/pytorch-a2c-ppo-acktr-gail/blob/master/README.md)
are recommanded and are able to give good results for a first training.

!!! Warning

    The reward function is only using the distance to a **fixed** objective,
    and the observation contains the position, velocity and torque of each servomotors
    and also **the absolute position of the endcap** of the leg.

![Training results](img/training_one_leg_pytorch-a2c-ppo-acktr-gail.png)

**The training is successful and converges after 300k steps.**
The `enjoy.py` script shows the leg moving to the fixed target,
but it vibrates after reaching the objective.

## Testing StableBaselines

Start StableBaselines Docker as explained in [previous page](implementations_ppo.md).
Then in Jupyter web interface,

-   `check_env.ipynb` will check that OpenAI Gym environments are working as expected,
-   `one_leg_training.ipynb` is an example of PPO training on one leg,
-   `render.ipynb` will render the agent to a MP4 video or a GIF.

As planned, it works as well as `pytorch-a2c-ppo-acktr-gail` on PyTorch,
but this time we get much more tools such as
[TensorBoard](https://www.tensorflow.org/tensorboard) data and graph.

As StableBaselines stands out as being an easy PPO implementation
with a clear documentation and hyperparameters,
all the following training were done with it.

## Tweaking the observation and reward

There are two problems with the previous trainings:

1.  The observation contains the absolute position of the endcap.

2.  The reward function is the opposite of the distance to a fixed objective,
    or we want the leg to be able to move to any objective that the user inputs.

### Indicating the target position in observations

The absolute position of the endcap could be computed through a mecanical equation using servomotors positions.
But before doing it, it is also interesting to study the learning when
the absolute position is remplaced by:

-   the objective position (constant during one episode),
-   the objective position vector substracted by the current position.
-   the objective position vector substracted by the current position and the objective position.

The third idea comes from
[OpenAI Gym Reacher-v2 environment](https://github.com/openai/gym/wiki/Reacher-v2).
which observation vector is:

| Num | Observation                                                         |
| --- | ------------------------------------------------------------------- |
| 0   | cos(theta) (first joint)                                            |
| 1   | cos(theta) (second joint)                                           |
| 2   | sin(theta) (first joint)                                            |
| 3   | sin(theta) (second joint)                                           |
| 4   | qpos (the x coordinate of the target)                               |
| 5   | qpos (the y coordinate of the target)                               |
| 6   | qvel (the velocity of the fingertip in the x direction)             |
| 7   | qvel (the velocity of the fingertip in the y direction)             |
| 8   | the x-axis component of the vector from the target to the fingertip |
| 9   | the y-axis component of the vector from the target to the fingertip |
| 10  | the z-axis component of the vector from the target to the fingertip |
