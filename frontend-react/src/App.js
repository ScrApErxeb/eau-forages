// src/App.js
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { UserProvider, useUser } from "./context/UserContext";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Logicien from "./pages/Logicien";
import Unauthorized from "./pages/Unauthorized";
import ProtectedRoute from "./routes/ProtectedRoute";
import Navbar from "./components/Navbar";

// Composant pour redirection depuis "/"
function HomeRedirect() {
  const { user } = useUser();
  if (user) return <Navigate to="/dashboard" />;
  return <Navigate to="/login" />;
}

function App() {
  return (
    <UserProvider>
      <Router>
        <Navbar /> {/* Menu visible uniquement si connecté */}
        <Routes>
          <Route path="/" element={<HomeRedirect />} />
          <Route path="/login" element={<Login />} />
          <Route path="/unauthorized" element={<Unauthorized />} />

          <Route
            path="/dashboard"
            element={
              <ProtectedRoute allowedRoles={["admin","patron","secretaire","technicien","client"]}>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/logicien"
            element={
              <ProtectedRoute allowedRoles={["admin","patron","secretaire"]}>
                <Logicien />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </UserProvider>
  );
}

export default App;
