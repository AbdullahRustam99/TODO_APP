'use client';

import { motion } from 'framer-motion';

// Animation variants for common UI elements
export const fadeIn = {
  initial: { opacity: 0 },
  animate: { opacity: 1, transition: { duration: 0.5 } },
  exit: { opacity: 0 }
};

export const slideIn = {
  initial: { y: 20, opacity: 0 },
  animate: { y: 0, opacity: 1, transition: { duration: 0.5 } },
  exit: { y: 20, opacity: 0 }
};

export const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
};

// Animated components using Framer Motion
export const AnimatedDiv = motion.div;
export const AnimatedSection = motion.section;
export const AnimatedCard = motion.div;
export const AnimatedButton = motion.button;
export const AnimatedInput = motion.input;
export const AnimatedListItem = motion.div;

// Animation wrapper component
interface AnimationWrapperProps {
  children: React.ReactNode;
  type?: 'fade' | 'slide' | 'stagger';
  delay?: number;
  duration?: number;
  className?: string;
}

export const AnimationWrapper = ({
  children,
  type = 'fade',
  delay = 0,
  duration = 0.5,
  className = ''
}: AnimationWrapperProps) => {
  const variants = {
    initial: type === 'slide' ? { y: 20, opacity: 0 } : { opacity: 0 },
    animate: {
      y: 0,
      opacity: 1,
      transition: {
        delay,
        duration,
        ease: [0.25, 0.46, 0.45, 0.94] // Custom easing for smooth animations
      }
    }
  };

  return (
    <motion.div
      initial="initial"
      animate="animate"
      variants={variants}
      className={className}
    >
      {children}
    </motion.div>
  );
};

// Staggered animation wrapper for lists
interface StaggerWrapperProps {
  children: React.ReactNode;
  className?: string;
}

export const StaggerWrapper = ({ children, className = '' }: StaggerWrapperProps) => {
  return (
    <motion.div
      initial="hidden"
      animate="show"
      variants={staggerContainer}
      className={className}
    >
      {children}
    </motion.div>
  );
};

// Individual item for staggered animations
interface StaggerItemProps {
  children: React.ReactNode;
  className?: string;
}

export const StaggerItem = ({ children, className = '' }: StaggerItemProps) => {
  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    show: { y: 0, opacity: 1, transition: { type: 'spring', damping: 12 } }
  };

  return (
    <motion.div
      variants={itemVariants}
      className={className}
    >
      {children}
    </motion.div>
  );
};