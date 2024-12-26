import { ComponentPropsWithoutRef, ReactNode } from "react";

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
