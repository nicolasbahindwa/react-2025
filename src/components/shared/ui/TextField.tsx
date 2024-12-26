import React, { forwardRef } from "react";
import { ComponentPropsWithoutRef, ReactNode } from "react";
import { Label } from "./Label";
import { cn } from "@/utils/helpers";

import { BaseFieldProps } from "./types";

interface TextFieldProps
  extends ComponentPropsWithoutRef<"input">,
    BaseFieldProps {}

export const TextField = forwardRef<HTMLInputElement, TextFieldProps>(
  (
    { label, helperText, error, className, containerClassName, id, ...props },
    ref
  ) => {
    const inputId = id || `input-${Math.random().toString(36).slice(2, 11)}`;

    return (
      <div className={cn("space-y-2", containerClassName)}>
        {label && (
          <Label
            htmlFor={inputId}
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
          className={cn(
            "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2",
            "text-sm ring-offset-background",
            "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
            "disabled:cursor-not-allowed disabled:opacity-50",
            error && "border-red-500 focus-visible:ring-red-500",
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
          <p id={`${inputId}-description`} className="text-sm text-gray-500">
            {helperText}
          </p>
        )}

        {error && (
          <p id={`${inputId}-error`} className="text-sm text-red-500">
            {error}
          </p>
        )}
      </div>
    );
  }
);

TextField.displayName = "TextField";
