import React, { ComponentPropsWithoutRef, forwardRef } from "react";
import { cn } from "@/utils/helpers";

interface LabelProps extends ComponentPropsWithoutRef<"label"> {
  /**
   * Whether the label is required
   */
  required?: boolean;
  /**
   * Whether the label should be bold
   */
  bold?: boolean;
  /**
   * Custom color for the label
   */
  color?: "primary" | "secondary" | "success" | "warning" | "error" | "default";
  /**
   * Error state
   */
  error?: boolean;
}

export const Label = forwardRef<HTMLLabelElement, LabelProps>(
  ({ className, children, required, bold, color = "default", error, ...props }, ref) => {
    const labelColor = error ? "error" : color;

    return (
      <label
        ref={ref}
        className={cn(
          "label",
          bold && "label--bold",
          `label--${labelColor}`,
          className
        )}
        {...props}
      >
        {children}
        {required && <span className="label__required">*</span>}
      </label>
    );
  }
);

Label.displayName = "Label";
