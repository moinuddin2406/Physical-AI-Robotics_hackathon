import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Physical AI',
    description: (
      <>
        Explore how AI can be grounded in physical reality for robotics applications.
      </>
    ),
  },
  {
    title: 'Humanoid Robotics',
    description: (
      <>
        Learn about the design, control, and autonomy of humanoid robots.
      </>
    ),
  },
  {
    title: 'Comprehensive Textbook',
    description: (
      <>
        A complete guide covering all aspects from fundamentals to advanced topics.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
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