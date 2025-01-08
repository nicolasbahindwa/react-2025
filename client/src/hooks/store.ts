import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';
import type { RootState, AppDispatch } from '@/store';

// These are perfect as they are
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

// Better thunk handling
export const useThunkDispatch = () => {
  const dispatch = useAppDispatch();
  return {
    dispatch,
    // This signature better matches how thunks work
    dispatchThunk: <ReturnType>(thunkAction: any) => {
      return dispatch(thunkAction) as Promise<ReturnType>;
    },
  };
};

// This is fine as is
export const useCommonSelectors = () => {
  const select = useAppSelector;
  
  return {
  
    // Auth selectors
    getUser: () => select((state) => state.auth.user),
    getAuthToken: () => select((state) => state.auth.token),
    
    // Common selectors
    getLoading: () => select((state) => state.common.loading),
    getErrorMessage: () => select((state) => state.common.errorMessage),
    
    // Posts selectors
    getPosts: () => select((state) => state.posts.all),
    getPostById: (id: number) => select((state) => state.posts.byId[id]),
    
    // Comments selectors
    getCommentsForPost: (postId: number) => select((state) => state.comments.byPostId[postId]),
    
    // Add any other common selectors here
 

  };
};