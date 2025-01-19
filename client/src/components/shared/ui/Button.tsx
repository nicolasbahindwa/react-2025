import React, { forwardRef } from "react";
import { cn } from "@/utils/helpers"; // Ensure this is your utility for classnames
import { ButtonProps, buttonVariants, buttonSizes } from "./types";
import Spinner from "./Spinner";

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      children,
      className,
      variant = "primary", // Default to primary variant
      size = "md", // Default to medium size
      isLoading = false,
      disabled,
      fullWidth,
      leftIcon,
      rightIcon,
      type = "button",
      ...props
    },
    ref
  ) => {
    // Ensure variant and size are valid keys
    const variantClass = buttonVariants[variant] || buttonVariants.primary;
    const sizeClass = buttonSizes[size] || buttonSizes.md;

    return (
      <button
        ref={ref}
        type={type}
        disabled={disabled || isLoading}
        className={cn(
          // Base styles
          "inline-flex items-center justify-center font-medium rounded-md",
          "focus:outline-none focus:ring-2 focus:ring-offset-2",
          "transition-all duration-200",
          "disabled:opacity-50 disabled:cursor-not-allowed",
          // Variant styles
          variantClass,
          // Size styles
          sizeClass,
          // Full width style
          fullWidth && "w-full",
          className
        )}
        {...props}
      >
        {isLoading ? (
          <div className="flex items-center">
            <span>
              Loading <Spinner />
            </span>
          </div>
        ) : (
          <>
            {leftIcon && (
              <span className="mr-2 inline-flex items-center">{leftIcon}</span>
            )}
            {children}
            {rightIcon && (
              <span className="ml-2 inline-flex items-center">{rightIcon}</span>
            )}
          </>
        )}
      </button>
    );
  }
);

Button.displayName = "Button";
