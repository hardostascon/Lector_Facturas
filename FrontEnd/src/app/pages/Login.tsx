import { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router';
import { apiRequest, USE_MOCK_DATA } from '../config/api';
import { LogIn } from 'lucide-react';

export function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {

      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const data = await apiRequest('/api/v1/auth/login', {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify({
        id: data.user_id,
        nombre_usuario: data.nombre_usuario,
        rol: data.rol
      }));
      
      navigate('/');
      /*if (USE_MOCK_DATA) {
        // Modo desarrollo: simular login exitoso
        // Usuarios de prueba: admin/admin o demo/demo
        if ((username === 'admin' && password === 'admin') || 
            (username === 'demo' && password === 'demo')) {
          const mockData = {
            access_token: 'mock_token_12345',
            user: {
              id: 1,
              username: username,
              name: username === 'admin' ? 'Administrador' : 'Usuario Demo',
              email: `${username}@example.com`,
            }
          };
          
          localStorage.setItem('token', mockData.access_token);
          localStorage.setItem('user', JSON.stringify(mockData.user));
          navigate('/');
        } else {
          throw new Error('Credenciales incorrectas');
        }
      } else {
        // Endpoint de ejemplo - ajusta según tu API de FastAPI
        // Ejemplo: POST /api/auth/login con body { username, password }
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const data = await apiRequest('/api/v1/auth/login', {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

        // Guarda el token en localStorage
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        // Redirige al dashboard
        navigate('/');
      }*/
    } catch (err) {
      setError('Credenciales incorrectas. Por favor, intenta de nuevo.');
      console.error('Error de login:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
        <div className="flex flex-col items-center mb-8">
          <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mb-4">
            <LogIn className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">Iniciar Sesión</h1>
          <p className="text-gray-600 mt-2">Accede a tu cuenta</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
              Usuario
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
              placeholder="Ingresa tu usuario"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
              Contraseña
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
              placeholder="Ingresa tu contraseña"
            />
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-blue-400 disabled:cursor-not-allowed font-medium"
          >
            {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
          </button>
        </form>

        
      </div>
    </div>
  );
}