import React, { ComponentPropsWithoutRef, forwardRef } from "react";
import { cn } from "@/utils/helpers";

interface LabelProps extends ComponentPropsWithoutRef<"label"> {
  /**
   * Whether the label is required
   */
  required?: boolean;
}

export const Label = forwardRef<HTMLLabelElement, LabelProps>(
  ({ className, children, required, ...props }, ref) => {
    return (
      <label
        ref={ref}
        className={cn(
          "text-sm py-1 font-medium leading-none peer-disabled:cursor-not-allowed",
          className
        )}
        {...props}
      >
        {children}
        {required && <span className="text-error-500 ml-1">*</span>}
      </label>
    );
  }
);

Label.displayName = "Label";
