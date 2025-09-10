import api from "../../api/axios";

export const fetchClients = async () => {
  const { data } = await api.get("/clients/clients/?skip=0&limit=100");
  return data;
};
