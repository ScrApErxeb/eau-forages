import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../../api/axios";
import "./SiteForm.css";

export default function SiteForm() {
  const queryClient = useQueryClient();
  const [nom, setNom] = useState("");
  const [localisation, setLocalisation] = useState("");
  const [actif, setActif] = useState(true);

  const mutation = useMutation({
    mutationFn: async (newSite) => {
      const { data } = await api.post("/sites/sites/", newSite);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["sites"] });
      setNom(""); setLocalisation(""); setActif(true);
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate({ nom, localisation, actif });
  };

  return (
    <form onSubmit={handleSubmit} className="site-form">
      <input placeholder="Nom du site" value={nom} onChange={(e) => setNom(e.target.value)} required />
      <input placeholder="Localisation" value={localisation} onChange={(e) => setLocalisation(e.target.value)} />
      <label>
        Actif:
        <input type="checkbox" checked={actif} onChange={(e) => setActif(e.target.checked)} />
      </label>
      <button type="submit">Ajouter</button>
      {mutation.isLoading && <span>Envoi…</span>}
      {mutation.isError && <span style={{ color: "red" }}>Erreur : {mutation.error.message}</span>}
      {mutation.isSuccess && <span style={{ color: "green" }}>Site ajouté ! ✅</span>}
    </form>
  );
}
