import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../../api/axios";
import "./ConsommationList.css";

export default function ConsommationList() {
  const queryClient = useQueryClient();

  const { data, isLoading, error } = useQuery({
    queryKey: ["consommations"],
    queryFn: async () => (await api.get("/consommations/consommations/?skip=0&limit=100")).data,
  });

  const deleteMutation = useMutation({
    mutationFn: async (id) => await api.delete(`/consommations/consommations/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["consommations"] }),
  });

  if (isLoading) return <p>Chargement...</p>;
  if (error) return <p>Erreur : {error.message}</p>;

  return (
    <div className="consommation-list-container">
      <h2>Liste des Consommations</h2>
      <table className="consommation-table">
        <thead>
          <tr>
            <th>Abonné</th>
            <th>Numéro Abonné</th>
            <th>Volume</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data.map((c) => (
            <tr key={c.id}>
              <td>{c.abonne?.nom} {c.abonne?.prenom}</td>
              <td>{c.abonne?.numero_abonne}</td>
              <td>{c.volume}</td>
              <td>{new Date(c.date_consommation).toLocaleString()}</td>
              <td>
                <button onClick={() => deleteMutation.mutate(c.id)}>Supprimer</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
