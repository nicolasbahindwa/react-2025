
import { ComponentPropsWithoutRef } from "react";
export interface TextFieldProps extends ComponentPropsWithoutRef<"input"> {
  label?: string;
  helperText?: string;
  error?: boolean;
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
            required
            htmlFor={inputId}
            className={cn(
              "block text-sm font-medium"
            )}
            color="primary"
            error={error} // This will conditionally set the color to "error" if true
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
            " ",
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
          <p id={`${inputId}-description`} className="label--text-helper-text">
            {helperText}
          </p>
        )}

        {error && (
          <p id={`${inputId}-error`} className=" label--error label--italic">
            {error}
          </p>
        )}
      </div>
    );
  }
);

TextField.displayName = "TextField";


 