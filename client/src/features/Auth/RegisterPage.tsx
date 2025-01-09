import { useForm, SubmitHandler } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/shared/ui/Button';
import { FormRegister } from './types';
import { useRegisterMutation } from '@/features/Auth/services/actions';
import { useAppDispatch } from '@/hooks/store';
import { setError, setUser } from './services/slice/userAuthSlice';
import { ArrowRight } from 'lucide-react';
import { zodResolver } from '@hookform/resolvers/zod';
import { registerSchema } from './validations/registration_validation';
import { RegisterFormFields } from './components';

function RegisterPage() {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const [registerUser, { isLoading, error: registerError }] = useRegisterMutation();

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<FormRegister>({
    resolver: zodResolver(registerSchema),
    mode: 'onChange',
  });

  const passwordValue = watch('password');

  const onSubmit: SubmitHandler<FormRegister> = async (data) => {
    try {
      // Call the register mutation and unwrap the result
      await registerUser(data).unwrap();
      // Redirect to the dashboard on success
      navigate('/login');
    } catch (error) {
      // Handle errors
      const errorMessage =
        error instanceof Error ? error.message : 'Registration failed. Please try again.';
      dispatch(setError(errorMessage));
    }
  };

  return (
    <div className="max-w-md mx-auto p-6">
      <h2 className="text-2xl font-semibold text-center">Create Your Account</h2>

      {/* Display registration error */}
      {registerError && (
        <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
          {registerError instanceof Error ? registerError.message : 'Registration failed'}
        </div>
      )}

      {/* Registration form */}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 mt-6">
        <RegisterFormFields register={register} errors={errors} isLoading={isLoading} />
        <div className="flex items-center">
          <input
            type="checkbox"
            {...register('terms')}
            className="h-4 w-4 text-blue-600"
            disabled={isLoading}
          />
          <label className="ml-2 text-sm text-gray-600">
            I agree to the{' '}
            <a href="/terms" className="text-blue-600">
              Terms and Conditions
            </a>
          </label>
        </div>
        <Button
          type="submit"
          fullWidth
          rightIcon={<ArrowRight />}
          disabled={isLoading}
          className="mt-4"
        >
          {isLoading ? 'Registering...' : 'Register'}
        </Button>
      </form>
    </div>
  );
}

export default RegisterPage;