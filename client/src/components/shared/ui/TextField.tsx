
import { ComponentPropsWithoutRef } from "react";
export interface TextFieldProps extends ComponentPropsWithoutRef<"input"> {
  label?: string;
  helperText?: string;
  error?: string;
  containerClassName?: string;
  required?: boolean;
}

// TextField.tsx
import React, { forwardRef } from "react";
import { Label } from "./Label";
import { cn } from "@/utils/helpers";
// import { TextFieldProps } from "./types";
 
export const TextField = forwardRef<HTMLInputElement, TextFieldProps>(
  (
    { 
      label, 
      helperText, 
      error, 
      className, 
      containerClassName, 
      id,
      required,
      ...props 
    },
    ref
  ) => {
    const inputId = id || `input-${Math.random().toString(36).slice(2, 11)}`;

    return (
      <div className={cn("space-y-2", containerClassName)}>
        {label && (
          <Label
            htmlFor={inputId}
            required={required}
            className={cn(
              "block text-sm font-medium",
              error ? "text-red-500" : "text-gray-700"
            )}
          >
            {label}
          </Label>
        )}

        <input
          ref={ref}
          id={inputId}
          required={required}
          className={cn(
            "input ",
            "input:disabled",
            error && "input-error",
            
            className
          )}
          aria-invalid={!!error}
          aria-describedby={
            error
              ? `${inputId}-error`
              : helperText
              ? `${inputId}-description`
              : undefined
          }
          {...props}
        />

        {helperText && !error && (
          <p id={`${inputId}-description`} className="text-xs text-neutral-500">
            {helperText}
          </p>
        )}

        {error && (
          <p id={`${inputId}-error`} className="font-italic font-thin pl-1 text-xs text-error-500">
            {error}
          </p>
        )}
      </div>
    );
  }
);

TextField.displayName = "TextField";


 