export const filterContextReducer = (state, action) => {
  switch (action.type) {
    case "setLabels":
      return {
        ...state,
        labels: action.payload,
      };
    case "setFilters":
      return {
        ...state,
        filters: action.payload,
      };
    case "removeFilters":
      return {
        ...state,
        filters: null,
      };
    default:
      throw new Error();
  }
};

export const contextReducer = (state, action) => {
  switch (action.type) {
    case "login":
      localStorage.setItem("loggedIn", true);
      localStorage.setItem("username", action.payload);
      return {
        ...state,
        loggedIn: true,
        username: action.payload,
      };
    case "logout":
      localStorage.removeItem("loggedIn");
      localStorage.removeItem("username");
      return {
        ...state,
        loggedIn: false,
        username: "",
      };
    default:
      throw new Error();
  }
};
