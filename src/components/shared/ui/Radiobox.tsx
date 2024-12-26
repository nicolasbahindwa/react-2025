// FormComponents/Radio.tsx
import React, { forwardRef } from 'react';
import { ComponentPropsWithoutRef, ReactNode } from 'react';
import { OptionType } from './types';
import { Label } from "./Label";
import { cn } from "@/utils/helpers"; 


import { BaseFieldProps } from "./types";

interface TextFieldProps
  extends ComponentPropsWithoutRef<"input">,
    BaseFieldProps {}

interface RadioProps extends Omit<ComponentPropsWithoutRef<'input'>, 'type'>, BaseFieldProps {
  options: OptionType[];
}

export const Radio = forwardRef<HTMLInputElement, RadioProps>(({
  label,
  helperText,
  error,
  className,
  containerClassName,
  id,
  name,
  options,
  ...props
}, ref) => {
  const groupId = id || `radio-group-${Math.random().toString(36).substr(2, 9)}`;

  return (
    <div className={cn("space-y-2", containerClassName)}>
      {label && (
        <Label 
          className={cn(
            "block text-sm font-medium",
            error ? "text-red-500" : "text-gray-700"
          )}
        >
          {label}
        </Label>
      )}
      
      <div className="space-y-2">
        {options.map((option, index) => {
          const optionId = `${groupId}-${index}`;
          return (
            <div key={option.value} className="flex items-center">
              <input
                ref={index === 0 ? ref : undefined}
                type="radio"
                id={optionId}
                name={name}
                value={option.value}
                className={cn(
                  "h-4 w-4 border-gray-300",
                  "focus:ring-2 focus:ring-blue-500",
                  error && "border-red-500",
                  className
                )}
                aria-invalid={!!error}
                aria-describedby={
                  error ? `${groupId}-error` : 
                  helperText ? `${groupId}-description` : 
                  undefined
                }
                {...props}
              />
              <Label 
                htmlFor={optionId}
                className="ml-3 block text-sm font-medium text-gray-700"
              >
                {option.label}
              </Label>
            </div>
          );
        })}
      </div>

      {helperText && !error && (
        <p id={`${groupId}-description`} className="text-sm text-gray-500">
          {helperText}
        </p>
      )}

      {error && (
        <p id={`${groupId}-error`} className="text-sm text-red-500">
          {error}
        </p>
      )}
    </div>
  );
});