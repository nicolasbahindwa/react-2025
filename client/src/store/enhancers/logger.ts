import { StoreEnhancer } from 'redux';

const loggerEnhancer: StoreEnhancer =
  (createStore) => (reducer, initialState) => {
    const store = createStore(reducer, initialState);

    return {
      ...store,
      dispatch: (action: any) => {
        console.group(action.type);
        console.info('dispatching', action);
        const result = store.dispatch(action);
        console.log('next state', store.getState());
        console.groupEnd();
        return result;
      },
    };
  };

export default loggerEnhancer;