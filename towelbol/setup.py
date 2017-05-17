from distutils.core import setup

setup(
    name='towelbol',
    version='0.1.0',
    author='S. Dhawan',
    author_email='jrh@example.com',
    packages=['towelstuff', 'towelstuff.test'],
    scripts=['bin/bol.py'],
    url='http://pypi.python.org/pypi/towelbol/',
    license='LICENSE.txt',
    description='Useful towel-related stuff.',
    long_description=open('readme.txt').read(),
    install_requires=[
        "Numpy",
        "scipy",
    ],
)
