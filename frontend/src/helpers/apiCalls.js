import http from "./http-common";

export const logInCall = (credentials) => {
  info = {
    username: credentials.username,
    password: credentials.password,
  };
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

export const newMachineCall = async (inputs) => {
  const res = await fetch("http://localhost:5000/static/qr_320.png");
  console.log(res);
  const imageBlob = await res.blob();
  const imageObjectURL = URL.createObjectURL(imageBlob);
  return imageObjectURL;
};

export const runMachineCall = async (machineID) => {
  const res = http
    .post("/run-machine", { machine: machineID })
    .then((res) => true)
    .catch((error) => false);
};

export const getChargesData = async () => {
  const res = await http.get("/getCharges");
  return res.data;
};
