from setuptools import find_packages, setup

setup(
    name="mariokart2excel",
    version="0.1.0",
    py_modules=["mariokart2excel"],
    install_requires=["Click", "opencv-python", "openpyxl", "easyocr", "tqdm"],
    entry_points={
        "console_scripts": [
            "mariokart2excel = mariokart2excel:main",
        ],
    },
)
