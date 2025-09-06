import { useUser } from "../context/UserContext";

export default function Dashboard() {
  const { user } = useUser();

  return (
    <div className="container mt-5">
      <div className="card">
        <div className="card-body">
          <h2 className="card-title">Bienvenue {user?.nom}</h2>
          <p className="card-text">Rôle : {user?.role}</p>
        </div>
      </div>
    </div>
  );
}
