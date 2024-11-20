import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api", // Django REST Framework의 기본 URL
});

export default api;
