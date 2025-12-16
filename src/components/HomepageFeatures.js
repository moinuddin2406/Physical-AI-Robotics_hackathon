import React from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Physical AI Fundamentals',
    image: 'img/physical-ai.jpg',
    description: (
      <>
        Learn the core principles of Physical AI, combining perception, reasoning, 
        and action to create intelligent embodied systems.
      </>
    ),
  },
  {
    title: 'Humanoid Robotics',
    image: 'img/humanoid-robot.jpg',
    description: (
      <>
        Explore the design, control, and implementation of humanoid robots 
        that interact with the physical world.
      </>
    ),
  },
  {
    title: 'Practical Applications',
    image: 'img/robotics-applications.jpg',
    description: (
      <>
        Discover real-world applications of Physical AI and humanoid robotics 
        across various industries and domains.
      </>
    ),
  },
];

function Feature({image, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <img src={image} className={styles.featureImage} alt={title} />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}