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
          "button",
          // Variant styles
          variantClass,
          // Size styles
          sizeClass,
          // Full width style
          fullWidth && "button--full-width",
          className
        )}
        {...props}
      >
        {isLoading ? (
          <div className="button__loading">
            <span>
              Loading <Spinner className="spinner" />
            </span>
          </div>
        ) : (
          <>
            {leftIcon && (
              <span className="button__icon button__icon--left">{leftIcon}</span>
            )}
            {children}
            {rightIcon && (
              <span className="button__icon button__icon--right">{rightIcon}</span>
            )}
          </>
        )}
      </button>
    );
  }
);

Button.displayName = "Button";
