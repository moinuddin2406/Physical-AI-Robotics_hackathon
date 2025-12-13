// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Physical AI & Humanoid Robotics — Essentials',
      items: [
        {
          type: 'doc',
          id: 'intro-physical-ai/README',
          label: 'Chapter 1: Introduction to Physical AI'
        },
        {
          type: 'doc',
          id: 'basics-humanoid-robotics/README',
          label: 'Chapter 2: Basics of Humanoid Robotics'
        },
        {
          type: 'doc',
          id: 'ros2-fundamentals/README',
          label: 'Chapter 3: ROS 2 Fundamentals'
        },
        {
          type: 'doc',
          id: 'digital-twin-simulation/README',
          label: 'Chapter 4: Digital Twin Simulation'
        },
        {
          type: 'doc',
          id: 'vision-language-action/README',
          label: 'Chapter 5: Vision-Language-Action Systems'
        },
        {
          type: 'doc',
          id: 'capstone-pipeline/README',
          label: 'Chapter 6: Capstone: Simple AI-Robot Pipeline'
        }
      ],
    }
  ],
};

export default sidebars;