import gym
import pybullet as p
from time import sleep
import numpy as np
import argparse

# Some settings
parser = argparse.ArgumentParser()
parser.add_argument("--one-leg", action="store_true")
parser.add_argument("--random", action="store_true")
args = parser.parse_args()

# Print float in decimal format
np.set_printoptions(formatter={'float': lambda x: "{0:6.3f}".format(x)})

# Connect to BulletPhysics GUI, can be DIRECT if no user inputs
p.connect(p.GUI)
if args.one_leg:
    env = gym.make('gym_kraby:OneLegBulletEnv-v0')
else:
    env = gym.make('gym_kraby:HexapodBulletEnv-v0')
observation = env.reset()
done = False

if not args.random:
    # Create user debug interface
    params = [p.addUserDebugParameter(p.getJointInfo(env.robot_id, j)[1].decode(), -1, 1, 0)
              for j in env.joint_list]

while not done:
    if not args.random:
        # Read user input and simulate motor
        a = [p.readUserDebugParameter(param) for param in params]
    else:
        a = env.action_space.sample()

    observation, reward, done, _ = env.step(a)
    print("\nobservation", observation)
    print("reward", reward)
    print("done", done)
    sleep(0.01)

print("[!] Env is done")
env.close()
