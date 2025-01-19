import { ComponentPropsWithoutRef, ButtonHTMLAttributes, ReactNode } from "react";
 
export interface BaseFieldProps {
  label?: string;
  helperText?: string;
  error?: string;
  containerClassName?: string;
}

export interface OptionType {
  label: string;
  value: string;
}


export interface TextFieldProps
  extends ComponentPropsWithoutRef<"input">,
  BaseFieldProps {}



// types button
// types.ts

// Define button variants
export type ButtonVariant = 
  | "primary"
  | "secondary" 
  | "tertiary"
  | "success"
  | "warning"
  | "error"
  | "ghost"
  | "link";

export type ButtonSize = "sm" | "md" | "lg";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
  fullWidth?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

// Define button styles for each variant
export const buttonVariants: Record<ButtonVariant, string> = {
  primary: "bg-[var(--action-primary)] text-[var(--text-inverse)] hover:bg-[var(--action-primary-hover)] active:bg-[var(--action-primary-active)] disabled:bg-[var(--action-primary-disabled)] disabled:text-[var(--text-disabled)] focus:ring-[var(--border-focus)]",
  
  secondary: "bg-[var(--bg-surface)] text-[var(--text-primary)] border border-[var(--border-default)] hover:bg-[var(--bg-surface-alt)] hover:border-[var(--border-strong)] active:bg-[var(--action-secondary-active)] disabled:text-[var(--text-disabled)] focus:ring-[var(--border-focus)]",
  
  tertiary: "bg-transparent text-[var(--text-primary)] hover:bg-[var(--bg-surface-alt)] active:bg-[var(--action-secondary-active)] disabled:text-[var(--text-disabled)] focus:ring-[var(--border-focus)]",
  
  success: "bg-[var(--success-500)] text-[var(--text-inverse)] hover:bg-[var(--success-600)] active:bg-[var(--success-700)] disabled:bg-[var(--success-200)] disabled:text-[var(--text-disabled)] focus:ring-[var(--success-400)]",
  
  warning: "bg-[var(--warning-500)] text-[var(--text-primary)] hover:bg-[var(--warning-600)] active:bg-[var(--warning-700)] disabled:bg-[var(--warning-200)] disabled:text-[var(--text-disabled)] focus:ring-[var(--warning-400)]",
  
  error: "bg-[var(--error-500)] text-[var(--text-inverse)] hover:bg-[var(--error-600)] active:bg-[var(--error-700)] disabled:bg-[var(--error-200)] disabled:text-[var(--text-disabled)] focus:ring-[var(--error-400)]",
  
  ghost: "bg-transparent text-[var(--text-primary)] hover:bg-[var(--bg-surface-alt)] active:bg-[var(--action-secondary-active)] disabled:text-[var(--text-disabled)] focus:ring-[var(--border-focus)]",
  
  link: "bg-transparent text-[var(--text-brand)] hover:underline disabled:text-[var(--text-disabled)] focus:ring-[var(--border-focus)] p-0"
};

// Define button sizes
export const buttonSizes: Record<ButtonSize, string> = {
  sm: "px-3 py-1.5 text-sm",
  md: "px-4 py-2 text-base",
  lg: "px-6 py-3 text-lg"
};
