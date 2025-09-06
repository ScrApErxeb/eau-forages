export default function Unauthorized() {
  return (
    <div className="container mt-5">
      <div className="alert alert-danger" role="alert">
        <h4 className="alert-heading">Accès refusé</h4>
        <p>Vous n'avez pas les droits pour accéder à cette page.</p>
      </div>
    </div>
  );
}
