from setuptools import setup

setup(
    name='pyRealParser',
    version='0.1.0',
    packages=['pyRealParser'],
    url='https://github.com/drs251/pyRealParser',
    license='MIT',
    platforms=['Windows', 'Mac OS X', 'Linux'],
    author='Daniel R. Stephan',
    author_email='danrstephan@gmail.com',
    keywords = ['music', 'chords', 'irealpro', 'jazz'],
    description='A Python package to read songs in the iRealPro fromat.',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "Topic :: Artistic Software",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Music"]
)
