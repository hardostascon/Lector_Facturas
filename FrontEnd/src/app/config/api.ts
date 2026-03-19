// Configuración de la API FastAPI
// Cambia esta URL por la de tu servidor FastAPI
export const API_BASE_URL = 'http://localhost:8000';

// Modo desarrollo: usa datos mock en lugar de hacer peticiones reales
// Cambia a false cuando tu API de FastAPI esté lista
export const USE_MOCK_DATA = false;

// Helper para hacer peticiones a la API
export async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const token = localStorage.getItem('token');

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    if (response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

// Helper para subir archivos
export async function uploadFile(endpoint: string, file: File) {
  const token = localStorage.getItem('token');
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'POST',
    headers: {
      ...(token && { 'Authorization': `Bearer ${token}` }),
    },
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}