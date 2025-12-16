import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();

  // Chapter card data - All 6 chapters
  const chapters = [
    {
      title: "Introduction to Physical AI",
      description: "Core concepts of Physical AI, combining perception, reasoning, and action",
      path: "/docs/intro-physical-ai/",
      icon: (
        <svg className={styles.chapterCardIcon} viewBox="0 0 24 24">
          <path d="M12,3L1,9L12,15L21,10.09V17H23V9M5,13.18V17.18L12,21.18L19,17.18V13.18L12,17.18L5,13.18Z" />
        </svg>
      )
    },
    {
      title: "Basics of Humanoid Robotics",
      description: "Design, mechanics, and principles of humanoid robots",
      path: "/docs/basics-humanoid-robotics/",
      icon: (
        <svg className={styles.chapterCardIcon} viewBox="0 0 24 24">
          <path d="M12,10.83L15.17,14.17L16.58,12.76L12,8.17L7.42,12.76L8.83,14.17L12,10.83M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z" />
        </svg>
      )
    },
    {
      title: "ROS 2 Fundamentals",
      description: "Robot Operating System concepts and implementation",
      path: "/docs/ros2-fundamentals/",
      icon: (
        <svg className={styles.chapterCardIcon} viewBox="0 0 24 24">
          <path d="M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22C6.47,22 2,17.5 2,12A10,10 0 0,1 12,2Z" />
        </svg>
      )
    },
    {
      title: "Digital Twin Simulation",
      description: "Creating virtual models of physical robot systems",
      path: "/docs/digital-twin-simulation/",
      icon: (
        <svg className={styles.chapterCardIcon} viewBox="0 0 24 24">
          <path d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L5,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.21,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.21,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 5,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.67 16.04,18.34 16.56,17.94L19,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z" />
        </svg>
      )
    },
    {
      title: "Vision-Language-Action Systems",
      description: "Integrating perception, language understanding, and physical action",
      path: "/docs/vision-language-action/",
      icon: (
        <svg className={styles.chapterCardIcon} viewBox="0 0 24 24">
          <path d="M7.5,12C5.47,12 3.76,10.68 3.25,8.82L2.19,5.17L5.84,4.11C7.7,3.59 9.5,4.47 10.13,6.12C10.38,5.31 11.11,4.69 12,4.69C12.64,4.69 13.22,4.96 13.64,5.39L15.89,3.14L17.19,6.86L14.94,9.11C15.37,9.91 15.37,10.86 14.94,11.65L17.19,13.91L15.89,17.62L13.64,15.37C12.85,15.8 11.9,15.8 11.1,15.37C10.68,15.79 10.1,16.05 9.5,16.05C8.6,16.05 7.75,15.57 7.25,14.83C6.72,15.5 5.82,16 4.75,16C3.62,16 2.67,15.2 2.41,14.13L1.11,10.41L4.75,9.35C5.27,11.21 6.48,12 7.5,12M22,9V15C22,16.11 21.11,17 20,17H16.5V15.5H20V9H16.5V7.5H20A1,1 0 0,1 21,8.5V9H22M14,9V15H12.5V10.5H11V9H14M9.5,9V15H8V9H9.5Z" />
        </svg>
      )
    },
    {
      title: "Capstone: Simple AI-Robot Pipeline",
      description: "Integrating all concepts into a practical AI-robot system",
      path: "/docs/capstone-pipeline/",
      icon: (
        <svg className={styles.chapterCardIcon} viewBox="0 0 24 24">
          <path d="M12,2A7,7 0 0,1 19,9C19,11.38 17.81,13.47 16,14.74V17A1,1 0 0,1 15,18H9A1,1 0 0,1 8,17V14.74C6.19,13.47 5,11.38 5,9A7,7 0 0,1 12,2M9,21V20H15V21A1,1 0 0,1 14,22H10A1,1 0 0,1 9,21M12,4A5,5 0 0,0 7,9C7,11.05 8.23,12.81 10,13.58V16H14V13.58C15.77,12.81 17,11.05 17,9A5,5 0 0,0 12,4Z" />
        </svg>
      )
    }
  ];

  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro-physical-ai">
            Start Learning - 5 min ⏱️
          </Link>
        </div>

        {/* Chapter Cards Section */}
        <div className={styles.chapterCardsContainer}>
          {chapters.map((chapter, index) => (
            <Link
              key={index}
              to={chapter.path}
              className={styles.chapterCard}
            >
              <h3>
                {chapter.icon}
                {chapter.title}
              </h3>
              <p>{chapter.description}</p>
            </Link>
          ))}
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="A comprehensive textbook on Physical AI and Humanoid Robotics">
      <HomepageHeader />
    </Layout>
  );
}