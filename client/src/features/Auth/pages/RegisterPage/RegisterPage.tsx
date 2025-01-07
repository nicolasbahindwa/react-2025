import React from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { TextField } from '@/components/shared/ui/TextField';
import { Button } from '@/components/shared/ui/Button';
import { FormRegister } from './types';
import { useRegisterMutation } from '@/features/Auth/services/api/authApi';
import { useAppDispatch } from '@/hooks/store'; // Type-safe dispatch hook
import { setUser, setError } from '../../services/slice';
import { ArrowRight } from 'lucide-react';
import { zodResolver } from '@hookform/resolvers/zod';
import { registerSchema } from './validation';

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
      const response = await registerUser(data).unwrap();
      dispatch(setUser(response));
      navigate('/dashboard');
    } catch (error) {
      const errorMessage = 
        error instanceof Error 
          ? error.message 
          : 'Registration failed. Please try again.';
      dispatch(setError(errorMessage));
    }
  };

  // Extract form fields to a separate component for better organization
  const renderFormFields = () => (
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

  return (
    <div className="max-w-md mx-auto p-6">
      <h2 className="text-2xl font-semibold text-center">
        Create Your Account
      </h2>

      {registerError && (
        <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
          {registerError instanceof Error
            ? registerError.message
            : "Registration failed"}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 mt-6">
        {renderFormFields()}

        <div className="flex items-center">
          <input
            type="checkbox"
            {...register("terms")}
            className="h-4 w-4 text-blue-600"
            disabled={isLoading}
          />
          <label className="ml-2 text-sm text-gray-600">
            I agree to the{" "}
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
          {isLoading ? "Registering..." : "Register"}
        </Button>
        <Button
          variant="primary"
          size="md"
          leftIcon={<ArrowRight />}
          disabled={isLoading}
          onClick={() => console.log("clicked")}
        >
          Click Me
        </Button>
      </form>
    </div>
  );
}

export default RegisterPage;