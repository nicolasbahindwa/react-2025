import { useSelector } from 'react-redux';
import { RootState } from '@/store';

export const useAuth = () => {
  const auth = useSelector((state: RootState) => state.auth);
  
  return {
    user: auth.user,
    isAuthenticated: auth.isAuthenticated,
    loading: auth.loading,
    error: auth.error,
  };
};