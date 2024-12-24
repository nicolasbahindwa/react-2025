// FormComponents/Select.tsx
import React, { forwardRef } from 'react';
import { ComponentPropsWithoutRef, ReactNode } from 'react';

interface SelectProps extends ComponentPropsWithoutRef<'select'>, BaseFieldProps {
  options: OptionType[];
  placeholder?: string;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(({
  label,
  helperText,
  error,
  className,
  containerClassName,
  id,
  options,
  placeholder,
  ...props
}, ref) => {
  const selectId = id || `select-${Math.random().toString(36).substr(2, 9)}`;

  return (
    <div className={cn("space-y-2", containerClassName)}>
      {label && (
        <Label 
          htmlFor={selectId}
          className={cn(
            "block text-sm font-medium",
            error ? "text-red-500" : "text-gray-700"
          )}
        >
          {label}
        </Label>
      )}
      
      <select
        ref={ref}
        id={selectId}
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
          error ? `${selectId}-error` : 
          helperText ? `${selectId}-description` : 
          undefined
        }
        {...props}
      >
        {placeholder && (
          <option value="" disabled>
            {placeholder}
          </option>
        )}
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>

      {helperText && !error && (
        <p id={`${selectId}-description`} className="text-sm text-gray-500">
          {helperText}
        </p>
      )}

      {error && (
        <p id={`${selectId}-error`} className="text-sm text-red-500">
          {error}
        </p>
      )}
    </div>
  );
});