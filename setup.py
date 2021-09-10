from setuptools import setup, find_packages
import toml

config = toml.load('./extension_info.toml')
#PLUGIN_NAME = f"pymodaq_plugins_{config['plugin-info']['SHORT_PLUGIN_NAME']}" #for all plugins but this one that is the
# default

SHORT_EXTENSION_NAME = config['extension-info']['SHORT_EXTENSION_NAME']
EXTENSION_NAME = f"pymodaq_{SHORT_EXTENSION_NAME}"

from pathlib import Path

with open(str(Path(__file__).parent.joinpath(f'src/{EXTENSION_NAME}/VERSION')), 'r') as fvers:
    version = fvers.read().strip()


with open('README.rst') as fd:
    long_description = fd.read()

setupOpts = dict(
    name=EXTENSION_NAME,
    description=config['extension-info']['description'],
    long_description=long_description,
    license='MIT',
    url=config['extension-info']['package-url'],
    author=config['extension-info']['author'],
    author_email=config['extension-info']['author-email'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: CeCILL-B Free Software License Agreement (CECILL-B)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
    ], )


setup(
    version=version,
    packages=find_packages(where='./src'),
    package_dir={'': 'src'},
    include_package_data=True,
    entry_points={'pymodaq.extension': f'default = {EXTENSION_NAME}'},
    install_requires=['toml', ]+config['extension-install']['packages-required'],
    **setupOpts
)
