import { useState, useEffect } from 'react';
import { apiRequest } from '../config/api';
import { UserPlus, Edit, Trash2, X, Filter, Search, ChevronLeft, ChevronRight } from 'lucide-react';
import { useNavigate } from 'react-router';

interface Rol {
  id: number;
  nombre: string;
  descripcion?: string;
  estado: boolean;
}

interface Usuario {
  id: number;
  email: string;
  nombre: string;
  apellido: string;
  rol_id: number;
  rol: Rol;
}

export function Usuarios() {
  const navigate = useNavigate();
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [roles, setRoles] = useState<Rol[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingUser, setEditingUser] = useState<Usuario | null>(null);
  const [currentUser, setCurrentUser] = useState<any>(null);
  
  // Filtros y Paginación
  const [search, setSearch] = useState('');
  const [selectedRol, setSelectedRol] = useState<string>('');
  const [page, setPage] = useState(0);
  const limit = 10;

  const [formData, setFormData] = useState({
    nombre: '',
    apellido: '',
    email: '',
    rol_id: '',
    password: '',
    confirmar_password: '',
  });

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (!token) {
      navigate('/login');
      return;
    }

    if (userData) {
      setCurrentUser(JSON.parse(userData));
    }

    loadRoles();
  }, [navigate]);

  useEffect(() => {
    loadUsuarios();
  }, [page, selectedRol]); // Recargar cuando cambie la página o el rol

  const loadUsuarios = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams({
        skip: (page * limit).toString(),
        limit: limit.toString(),
      });
      
      if (selectedRol) params.append('rol_id', selectedRol);
      if (search) params.append('search', search);

      const data = await apiRequest(`/api/v1/usuarios?${params.toString()}`);
      setUsuarios(data);
    } catch (error) {
      console.error('Error cargando usuarios:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadRoles = async () => {
    try {
      const data = await apiRequest('/api/v1/roles');
      setRoles(data);
    } catch (error) {
      console.error('Error cargando roles:', error);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(0); // Reiniciar a la primera página al buscar
    loadUsuarios();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!editingUser && formData.password !== formData.confirmar_password) {
      alert('Las contraseñas no coinciden');
      return;
    }

    try {
      const payload = {
        ...formData,
        rol_id: parseInt(formData.rol_id),
      };

      if (editingUser) {
        const updatePayload: any = { ...payload };
        if (!formData.password) {
          delete updatePayload.password;
          delete updatePayload.confirmar_password;
        }
        
        await apiRequest(`/api/v1/usuarios/${editingUser.id}`, {
          method: 'PUT',
          body: JSON.stringify(updatePayload),
        });
      } else {
        await apiRequest('/api/v1/usuarios', {
          method: 'POST',
          body: JSON.stringify(payload),
        });
      }
      loadUsuarios();
      closeModal();
    } catch (error) {
      console.error('Error guardando usuario:', error);
      alert('Error al guardar el usuario.');
    }
  };

  const handleDelete = async (id: number) => {
    if (currentUser?.id === id) {
      alert('No puedes eliminar tu propia cuenta.');
      return;
    }

    if (!confirm('¿Estás seguro de eliminar este usuario?')) return;

    try {
      await apiRequest(`/api/v1/usuarios/${id}`, {
        method: 'DELETE',
      });
      loadUsuarios();
    } catch (error) {
      console.error('Error eliminando usuario:', error);
      alert('Error al eliminar el usuario.');
    }
  };

  const openModal = (user?: Usuario) => {
    if (user) {
      setEditingUser(user);
      setFormData({
        nombre: user.nombre,
        apellido: user.apellido || '',
        email: user.email,
        rol_id: user.rol_id.toString(),
        password: '',
        confirmar_password: '',
      });
    } else {
      setEditingUser(null);
      setFormData({
        nombre: '',
        apellido: '',
        email: '',
        rol_id: roles.length > 0 ? roles[0].id.toString() : '',
        password: '',
        confirmar_password: '',
      });
    }
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setEditingUser(null);
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Gestión de Usuarios</h2>
          <p className="text-sm text-gray-500">Administra los accesos y roles del sistema</p>
        </div>
        {currentUser?.rol === 'admin' && (
          <button
            onClick={() => openModal()}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors shadow-sm"
          >
            <UserPlus className="w-5 h-5" />
            Nuevo Usuario
          </button>
        )}
      </div>

      {/* Barra de Filtros y Búsqueda */}
      <div className="mb-6 bg-white p-4 rounded-lg shadow-sm border border-gray-100 flex flex-wrap gap-4 items-end">
        <form onSubmit={handleSearch} className="flex-1 min-w-[200px]">
          <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Buscar</label>
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Nombre o email..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
            />
          </div>
        </form>

        <div className="w-48">
          <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Rol</label>
          <select
            value={selectedRol}
            onChange={(e) => { setSelectedRol(e.target.value); setPage(0); }}
            className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm bg-white"
          >
            <option value="">Todos los roles</option>
            {roles.map(rol => (
              <option key={rol.id} value={rol.id}>{rol.nombre}</option>
            ))}
          </select>
        </div>

        <button
          onClick={() => { setPage(0); loadUsuarios(); }}
          className="bg-gray-900 text-white px-6 py-2 rounded-lg hover:bg-gray-800 transition-colors text-sm font-medium"
        >
          Filtrar
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden relative">
        {loading && (
          <div className="absolute inset-0 bg-white/50 backdrop-blur-[1px] flex items-center justify-center z-10">
            <div className="text-gray-500 flex items-center gap-2">
              <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
              Cargando...
            </div>
          </div>
        )}

        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rol</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider text-right">Acciones</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {usuarios.map((usuario) => (
              <tr key={usuario.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap">
                   <div className="text-sm font-medium text-gray-900">{usuario.nombre} {usuario.apellido}</div>
                   <div className="text-xs text-gray-500">ID: {usuario.id}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{usuario.email}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    usuario.rol.nombre === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'
                  }`}>
                    {usuario.rol.nombre}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div className="flex justify-end gap-3">
                    {currentUser?.rol === 'admin' && (
                      <>
                        <button
                          onClick={() => openModal(usuario)}
                          className="text-blue-600 hover:text-blue-900"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        {currentUser?.id !== usuario.id && (
                          <button
                            onClick={() => handleDelete(usuario.id)}
                            className="text-red-600 hover:text-red-900"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        )}
                      </>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {!loading && usuarios.length === 0 && (
          <div className="p-8 text-center text-gray-500 italic">
            No se encontraron usuarios con estos criterios.
          </div>
        )}

        {/* Paginación */}
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-100 flex items-center justify-between">
          <div className="text-sm text-gray-600">
            Mostrando <span className="font-medium">{usuarios.length}</span> registros
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setPage(p => Math.max(0, p - 1))}
              disabled={page === 0 || loading}
              className="p-2 border border-gray-300 rounded-lg hover:bg-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <div className="flex items-center px-4 text-sm font-medium text-gray-700">
              Página {page + 1}
            </div>
            <button
              onClick={() => setPage(p => p + 1)}
              disabled={usuarios.length < limit || loading}
              className="p-2 border border-gray-300 rounded-lg hover:bg-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-lg overflow-hidden">
            <div className="flex justify-between items-center p-6 border-b border-gray-100">
              <h3 className="text-xl font-bold text-gray-900">
                {editingUser ? 'Actualizar Información' : 'Registrar Nuevo Usuario'}
              </h3>
              <button onClick={closeModal} className="text-gray-400 hover:text-gray-600 transition-colors">
                <X className="w-6 h-6" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-gray-700 uppercase mb-1">Nombre</label>
                  <input
                    type="text"
                    value={formData.nombre}
                    onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                    required
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-gray-700 uppercase mb-1">Apellido</label>
                  <input
                    type="text"
                    value={formData.apellido}
                    onChange={(e) => setFormData({ ...formData, apellido: e.target.value })}
                    required
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-gray-700 uppercase mb-1">Email / Usuario</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-gray-700 uppercase mb-1">Rol de Usuario</label>
                <select
                  value={formData.rol_id}
                  onChange={(e) => setFormData({ ...formData, rol_id: e.target.value })}
                  required
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm bg-white"
                >
                  <option value="" disabled>Selecciona un rol</option>
                  {roles.map(rol => (
                    <option key={rol.id} value={rol.id}>{rol.nombre}</option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-gray-700 uppercase mb-1">
                    {editingUser ? 'Nueva Contraseña' : 'Contraseña'}
                  </label>
                  <input
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    required={!editingUser}
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-gray-700 uppercase mb-1">Confirmar</label>
                  <input
                    type="password"
                    value={formData.confirmar_password}
                    onChange={(e) => setFormData({ ...formData, confirmar_password: e.target.value })}
                    required={!editingUser && formData.password !== ''}
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                  />
                </div>
              </div>

              <div className="flex gap-3 pt-6 border-t border-gray-50">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white py-2.5 rounded-lg hover:bg-blue-700 transition-colors font-medium text-sm shadow-sm"
                >
                  {editingUser ? 'Guardar Cambios' : 'Registrar Usuario'}
                </button>
                <button
                  type="button"
                  onClick={closeModal}
                  className="flex-1 bg-gray-100 text-gray-700 py-2.5 rounded-lg hover:bg-gray-200 transition-colors font-medium text-sm"
                >
                  Cerrar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}