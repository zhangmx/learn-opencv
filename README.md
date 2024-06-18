# myopencv

learn opencv with python.

## base

opencv version: opencv-contrib-python 4.10


## requirement
use pdm to manage project.

[PDM](https://pdm.fming.dev/) is a Python package manager and project manager. It aims to be a more modern and user-friendly alternative to pipenv. PDM provides a simple and intuitive command-line interface for managing Python packages and virtual environments. It allows you to easily create and manage isolated project environments, install dependencies, and handle project-specific configurations.

To install PDM, you can use pip:

```
pip install pdm
```

Once installed, you can initialize a new project with PDM by running:

```
pdm init
```

This will create a `pyproject.toml` file where you can specify your project dependencies and other configurations. PDM uses a lock file (`pdm.lock`) to ensure reproducible builds and consistent environments.

To install the dependencies specified in your `pyproject.toml`, you can run:

```
pdm install
```

PDM also provides other useful commands for managing your project, such as `pdm update` to update dependencies, `pdm run` to run commands in the project environment, and `pdm sync` to synchronize the project environment with the `pyproject.toml` file.

For more information on how to use PDM, you can refer to the [official documentation](https://pdm.fming.dev/).
