import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../../api/axios";
import { useState } from "react";
import AbonneEditForm from "./AbonneEditForm";
import "./AbonneList.css";

export default function AbonneList() {
  const queryClient = useQueryClient();
  const [editingAbonne, setEditingAbonne] = useState(null);

  // --- Fetch abonnés ---
  const { data, isLoading, error } = useQuery({
    queryKey: ["abonnes"],
    queryFn: async () => {
      const { data } = await api.get("/abonnes/abonnes/?skip=0&limit=100");
      return data;
    },
  });

  // --- Mutation suppression ---
  const deleteMutation = useMutation({
    mutationFn: async (id) => {
      await api.delete(`/abonnes/abonnes/${id}`);
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["abonnes"] }),
  });

  const handleDelete = (id) => {
    if (window.confirm("Voulez-vous vraiment supprimer cet abonné ?")) {
      deleteMutation.mutate(id);
    }
  };

  if (isLoading) return <p>Chargement...</p>;
  if (error) return <p>Erreur : {error.message}</p>;

  return (
    <div className="abonne-list-container">
      <h2>Liste des Abonnés</h2>
      <table className="abonne-table">
        <thead>
          <tr>
            <th>Nom</th>
            <th>Prénom</th>
            <th>Num Abonné</th>
            <th>Téléphone</th>
            <th>Num CNIB</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data.map((abonne) => (
            <tr key={abonne.id}>
              <td>{abonne.nom}</td>
              <td>{abonne.prenom}</td>
              <td>{abonne.numero_abonne}</td>
              <td>{abonne.tel}</td>
              <td>{abonne.num_cnib}</td>
              <td>
                <button onClick={() => handleDelete(abonne.id)} disabled={deleteMutation.isLoading}>
                  {deleteMutation.isLoading ? "Suppression..." : "Supprimer"}
                </button>
                <button onClick={() => setEditingAbonne(abonne)}>Éditer</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {editingAbonne && (
        <div style={{ marginTop: "1rem" }}>
          <h3>Éditer Abonné</h3>
          <AbonneEditForm abonne={editingAbonne} onClose={() => setEditingAbonne(null)} />
        </div>
      )}
    </div>
  );
}
