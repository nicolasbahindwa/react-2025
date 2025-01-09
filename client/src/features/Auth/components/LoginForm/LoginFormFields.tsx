import { TextField } from '@/components/shared/ui/TextField';
import { UseFormRegister, FieldErrors } from 'react-hook-form';
import { FormLogin } from '../../types';

interface Props {
  register: UseFormRegister<FormLogin>;
  errors: FieldErrors<FormLogin>;
  isLoading: boolean;
}

export const LoginFormFields: React.FC<Props> = ({ register, errors, isLoading }) => (
  <>
    <TextField
      label="Email"
      type="email"
      {...register('email')}
      required
      error={errors.email?.message}
      placeholder="Enter your email"
      disabled={isLoading}
    />
    <TextField
      label="Password"
      type="password"
      {...register('password')}
      required
      error={errors.password?.message}
      placeholder="Enter your password"
      disabled={isLoading}
    />
    <div className="flex items-center">
      <input
        type="checkbox"
        {...register('rememberMe')}
        className="h-4 w-4 text-blue-600"
        disabled={isLoading}
      />
      <label className="ml-2 text-sm text-gray-600">Remember Me</label>
    </div>
  </>
);
 