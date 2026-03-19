import { createBrowserRouter } from "react-router";
import { Login } from "./pages/Login";
import { Dashboard } from "./pages/Dashboard";
import { Usuarios } from "./pages/Usuarios";
import { Facturas } from "./pages/Facturas";

export const router = createBrowserRouter([
  {
    path: "/login",
    Component: Login,
  },
  {
    path: "/",
    Component: Dashboard,
    children: [
      { index: true, element: <div className="p-6 text-gray-500">Selecciona una opción del menú</div> },
      { path: "usuarios", Component: Usuarios },
      { path: "facturas", Component: Facturas },
    ],
  },
]);
