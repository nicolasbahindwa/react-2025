// FormComponents/TextArea.tsx
import { ComponentPropsWithoutRef, ReactNode } from 'react';
import React, { forwardRef } from 'react';
import { Label } from './Label';
import { cn } from '@/utils/helpers';

import { BaseFieldProps } from "./types";

interface TextFieldProps
  extends ComponentPropsWithoutRef<"input">,
    BaseFieldProps {}

interface TextAreaProps extends ComponentPropsWithoutRef<'textarea'>, BaseFieldProps {}

export const TextArea = forwardRef<HTMLTextAreaElement, TextAreaProps>(({
  label,
  helperText,
  error,
  className,
  containerClassName,
  id,
  rows = 4,
  ...props
}, ref) => {
  const textareaId = id || `textarea-${Math.random().toString(36).slice(2, 9)}`;

  return (
    <div className={cn("space-y-2", containerClassName)}>
      {label && (
        <Label 
          htmlFor={textareaId}
          className={cn(
            "block text-sm font-medium",
            error ? "text-red-500" : "text-gray-700"
          )}
        >
          {label}
        </Label>
      )}
      
      <textarea
        ref={ref}
        id={textareaId}
        rows={rows}
        className={cn(
          "flex w-full rounded-md border border-input bg-background px-3 py-2",
          "text-sm ring-offset-background",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
          "disabled:cursor-not-allowed disabled:opacity-50",
          error && "border-red-500 focus-visible:ring-red-500",
          className
        )}
        aria-invalid={!!error}
        aria-describedby={
          error ? `${textareaId}-error` : 
          helperText ? `${textareaId}-description` : 
          undefined
        }
        {...props}
      />

      {helperText && !error && (
        <p id={`${textareaId}-description`} className="text-sm text-gray-500">
          {helperText}
        </p>
      )}

      {error && (
        <p id={`${textareaId}-error`} className="text-sm text-red-500">
          {error}
        </p>
      )}
    </div>
  );
});
