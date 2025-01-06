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



export const buttonVariants = {
  primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
  secondary: 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500',
  outline: 'border border-gray-300 bg-transparent hover:bg-gray-50 focus:ring-gray-500',
  ghost: 'bg-transparent hover:bg-gray-50 focus:ring-gray-500',
  link: 'bg-transparent underline-offset-4 hover:underline text-blue-600 hover:text-blue-700'
} as const;

export const buttonSizes = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg'
} as const;

export type ButtonVariant = keyof typeof buttonVariants;
export type ButtonSize = keyof typeof buttonSizes;

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
  fullWidth?: boolean;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
}