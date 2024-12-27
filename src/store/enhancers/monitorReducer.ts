import { StoreEnhancer } from 'redux';

const round = (number: number) => Math.round(number * 100) / 100;

const monitorReducerEnhancer: StoreEnhancer =
  (createStore) => (reducer, initialState) => {
    const monitoredReducer = (state: any, action: any) => {
      const start = performance.now();
      const newState = reducer(state, action);
      const end = performance.now();
      const diff = round(end - start);

      console.log('reducer process time:', diff);

      return newState;
    };

    return createStore(monitoredReducer, initialState);
  };

export default monitorReducerEnhancer;