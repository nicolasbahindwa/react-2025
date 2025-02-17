import { useForm, SubmitHandler } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/shared/ui/Button';
import {Label} from '@/components/shared/ui/Label';
import { FormLogin } from './types';
import { useLoginMutation } from '@/features/Auth/services/actions/authActions';
import { useAppDispatch } from '@/store/hooks';
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
    <div className=" w-full md:w-lg lg:w-xl border-1 border-sm border-primary-500 rounded-lg"  >
      <div className=" flex  flex-column max-w-md mx-auto p-6 border-1 border-sm border-primary-500 rounded-lg">
        <h2 className="text-20 border-1 border-primary-500 font-semibold border-1 text-center   border-neutral-400">
          Login to Your Account
        </h2>

        {/* Display login error */}
        {loginError && (
          <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
            {loginError instanceof Error ? loginError.message : "Login failed"}
          </div>
        )}

        {/* Login form */}
        <form onSubmit={handleSubmit(onSubmit)} className=" mt-20 p-20 ">
          <LoginFormFields
            register={register}
            errors={errors}
            isLoading={isLoading}
          />
           
          <Button
            type="submit"
            // variant="secondary"
            fullWidth
            rightIcon={!isLoading ? <ArrowRight /> : null}
            isLoading={isLoading} // Make sure isLoading is passed correctly
            disabled={isLoading}
            variant="primary" // Specify the variant instead of using className
            className="rounded-md"
            
          >
            Login
          </Button>
           
          <p className=" " >
            Forgot your password? <Button variant="link" href="/forgot-password">Reset it</Button>
          </p>
          <p className="" >
            Don't have an account? <Button variant="link" href="/register">Register now</Button>
          </p>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;