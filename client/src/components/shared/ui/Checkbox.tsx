// import React, { forwardRef } from 'react';
// import { cn } from '@/utils/helpers';

// interface CustomCheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
//   label?: string;
//   helperText?: string;
//   error?: string;
//   containerClassName?: string;
//   checkboxClassName?: string;
//   labelClassName?: string;
//   errorClassName?: string;
//   helperTextClassName?: string;
// }

// export const Checkbox = forwardRef<HTMLInputElement, CustomCheckboxProps>(({
//   label,
//   helperText,
//   error,
//   containerClassName,
//   checkboxClassName,
//   labelClassName,
//   errorClassName,
//   helperTextClassName,
//   ...props
// }, ref) => {
//   const uniqueId = React.useId();

//   return (
//     <div className={cn("input-container", containerClassName)}>
//       <div className="input-content">
//         <input
//           ref={ref}
//           type="checkbox"
//           id={uniqueId}
//           className={cn(
//             "checkbox-box ",
            
//             error && "input-error",
//             checkboxClassName
//           )}
//           aria-invalid={!!error}
//           aria-describedby={
//             error ? `${uniqueId}-error` : 
//             helperText ? `${uniqueId}-description` : 
//             undefined
//           }
//           {...props}
//         />
//         {label && (
//           <label 
//             htmlFor={uniqueId} 
//             className={cn(
//               "input-label", 
//               error && "input-error",
//               labelClassName
//             )}
//           >
//             {label}
//           </label>
//         )}
//       </div>
      
//       {helperText && !error && (
//         <p 
//           id={`${uniqueId}-description`} 
//           className={cn("helperText", helperTextClassName)}
//         >
//           {helperText}
//         </p>
//       )}

//       {error && (
//         <p 
//           id={`${uniqueId}-error`} 
//           className={cn("input-error-label", errorClassName)}
//         >
//           {error}
//         </p>
//       )}
//     </div>
//   );
// });


import React, { forwardRef } from 'react';
import { cn } from '@/utils/helpers';

interface CustomCheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  helperText?: string;
  error?: string;
  containerClassName?: string;
  checkboxClassName?: string;
  labelClassName?: string;
  errorClassName?: string;
  helperTextClassName?: string;
}

export const Checkbox = forwardRef<HTMLInputElement, CustomCheckboxProps>(({
  label,
  helperText,
  error,
  containerClassName,
  checkboxClassName,
  labelClassName,
  errorClassName,
  helperTextClassName,
  ...props
}, ref) => {
  const uniqueId = React.useId();

  return (
    <div className={cn("checkbox-container", containerClassName)}>
      <label className={cn("checkbox-label", labelClassName)}>
        {/* Hidden Native Checkbox */}
        <input
          ref={ref}
          type="checkbox"
          id={uniqueId}
          className={cn("checkbox-input", checkboxClassName)}
          aria-invalid={!!error}
          aria-describedby={
            error ? `${uniqueId}-error` : 
            helperText ? `${uniqueId}-description` : 
            undefined
          }
          {...props}
        />
        {/* Custom Checkbox Box */}
        <span className={cn("checkmark", error && "checkmark-error")}></span>
        {label && <span className="checkbox-label-text">{label}</span>}
      </label>
      
      {helperText && !error && (
        <p 
          id={`${uniqueId}-description`} 
          className={cn("helperText", helperTextClassName)}
        >
          {helperText}
        </p>
      )}

      {error && (
        <p 
          id={`${uniqueId}-error`} 
          className={cn("input-error-label", errorClassName)}
        >
          {error}
        </p>
      )}
    </div>
  );
});