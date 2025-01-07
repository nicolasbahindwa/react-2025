import React from 'react'
import { useForm, SubmitHandler } from 'react-hook-form'
import { TextField } from '@/components/shared/ui/TextField'
import { Button } from '@/components/shared/ui/Button'
import { FormLogin } from './types'
import { ArrowRight, Download } from 'lucide-react'

function LoginPage() {
  // Move the form hooks to the main component
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormLogin>()

  const onSubmit: SubmitHandler<FormLogin> = (data) => {
    console.log("Form Submitted:", data)
  }

  return (
    <div>
      <form onSubmit={handleSubmit(onSubmit)} className='space-y-6'>
        <TextField
          label="Email"
          type="email"
          {...register('email', { required: 'Email is required' })}
          error={errors.email?.message}
          placeholder='Enter a valid email address'
        />

        <TextField
          label="Password"
          type="password"
          {...register('password', { required: 'Password is required' })}
          error={errors.password?.message}
          placeholder='Enter your password'
        />

        {/* Submit button - typically you only need one button for a login form */}
        <Button 
          type="submit" 
          fullWidth
          rightIcon={<ArrowRight />}
        >
          Login
        </Button>
      </form>
      
    </div>
  )
}

export default LoginPage