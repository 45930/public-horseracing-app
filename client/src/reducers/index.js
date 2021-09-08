import { combineReducers } from "redux";

import backendReducer from "./backendReducer";

export default combineReducers({
  backend: backendReducer,
});
