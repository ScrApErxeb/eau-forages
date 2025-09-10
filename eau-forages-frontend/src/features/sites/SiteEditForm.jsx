import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../../api/axios";
import "./SiteEditForm.css";

export default function SiteEditForm({ site, onClose }) {
  const queryClient = useQueryClient();
  const [nom, setNom] = useState(site.nom);
  const [localisation, setLocalisation] = useState(site.localisation);
  const [actif, setActif] = useState(site.actif);

  const mutation = useMutation({
    mutationFn: async (updatedSite) => {
      const { data } = await api.put(`/sites/sites/${site.id}`, updatedSite);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["sites"] });
      onClose();
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate({ nom, localisation, actif });
  };

  return (
    <form onSubmit={handleSubmit} className="site-edit-form">
      <input value={nom} onChange={(e) => setNom(e.target.value)} required />
      <input value={localisation} onChange={(e) => setLocalisation(e.target.value)} />
      <label>
        Actif:
        <input type="checkbox" checked={actif} onChange={(e) => setActif(e.target.checked)} />
      </label>
      <button type="submit">Enregistrer</button>
      <button type="button" onClick={onClose} style={{ marginLeft: "0.5rem" }}>Annuler</button>
    </form>
  );
}
