#!/usr/bin/env python3
import pybullet as p
import numpy as np
from pybullet_data import getDataPath
from gym import Env, spaces
from time import sleep


class HexapodBulletEnv(Env):
    """
    Hexapod simulation OpenAI Gym environnement using PyBullet
    """
    metadata = {'render.modes': ['human']}

    def __init__(self, time_step=0.01):
        super().__init__()

        # 18 actions (servomotors)
        high = np.ones([18])
        self.action_space = spaces.Box(-high, high)

        # 18*(position,speed,torque) + robot positions observations
        high = np.inf * np.ones([3*18+6])
        self.observation_space = spaces.Box(-high, high)

        # Add pybullet_data as search path
        p.setAdditionalSearchPath(getDataPath())

        # Change simulation timestep
        p.setTimeStep(time_step)

    def reset(self):
        p.resetSimulation()

        # Newton's apple
        p.setGravity(0, 0, -9.81)

        # Load a ground
        p.loadURDF("plane.urdf")

        # Load robot
        flags = p.URDF_USE_SELF_COLLISION | p.URDF_USE_INERTIA_FROM_FILE
        #flags |= p.URDF_MERGE_FIXED_LINKS  # only pybullet>2.89
        #flags |= p.URDF_IGNORE_VISUAL_SHAPES  # see collision shapes
        self.robot_id = p.loadURDF("hexapod.urdf", flags=flags)

        # Get all motorized joints id and name (which are revolute joints)
        self.joint_list = [j for j in range(p.getNumJoints(self.robot_id))
                           if p.getJointInfo(self.robot_id, j)[2] == p.JOINT_REVOLUTE]

        # Add torque sensor on servomotors
        for j in self.joint_list:
            p.enableJointForceTorqueSensor(self.robot_id, j)

        # Return observation
        observation = self.get_observation()
        return observation

    def step(self, action):
        # Update servomotors
        transformed_action = [k * np.pi/2 for k in action]
        p.setJointMotorControlArray(bodyIndex=self.robot_id,
                                    jointIndices=self.joint_list,
                                    controlMode=p.POSITION_CONTROL,
                                    targetPositions=transformed_action)

        # Step simulation
        p.stepSimulation()

        # Return observation, reward and done
        reward, done = self.get_reward()
        observation = self.get_observation()
        return observation, reward, done, {}

    def render(self, mode='human', close=False):
        pass

    def get_reward(self):
        reward = 0
        done = False
        return reward, done

    def get_observation(self):
        observation = []

        # Each servomotor position, speed and torque
        for j in self.joint_list:
            pos, vel, _, tor = p.getJointState(self.robot_id, j)
            observation += [pos, vel, tor]

        # Robot position and orientation
        pos, ori = p.getBasePositionAndOrientation(self.robot_id)
        observation += list(pos) + list(ori)

        return observation

    def terminate(self):
        p.disconnect()


if __name__ == '__main__':
    # Connect to BulletPhysics GUI, can be DIRECT if no user inputs
    p.connect(p.GUI)
    env = HexapodBulletEnv()
    observation = env.reset()

    # Create user debug interface
    params = [p.addUserDebugParameter(p.getJointInfo(env.robot_id, j)[1].decode(), -1, 1, 0)
              for j in env.joint_list]

    while True:
        # Read user input and simulate motor
        a = [p.readUserDebugParameter(param) for param in params]
        observation, reward, done, _ = env.step(a)
        print("\nobservation", observation)
        print("reward", reward)
        print("done", done)
        sleep(0.01)
