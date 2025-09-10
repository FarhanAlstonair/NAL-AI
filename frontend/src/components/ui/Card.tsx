import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/utils/cn';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'default' | 'glass' | 'luxury';
  hover?: boolean;
}

const Card: React.FC<CardProps> = ({
  children,
  className,
  variant = 'default',
  hover = false,
}) => {
  const baseClasses = 'rounded-2xl transition-all duration-300';
  
  const variants = {
    default: 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg',
    glass: 'glass-card',
    luxury: 'bg-gradient-to-br from-white to-gray-50 dark:from-gray-800 dark:to-gray-900 border border-luxury-gold/20 shadow-2xl',
  };

  const Component = hover ? motion.div : 'div';
  const motionProps = hover ? {
    whileHover: { y: -8, scale: 1.02 },
    transition: { duration: 0.2 }
  } : {};

  return (
    <Component
      className={cn(
        baseClasses,
        variants[variant],
        hover && 'cursor-pointer',
        className
      )}
      {...motionProps}
    >
      {children}
    </Component>
  );
};

export default Card;