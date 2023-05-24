from setuptools import setup, find_packages

setup(
    name="autonomous-api",
    version='1.0',
    description='ChatGPTにAPIの仕組みをやらせるサービス',
    author='Kobori Akira',
    author_email='private.beats@gmail.com',
    url='https://github.com/koboriakira/autonomous-api',
    packages=find_packages(),
    entry_points="""
        [console_scripts]
        autonomous-api = app.cli.cli:execute
    """
)
