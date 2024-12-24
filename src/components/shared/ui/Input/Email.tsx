// FormComponents/EmailField.tsx
import React, { forwardRef } from 'react';
import { ComponentPropsWithoutRef, ReactNode } from 'react';

interface EmailFieldProps extends Omit<ComponentPropsWithoutRef<'input'>, 'type'>, BaseFieldProps {}

export const EmailField = forwardRef<HTMLInputElement, EmailFieldProps>((props, ref) => {
  return <TextField ref={ref} type="email" {...props} />;
});