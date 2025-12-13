# ROS 2 Fundamentals

## Learning Objectives

By the end of this chapter, you should be able to:
- Understand the architecture of ROS 2 and how it differs from ROS 1
- Explain the concepts of nodes, topics, services, and actions in ROS 2
- Describe package management in ROS 2
- Implement basic robot control using ROS 2 concepts
- Practice with common ROS 2 tools and commands

## What is ROS 2?

ROS 2 (Robot Operating System 2) is not an actual operating system, but rather a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms and configurations.

ROS 2 is the second generation of the Robot Operating System, designed to address limitations of the original ROS (ROS 1) and to provide features necessary for production environments such as:
- Improved real-time support
- Better security
- Enhanced reliability and maintainability
- Quality of Service (QoS) policies for robust communication
- Multi-robot systems support
- Cross-platform compatibility

## ROS 2 Architecture

### Client Library Implementations

ROS 2 supports multiple client library implementations, each tailored to different programming languages and requirements:
- **rclcpp**: C++ client library
- **rclpy**: Python client library
- **rcl**: C client library (the underlying common library)
- Additional languages like Rust, Java, and C# have client libraries

### DDS Middleware

ROS 2 uses Data Distribution Service (DDS) as its underlying communication middleware. DDS provides:
- Publish/subscribe message passing
- Request/reply communication
- Discovery services
- Quality of Service (QoS) policies
- Language and platform independence

Popular DDS implementations include:
- Fast DDS (by eProsima)
- Cyclone DDS (by Eclipse)
- RTI Connext DDS
- OpenSplice DDS

## Core ROS 2 Concepts

### Nodes

A node is an executable that uses ROS to communicate with other nodes. Nodes are the fundamental building blocks of ROS applications. They can:
- Publish messages to topics
- Subscribe to topics
- Provide services
- Call services
- Send and receive actions

In ROS 2, nodes are contained within a process, and a single process can contain multiple nodes. Each node has its own name, namespace, and parameters.

Example of creating a simple node in Python:

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node_name')
        self.get_logger().info('Hello from my_node_name!')

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Topics and Messages

Topics provide a way for nodes to send and receive data asynchronously through a publish/subscribe communication pattern.

**Publishers** send messages to a topic, and **subscribers** receive messages from a topic. Multiple publishers and subscribers can be connected to the same topic.

Messages are defined in `.msg` files with simple data structures containing primitive types like integers, floats, booleans, strings, and arrays. Each message type has a specific format.

Common built-in message types include:
- `std_msgs`: Standard message types like String, Int32, Float64, etc.
- `geometry_msgs`: Messages for spatial operations like Point, Pose, Twist, etc.
- `sensor_msgs`: Messages for sensor data like LaserScan, Image, JointState, etc.

### Services

Services provide a request/reply communication pattern where a client sends a request to a server and waits for a response. This is synchronous communication, unlike the asynchronous nature of topics.

Service definitions are stored in `.srv` files, which specify the request and response message types. The format is:
```
[Request Message]
---
[Response Message]
```

Example: A service that adds two integers
```
int64 a
int64 b
---
int64 sum
```

### Actions

Actions are used for long-running tasks that have:
- Goal: Request to start a task
- Feedback: Periodic updates during the task
- Result: Final outcome when the task completes

Actions are defined in `.action` files with the format:
```
[Goal]
---
[Result]
---
[Feedback]
```

## ROS 2 Packages and Workspaces

### Packages

A package is the basic unit of organization in ROS 2. It contains:
- Source code (C++ and/or Python)
- Launch files
- Configuration files
- Message/service/action definitions
- Dependencies

Each package has:
- A `package.xml` file describing the package
- A `CMakeLists.txt` file for C++ packages
- Python setup files for Python packages

### Workspaces

A workspace is a directory that contains one or more packages and is used for development. The typical workspace structure is:
```
workspace_folder/
  src/
    package1/
    package2/
    ...
  build/
  install/
  log/
```

The `src` directory contains the source code of packages, while `build`, `install`, and `log` are generated during the build process.

### Colcon Build System

ROS 2 uses `colcon` as the build system, which is an improvement over `catkin` from ROS 1:
- Supports multiple build systems
- Parallel builds
- Per-package build commands
- Flexible build configuration

## Quality of Service (QoS)

QoS policies allow fine-tuning communication between nodes, which is especially important in production environments where reliability is crucial. QoS settings include:

- **Reliability**: Best effort vs. reliable delivery
- **Durability**: Volatile vs. transient local (for late-joining subscribers)
- **History**: Keep all messages vs. keep last N messages
- **Deadline**: Maximum time between messages
- **Lifespan**: How long messages are kept in history

## Practical Example: TurtleSim

TurtleSim is a simple simulator that provides a visual interface for learning ROS 2 concepts. Let's look at how the key concepts apply:

1. **Nodes**: turtle1, turtle2, teleop, turtlesim_node
2. **Topics**: /turtle1/cmd_vel (for sending velocity commands), /turtle1/pose (for getting position)
3. **Services**: /reset (to reset the simulation), /spawn (to create new turtles), /kill (to remove turtles)
4. **Actions**: Not used in basic TurtleSim

Command to run TurtleSim:
```bash
ros2 run turtlesim turtlesim_node
```

Command to control the turtle:
```bash
ros2 run turtlesim turtle_teleop_key
```

## Communication Patterns with Examples

### Publisher Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Subscriber Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Common ROS 2 Commands

### General Commands
- `ros2 run <package_name> <executable_name>`: Run a node
- `ros2 launch <package_name> <launch_file>`: Launch multiple nodes
- `ros2 topic list`: List all active topics
- `ros2 service list`: List all available services
- `ros2 action list`: List all available actions

### Topic Commands
- `ros2 topic echo <topic_name>`: Display messages on a topic
- `ros2 topic pub <topic_name> <msg_type> <args>`: Publish a message to a topic
- `ros2 topic info <topic_name>`: Display information about a topic

### Service Commands
- `ros2 service call <service_name> <service_type> <request_args>`: Call a service

### Node Commands
- `ros2 node list`: List all active nodes
- `ros2 node info <node_name>`: Display information about a node

## Security in ROS 2

ROS 2 includes security features that were not present in ROS 1:
- **Authentication**: Verifying the identity of ROS entities
- **Authorization**: Controlling what authenticated entities can do
- **Encryption**: Protecting communication between entities

Security is implemented using DDS Security, which provides:
- Identity certificates
- Access control lists
- Secure communication channels

## Practical Implementation

Let's implement a simple example that demonstrates nodes, topics, services, and basic robot control:

1. Create a package for our example:
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python my_robot_controller
```

2. Inside the package, create a publisher for velocity commands and a service for changing robot behavior.

This example demonstrates how ROS 2 concepts can be used to control a robot, with nodes handling different aspects of the robot's behavior and communicating through topics and services.

## Comparison with ROS 1

| Feature | ROS 1 | ROS 2 |
|---------|-------|--------|
| Communication | Custom | DDS-based |
| Real-time Support | Limited | Improved |
| Security | No | Built-in |
| Platforms | Linux | Linux, Windows, macOS, others |
| Architecture | Master-based | Distributed |
| Quality of Service | No | Yes |
| Cross-compilation | Difficult | Improved |

## Best Practices

1. **Use namespaces** to organize your nodes and topics in larger systems
2. **Set appropriate QoS policies** based on your application requirements
3. **Structure your packages** logically and follow naming conventions
4. **Use launch files** to start multiple nodes with appropriate parameters
5. **Implement proper error handling** in your nodes
6. **Document your custom message types** and interfaces clearly

## Summary

ROS 2 is a flexible framework for developing robot applications that addresses the limitations of ROS 1 and provides features necessary for production environments. Key concepts include nodes (executables), topics (publish/subscribe communication), services (request/reply communication), and actions (for long-running tasks). The architecture is built on DDS middleware, providing Quality of Service policies, security, and cross-platform support. Package management with colcon and proper workspace organization help structure development projects. ROS 2 is widely used in research, industry, and commercial robotics applications.

## Exercises

1. Explain the difference between ROS 2 and ROS 1 in terms of architecture and communication.
2. Create a simple publisher and subscriber pair in ROS 2 using Python.
3. Describe how Quality of Service policies affect communication in ROS 2 systems.

## Next Chapter

Continue to [Chapter 4: Digital Twin Simulation](../digital-twin-simulation/README.md) to learn about simulation environments for robotics and their applications.

---
**Chapter Word Count**: 1,420