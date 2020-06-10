from gym.envs.registration import register

register(
    id='HexapodBulletEnv-v0',
    entry_point='gym_kraby.envs:HexapodBulletEnv',
)

register(
    id='HexapodRealEnv-v0',
    entry_point='gym_kraby.envs:HexapodRealEnv',
)

register(
    id='OneLegBulletEnv-v0',
    entry_point='gym_kraby.envs:OneLegBulletEnv',
)

register(
    id='OneLegRealEnv-v0',
    entry_point='gym_kraby.envs:OneLegRealEnv',
)
