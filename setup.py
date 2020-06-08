from setuptools import setup, find_packages

setup(
    name='gym_kraby',
    author='Alexandre Iooss',
    author_email='erdnaxe@crans.org',
    license='GPLv3',
    url='https://kraby.readthedocs.io/',
    install_requires=[
        'gym',
        'pybullet',
    ],
    packages=find_packages(),
    package_data = {
        # Include URDF and associated STL
        'gym_kraby': ['data/*.urdf', 'data/meshes/*.stl'],
    },
    include_package_data=True,
    use_scm_version = {
        "local_scheme": "no-local-version"
    },
    setup_requires=['setuptools_scm'],
)
