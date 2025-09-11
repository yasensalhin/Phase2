from setuptools import find_packages, setup

package_name = 'weather_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='YasenSalhin',
    maintainer_email='yasensalhin@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'temp_node=weather_pkg.temp_node:main',
            'humidity_node=weather_pkg.humidity_node:main',
            'pressure_node=weather_pkg.pressure_node:main',
            'monitor = weather_pkg.monitor:main'
        ],
    },
)
