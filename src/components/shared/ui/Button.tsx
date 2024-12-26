// components/ui/button/Button.tsx
import React, { forwardRef } from 'react';
import { cn } from '@/utils/helpers';
import { ButtonProps } from './types';

const variantStyles = {
  primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
  secondary: 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500',
  outline: 'border border-gray-300 bg-transparent hover:bg-gray-50 focus:ring-gray-500',
  ghost: 'bg-transparent hover:bg-gray-50 focus:ring-gray-500',
  link: 'bg-transparent underline-offset-4 hover:underline text-blue-600 hover:text-blue-700'
};

const sizeStyles = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg'
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({
    children,
    className,
    variant = 'primary',
    size = 'md',
    isLoading = false,
    disabled,
    fullWidth,
    leftIcon,
    rightIcon,
    type = 'button',
    ...props
  }, ref) => {
    return (
      <button
        ref={ref}
        type={type}
        disabled={disabled || isLoading}
        className={cn(
          // Base styles
          'inline-flex items-center justify-center font-medium rounded-md',
          'focus:outline-none focus:ring-2 focus:ring-offset-2',
          'transition-colors duration-200',
          'disabled:opacity-50 disabled:cursor-not-allowed',
          // Variant styles
          variantStyles[variant],
          // Size styles
          sizeStyles[size],
          // Full width style
          fullWidth && 'w-full',
          className
        )}
        {...props}
      >
        {isLoading ? (
          <>
            <svg
              className="animate-spin -ml-1 mr-2 h-4 w-4"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            Loading...
          </>
        ) : (
          <>
            {leftIcon && <span className="mr-2">{leftIcon}</span>}
            {children}
            {rightIcon && <span className="ml-2">{rightIcon}</span>}
          </>
        )}
      </button>
    );
  }
);

Button.displayName = 'Button';

// Example usage:
/* 
import { Button } from '@/components/ui/button';

function MyComponent() {
  return (
    <div>
      <Button>Default Button</Button>
      
      <Button variant="secondary" size="lg">
        Large Secondary
      </Button>
      
      <Button 
        variant="outline" 
        leftIcon={<IconComponent />}
        isLoading={isLoading}
      >
        With Icon
      </Button>
      
      <Button variant="ghost" fullWidth>
        Full Width Ghost
      </Button>
      
      <Button variant="link">
        Link Style
      </Button>
    </div>

    <div className="space-y-4 mt-8">
        <h2>Button Examples</h2>
        <Button variant="secondary">Secondary</Button>
        <Button variant="outline">Outline</Button>
        <Button variant="ghost">Ghost</Button>
        <Button variant="link">Link Style</Button>
        <Button size="sm">Small</Button>
        <Button size="lg">Large</Button>
        <Button leftIcon={<Download />}>Download</Button>
        <Button isLoading>Processing</Button>
        <Button disabled>Disabled</Button>
      </div>
  );
}
*/