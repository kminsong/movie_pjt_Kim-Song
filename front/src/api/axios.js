import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api", // Django REST Framework의 기본 URL
});

// 요청 인터셉터 추가: 모든 요청에 Authorization 헤더 추가
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("authToken");
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default api;
