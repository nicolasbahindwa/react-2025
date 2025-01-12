import { useForm, SubmitHandler } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/shared/ui/Button';
import {Label} from '@/components/shared/ui/Label';
import { FormLogin } from './types';
import { useLoginMutation } from '@/features/Auth/services/actions';
import { useAppDispatch } from '@/hooks/store';
import { setError } from './services/slice/authSlice';
import { ArrowRight } from 'lucide-react';
import { zodResolver } from '@hookform/resolvers/zod';
import { loginSchema } from './validations/login_validation';
import { LoginFormFields } from './components';

function LoginPage() {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const [loginUser, { isLoading, error: loginError }] = useLoginMutation();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormLogin>({
    resolver: zodResolver(loginSchema),
    mode: 'onChange',
  });

  const onSubmit: SubmitHandler<FormLogin> = async (data) => {
    try {
      // Call the login mutation and unwrap the result
      await loginUser(data).unwrap();
      // Redirect to the dashboard on success
      navigate('/dashboard');
    } catch (error) {
      // Handle errors
      const errorMessage =
        error instanceof Error ? error.message : 'Login failed. Please try again.';
      dispatch(setError(errorMessage));
    }
  };

  return (
    <div className="max-w-md mx-auto p-6">
      <h2 className="text-2xl font-semibold text-center">Login to Your Account</h2>

      {/* Display login error */}
      {loginError && (
        <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
          {loginError instanceof Error ? loginError.message : 'Login failed'}
        </div>
      )}

      {/* Login form */}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 mt-6">
        <LoginFormFields register={register} errors={errors} isLoading={isLoading} />
        <Button
          type="submit"
          fullWidth
          rightIcon={<ArrowRight />}
          disabled={isLoading}
          className="mt-4"
        >
          {isLoading ? 'Logging in...' : 'Login'}
        </Button>
        <Label className="block text-sm text-gray-600">
          Forgot your password? <a href="/forgot-password">Reset it</a>
        </Label>
        <Label className="block text-sm text-gray-600">
          Don't have an account? <a href="/register">Register now</a>
        </Label>
      </form>
    </div>
  );
}

export default LoginPage;