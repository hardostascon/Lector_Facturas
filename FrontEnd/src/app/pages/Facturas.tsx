import { useState, useEffect } from 'react';
import { apiRequest, uploadFile } from '../config/api';
import { Trash2, X, Upload, Eye, Search, ChevronLeft, ChevronRight, Filter } from 'lucide-react';
import { useNavigate } from 'react-router';

interface DetalleFactura {
  id: number;
  descripcion: string;
  cantidad: number;
  precio_unitario: number;
  impuesto: number;
}

interface Factura {
  id: number;
  archivo: string | null;
  facturador: string | null;
  factura_numero: string;
  factura_fecha: string;
  factura_monto: number;
  factura_moneda: string;
  factura_status: string;
  factura_fcreacion: string;
  factura_estado: boolean;
  detalle: DetalleFactura[];
}

export function Facturas() {
  const navigate = useNavigate();
  const [facturas, setFacturas] = useState<Factura[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [selectedFactura, setSelectedFactura] = useState<Factura | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  
  // Paginación y Búsqueda
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(0);
  const limit = 10;

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }
    loadFacturas();
  }, [navigate, page]);

  const loadFacturas = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams({
        skip: (page * limit).toString(),
        limit: limit.toString(),
      });
      if (search) params.append('search', search);

      const data = await apiRequest(`/api/v1/facturas?${params.toString()}`);
      setFacturas(data);
    } catch (error) {
      console.error('Error cargando facturas:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(0);
    loadFacturas();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const validTypes = ['application/pdf', 'image/jpeg', 'image/jpg'];
      if (!validTypes.includes(file.type)) {
        alert('Solo se permiten archivos PDF o JPG');
        return;
      }
      setSelectedFile(file);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;

    setUploading(true);
    try {
      await uploadFile('/api/v1/facturas/upload', selectedFile);
      setPage(0);
      loadFacturas();
      alert('Factura procesada exitosamente');
      closeModal();
    } catch (error) {
      console.error('Error procesando factura:', error);
      alert('Error al procesar la factura.');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('¿Estás seguro de eliminar esta factura?')) return;
    try {
      await apiRequest(`/api/v1/facturas/${id}`, { method: 'DELETE' });
      loadFacturas();
    } catch (error) {
      console.error('Error eliminando factura:', error);
    }
  };

  const downloadFile = (factura: Factura) => {
    if (factura.archivo) {
      window.open(factura.archivo, '_blank');
    }
  };

  const openDetails = (factura: Factura) => {
    setSelectedFactura(factura);
    setShowDetailModal(true);
  };

  const openModal = () => setShowModal(true);
  const closeModal = () => {
    setShowModal(false);
    setSelectedFile(null);
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Gestión de Facturas</h2>
          <p className="text-sm text-gray-500">Visualiza y procesa tus documentos comerciales</p>
        </div>
        <button
          onClick={openModal}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors shadow-sm"
        >
          <Upload className="w-5 h-5" />
          Cargar Factura
        </button>
      </div>

      {/* Buscador */}
      <div className="mb-6 bg-white p-4 rounded-lg shadow-sm border border-gray-100 flex gap-4">
        <form onSubmit={handleSearch} className="flex-1 relative">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Buscar por número o facturador..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
          />
        </form>
        <button
          onClick={() => { setPage(0); loadFacturas(); }}
          className="bg-gray-900 text-white px-6 py-2 rounded-lg hover:bg-gray-800 transition-colors text-sm font-medium"
        >
          Filtrar
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden relative">
        {loading && (
          <div className="absolute inset-0 bg-white/50 backdrop-blur-[1px] flex items-center justify-center z-10">
            <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          </div>
        )}

        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Número</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Facturador</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Monto</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {facturas.length === 0 && !loading ? (
              <tr>
                <td colSpan={6} className="px-6 py-8 text-center text-gray-500 italic">
                  No se encontraron facturas.
                </td>
              </tr>
            ) : (
              facturas.map((factura) => (
                <tr key={factura.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">{factura.factura_numero}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{factura.facturador || '-'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {factura.factura_fecha ? new Date(factura.factura_fecha).toLocaleDateString('es-ES') : '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    ${factura.factura_monto?.toFixed(2)} <span className="text-xs text-gray-400">{factura.factura_moneda}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                      factura.factura_status === 'pagada' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {factura.factura_status || 'pendiente'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                    <div className="flex justify-end gap-3">
                      <button onClick={() => openDetails(factura)} className="text-gray-600 hover:text-blue-600" title="Ver Detalle">
                        <Search className="w-4 h-4" />
                      </button>
                      {factura.archivo && (
                        <button onClick={() => downloadFile(factura)} className="text-blue-600 hover:text-blue-900" title="Ver PDF">
                          <Eye className="w-4 h-4" />
                        </button>
                      )}
                      <button onClick={() => handleDelete(factura.id)} className="text-red-600 hover:text-red-900" title="Eliminar">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>

        {/* Paginación */}
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-100 flex items-center justify-between">
          <div className="text-sm text-gray-600">
            Mostrando <span className="font-medium">{facturas.length}</span> registros
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setPage(p => Math.max(0, p - 1))}
              disabled={page === 0 || loading}
              className="p-2 border border-gray-300 rounded-lg hover:bg-white disabled:opacity-50 transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <div className="flex items-center px-4 text-sm font-medium">Página {page + 1}</div>
            <button
              onClick={() => setPage(p => p + 1)}
              disabled={facturas.length < limit || loading}
              className="p-2 border border-gray-300 rounded-lg hover:bg-white disabled:opacity-50 transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Modal Carga */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-200">
            <div className="flex justify-between items-center p-6 border-b border-gray-100">
              <h3 className="text-xl font-bold text-gray-900">Cargar Factura</h3>
              <button onClick={closeModal} className="text-gray-400 hover:text-gray-600">
                <X className="w-6 h-6" />
              </button>
            </div>

            <form onSubmit={handleUpload} className="p-6 space-y-4">
              <div className="border-2 border-dashed border-gray-200 rounded-xl p-8 text-center hover:border-blue-500 transition-colors group">
                <input type="file" accept=".pdf,.jpg,.jpeg" onChange={handleFileChange} className="hidden" id="file-upload" required />
                <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center">
                  <Upload className="w-12 h-12 text-gray-300 group-hover:text-blue-500 mb-3 transition-colors" />
                  {selectedFile ? (
                    <span className="text-sm font-medium text-gray-900">{selectedFile.name}</span>
                  ) : (
                    <>
                      <span className="text-sm text-gray-600">Click para seleccionar archivo</span>
                      <p className="text-xs text-gray-400 mt-1">PDF o JPG (máx. 10MB)</p>
                    </>
                  )}
                </label>
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  disabled={uploading || !selectedFile}
                  className="flex-1 bg-blue-600 text-white py-2.5 rounded-lg hover:bg-blue-700 disabled:bg-blue-400 transition-colors font-medium"
                >
                  {uploading ? 'Procesando...' : 'Iniciar Carga'}
                </button>
                <button
                  type="button"
                  onClick={closeModal}
                  className="flex-1 bg-gray-100 text-gray-700 py-2.5 rounded-lg hover:bg-gray-200 transition-colors font-medium"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Detalle Items */}
      {showDetailModal && selectedFactura && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-2xl overflow-hidden animate-in fade-in zoom-in duration-200">
            <div className="flex justify-between items-center p-6 border-b border-gray-100 bg-gray-50">
              <div>
                <h3 className="text-lg font-bold text-gray-900">Detalle de Factura: {selectedFactura.factura_numero}</h3>
                <p className="text-sm text-gray-500">{selectedFactura.facturador}</p>
              </div>
              <button onClick={() => setShowDetailModal(false)} className="text-gray-400 hover:text-gray-600">
                <X className="w-6 h-6" />
              </button>
            </div>

            <div className="p-6 max-h-[60vh] overflow-y-auto">
              {selectedFactura.detalle && selectedFactura.detalle.length > 0 ? (
                <table className="min-w-full divide-y divide-gray-200 border rounded-lg overflow-hidden">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase">Descripción</th>
                      <th className="px-4 py-2 text-center text-xs font-semibold text-gray-600 uppercase">Cant.</th>
                      <th className="px-4 py-2 text-right text-xs font-semibold text-gray-600 uppercase">Precio Unit.</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {selectedFactura.detalle.map((item) => (
                      <tr key={item.id} className="hover:bg-gray-50">
                        <td className="px-4 py-3 text-sm text-gray-800">{item.descripcion}</td>
                        <td className="px-4 py-3 text-sm text-gray-600 text-center">{item.cantidad}</td>
                        <td className="px-4 py-3 text-sm text-gray-900 text-right font-medium">${item.precio_unitario.toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                  <tfoot className="bg-gray-50">
                    <tr>
                      <td colSpan={2} className="px-4 py-2 text-right text-sm font-bold text-gray-900">Total Detectado:</td>
                      <td className="px-4 py-2 text-right text-sm font-bold text-blue-600">
                        ${selectedFactura.detalle.reduce((acc, curr) => acc + (curr.precio_unitario * curr.cantidad), 0).toFixed(2)}
                      </td>
                    </tr>
                  </tfoot>
                </table>
              ) : (
                <div className="text-center py-10">
                  <Filter className="w-10 h-10 text-gray-200 mx-auto mb-3" />
                  <p className="text-gray-500">No se extrajeron ítems detallados para esta factura.</p>
                </div>
              )}
            </div>

            <div className="p-4 bg-gray-50 text-right border-t border-gray-100">
              <button
                onClick={() => setShowDetailModal(false)}
                className="bg-gray-900 text-white px-6 py-2 rounded-lg hover:bg-gray-800 transition-colors text-sm font-medium"
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}