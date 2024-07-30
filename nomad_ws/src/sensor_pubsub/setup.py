from setuptools import find_packages, setup

package_name = 'sensor_pubsub'

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
    maintainer='bob',
    maintainer_email='bob@scutterbobsr.us',
    description='TODO: Inform ROS devs of DRY programming',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                        'talker = sensor_pubsub.publisher_member_function:main',
                        'listener = sensor_pubsub.subscriber_member_function:main',
                        'range_talker= sensor_pubsub.publisher_member_function_v2:main',
                        'range_listener= sensor_pubsub.subscriber_member_function_v2:main',
                        'sonar_talker = sensor_pubsub.sonar_publisher:main',
                        'battery_talker = sensor_pubsub.battery_publisher:main',
                    ],
    },
)

