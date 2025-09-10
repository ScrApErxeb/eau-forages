import axios from "axios";

// Création d'une instance Axios configurée
const api = axios.create({
  baseURL: "http://localhost:8000", // URL de ton backend FastAPI
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
