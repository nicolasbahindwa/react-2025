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
  primary: "button--primary",
  secondary: "button--secondary",
  tertiary: "button--tertiary",
  success: "button--success",
  warning: "button--warning",
  error: "button--error",
  ghost: "button--ghost",
  link: "button--link"
};


// Define button sizes
export const buttonSizes: Record<ButtonSize, string> = {
  sm: "button--small",
  md: "button--medium",
  lg: "button--large"
}