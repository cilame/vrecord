from setuptools import setup
import vrecord
 
setup(
    name = "vrecord",
    version = vrecord.__version__,
    keywords = "vrecord",
    author = "cilame",
    author_email = "opaquisrm@hotmail.com",
    url="https://github.com/cilame/vrecord",
    license = "MIT",
    description = "",
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],
    packages = [
        "vrecord",
    ],
    python_requires=">=3.6",
    install_requires=[
       'pynput',
    ],
    entry_points={
        'gui_scripts': [
            'vvv = vrecord.recorder:execute',
        ]
    },
)