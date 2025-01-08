import { TextField } from '@/components/shared/ui/TextField';
import { UseFormRegister, FieldErrors } from 'react-hook-form';
import { FormRegister } from './types';

interface Props {
  register: UseFormRegister<FormRegister>;
  errors: FieldErrors<FormRegister>;
  isLoading: boolean;
}

const RegisterFormFields: React.FC<Props> = ({ register, errors, isLoading }) => (
  <>
    <TextField
      label="Username"
      type="text"
      {...register('username')}
      required
      error={errors.username?.message}
      placeholder="Enter your username"
      disabled={isLoading}
    />
    <TextField
      label="Email"
      type="email"
      {...register('email')}
      error={errors.email?.message}
      placeholder="Enter a valid email address"
      disabled={isLoading}
    />
    <TextField
      label="Password"
      type="password"
      {...register('password')}
      error={errors.password?.message}
      placeholder="Create a password"
      disabled={isLoading}
    />
    <TextField
      label="Confirm Password"
      type="password"
      {...register('confirmPassword')}
      error={errors.confirmPassword?.message}
      placeholder="Confirm your password"
      disabled={isLoading}
    />
  </>
);

export default RegisterFormFields;
