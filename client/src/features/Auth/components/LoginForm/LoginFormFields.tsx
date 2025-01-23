import { TextField } from '@/components/shared/ui/TextField';
import { Checkbox } from '../../../../components/shared/ui/Checkbox';
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
      className="input-small"
      disabled={isLoading}
    />
    <TextField
      label="Password"
      type="password"
      {...register('password')}
      required
      error={errors.password?.message}
      placeholder="Enter your password"
      className="input-small"
      disabled={isLoading}
    />
    <div className="flex items-center">
    <Checkbox
        label="Accept terms and conditions"
        helperText="You must agree to the terms to proceed."
        id="terms"
      />
       
       
    </div>
  </>
);
 