import React from "react";
import { Link } from "react-router-dom";
import { useUser } from "../context/UserContext";

export default function Navbar() {
  const { user, logout } = useUser();

  if (!user) return null; // Pas de menu si pas connecté

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
      <div className="container">
        <Link className="navbar-brand" to="/dashboard">Eau Forages</Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto">
            <li className="nav-item">
              <Link className="nav-link" to="/dashboard">Dashboard</Link>
            </li>

            {/* Menu Logicien visible uniquement pour admin/patron/secretaire */}
            {["admin", "patron", "secretaire"].includes(user.role) && (
              <li className="nav-item">
                <Link className="nav-link" to="/logicien">Logicien</Link>
              </li>
            )}
          </ul>

          <span className="navbar-text me-3">
            {user.nom} ({user.role})
          </span>
          <button className="btn btn-outline-light" onClick={logout}>Logout</button>
        </div>
      </div>
    </nav>
  );
}
