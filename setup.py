from distutils.core import setup

setup(
    name='SwaggerReader',
    version='0.0.1dev',
    packages=['swaggerreader',],
    license='MIT',
    install_requires=[
        'requests',
        'json'
    ],
    url='https://github.com/gatneil/SwaggerReader'
)

