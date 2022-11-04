import http from "./http-common";

export const logInCall = (credentials) => {
  const res = http
    .post("/login", credentials)
    .then((res) => true)
    .catch((error) => false);
  return res;
};

export const logOutCall = () => {
  const res = http
    .get("/logout")
    .then((res) => true)
    .catch((error) => false);
  return res;
};

export const getChargesData = async () => {
  const res = await http.get("/getCharges");
  return res.data;
};
