import React from 'react';
import { useForm, SubmitHandler, useWatch } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { TextField } from '@/components/shared/ui/TextField';
import { Button } from '@/components/shared/ui/Button';
import { FormRegister } from './types';
import { useRegisterMutation } from '@/features/Auth/services/api/authApi';
import { useDispatch } from 'react-redux';
import { setUser, setError } from '../../services/slice';
import { ArrowRight } from 'lucide-react';

function RegisterPage() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [registerUser, { isLoading }] = useRegisterMutation(); // Renamed to registerUser

  const {
    register,  // Keep the original register from useForm
    handleSubmit,
    formState: { errors },
    control,
  } = useForm<FormRegister>();

  const passwordValue = useWatch({ control, name: 'password' });

  const onSubmit: SubmitHandler<FormRegister> = async (data) => {
    try {
      const response = await registerUser(data).unwrap(); // Using renamed mutation
      dispatch(setUser(response));
      navigate('/dashboard');
    } catch (error) {
      dispatch(setError(error instanceof Error ? error.message : 'Registration failed'));
    }
  };

  return (
    <div className="max-w-md mx-auto p-6">
      <h2 className="text-2xl font-semibold text-center">Create Your Account</h2>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 mt-6">
        {/* Username Field */}
        <TextField
          label="Username"
          type="text"
          {...register('username', { required: 'Username is required' })}
          error={errors.username?.message}
          placeholder="Enter your username"
          disabled={isLoading}
        />

        {/* Email Field */}
        <TextField
          label="Email"
          type="email"
          {...register('email', { required: 'Email is required' })}
          error={errors.email?.message}
          placeholder="Enter a valid email address"
          disabled={isLoading}
        />

        {/* Password Field */}
        <TextField
          label="Password"
          type="password"
          {...register('password', { required: 'Password is required' })}
          error={errors.password?.message}
          placeholder="Create a password"
          disabled={isLoading}
        />

        {/* Confirm Password Field */}
        <TextField
          label="Confirm Password"
          type="password"
          {...register('confirmPassword', { 
            required: 'Confirm password is required',
            validate: (value) => value === passwordValue || 'Passwords do not match',
          })}
          error={errors.confirmPassword?.message}
          placeholder="Confirm your password"
          disabled={isLoading}
        />

        {/* Terms and Conditions */}
        <div className="flex items-center">
          <input
            type="checkbox"
            {...register('terms', { required: 'You must accept the terms and conditions' })}
            className="h-4 w-4 text-blue-600"
            disabled={isLoading}
          />
          <label className="ml-2 text-sm text-gray-600">
            I agree to the <a href="/terms" className="text-blue-600">Terms and Conditions</a>
          </label>
        </div>

        {/* Submit Button */}
        <Button 
          type="submit" 
          fullWidth
          rightIcon={<ArrowRight />}
          disabled={isLoading}
        >
          {isLoading ? 'Registering...' : 'Register'}
        </Button>
      </form>
    </div>
  );
}

export default RegisterPage;