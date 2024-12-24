// FormComponents/Checkbox.tsx
import React, { forwardRef } from 'react';
import { ComponentPropsWithoutRef, ReactNode } from 'react';

interface CheckboxProps extends Omit<ComponentPropsWithoutRef<'input'>, 'type'>, BaseFieldProps {}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(({
  label,
  helperText,
  error,
  className,
  containerClassName,
  id,
  ...props
}, ref) => {
  const checkboxId = id || `checkbox-${Math.random().toString(36).substr(2, 9)}`;

  return (
    <div className={cn("flex items-start", containerClassName)}>
      <div className="flex items-center h-5">
        <input
          ref={ref}
          type="checkbox"
          id={checkboxId}
          className={cn(
            "h-4 w-4 rounded border-gray-300",
            "focus:ring-2 focus:ring-blue-500",
            error && "border-red-500",
            className
          )}
          aria-invalid={!!error}
          aria-describedby={
            error ? `${checkboxId}-error` : 
            helperText ? `${checkboxId}-description` : 
            undefined
          }
          {...props}
        />
      </div>
      <div className="ml-3 text-sm">
        {label && (
          <Label 
            htmlFor={checkboxId}
            className={cn(
              "font-medium",
              error ? "text-red-500" : "text-gray-700"
            )}
          >
            {label}
          </Label>
        )}
        
        {helperText && !error && (
          <p id={`${checkboxId}-description`} className="text-gray-500">
            {helperText}
          </p>
        )}

        {error && (
          <p id={`${checkboxId}-error`} className="text-red-500">
            {error}
          </p>
        )}
      </div>
    </div>
  );
});
