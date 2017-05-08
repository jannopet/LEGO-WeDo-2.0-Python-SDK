from setuptools import setup

setup(
    name='wedo2',
    version='1.0',
    description='Python SDK for LEGO WeDo 2.0',
    long_description='A Python SDK, which provides an API for connecting and controlling LEGO WeDo 2.0 Smarthubs. Requires BLED112 Bluetooth LE module.',
    url='https://github.com/jannopet/LEGO-WeDo-2.0-Python-SDK',
    author='Janno Peterson',
    author_email='janno.peterson@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Education',
        'Topic :: Software Development'
    ],
    keywords='SDK lego education',
    packages=[
        "wedo2",
        "wedo2.bluetooth",
        "wedo2.input_output",
        "wedo2.services",
        "wedo2.utils"
    ],
    install_requires=['pygatt']
)

