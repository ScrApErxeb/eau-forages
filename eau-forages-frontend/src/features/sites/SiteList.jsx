import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../../api/axios";
import { useState } from "react";
import SiteEditForm from "./SiteEditForm";
import "./SiteList.css";

export default function SiteList() {
  const queryClient = useQueryClient();
  const [editingSite, setEditingSite] = useState(null);

  const { data, isLoading, error } = useQuery({
    queryKey: ["sites"],
    queryFn: async () => {
      const { data } = await api.get("/sites/sites/?skip=0&limit=100");
      return data;
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async (id) => await api.delete(`/sites/sites/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["sites"] }),
  });

  if (isLoading) return <p>Chargement...</p>;
  if (error) return <p>Erreur : {error.message}</p>;

  return (
    <div className="site-list-container">
      <h2>Liste des Sites</h2>
      <table className="site-table">
        <thead>
          <tr>
            <th>Nom</th>
            <th>Localisation</th>
            <th>Actif</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data.map((site) => (
            <tr key={site.id}>
              <td>{site.nom}</td>
              <td>{site.localisation}</td>
              <td>{site.actif ? "Oui" : "Non"}</td>
              <td>
                <button onClick={() => setEditingSite(site)}>Éditer</button>
                <button onClick={() => deleteMutation.mutate(site.id)}>Supprimer</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {editingSite && (
        <SiteEditForm site={editingSite} onClose={() => setEditingSite(null)} />
      )}
    </div>
  );
}
