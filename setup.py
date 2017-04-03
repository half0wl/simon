from setuptools import setup

from simon import __version__


setup(
    name='simon_mac',
    version=__version__,
    author='Ray Chen',
    author_email='ray@half0wl.com',
    packages=['simon'],
    scripts=['bin/simon'],
    url='http://pypi.python.org/pypi/simon_mac/',
    license='MIT',
    description='Simple menubar system monitor for macOS.',
    long_description='Visit https://github.com/half0wl/simon for info.',
    install_requires=[
        'psutil >= 5.2.0',
        'pyobjc-core >= 3.2.1',
        'pyobjc-framework-Cocoa >= 3.2.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: MacOS X',
        'Environment :: MacOS X :: Cocoa',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Monitoring',
        'Topic :: Utilities',
    ],
)
