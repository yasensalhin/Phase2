#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim'
        ),
        
        Node(
            package='chase_pkg',       
            executable='chase',  
            name='turtle_chase_node',
            output='screen'
        ),
    ])
