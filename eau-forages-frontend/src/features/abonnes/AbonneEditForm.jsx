import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../../api/axios";
import "./AbonneEditForm.css"

export default function AbonneEditForm({ abonne, onClose }) {
  const queryClient = useQueryClient();
  const [nom, setNom] = useState(abonne.nom);
  const [prenom, setPrenom] = useState(abonne.prenom);
  const [numCnib, setNumCnib] = useState(abonne.num_cnib);
  const [numeroAbonne, setNumeroAbonne] = useState(abonne.numero_abonne);
  const [tel, setTel] = useState(abonne.tel);

  const mutation = useMutation({
    mutationFn: async (updatedAbonne) => {
      const { data } = await api.put(`/abonnes/abonnes/${abonne.id}`, updatedAbonne);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["abonnes"] });
      onClose();
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate({ nom, prenom, num_cnib: numCnib, numero_abonne: numeroAbonne, tel });
  };

  return (
    <form onSubmit={handleSubmit} className="abonne-form">
      <input value={nom} onChange={(e) => setNom(e.target.value)} required />
      <input value={prenom} onChange={(e) => setPrenom(e.target.value)} required />
      <input value={numCnib} onChange={(e) => setNumCnib(e.target.value)} required />
      <input value={numeroAbonne} onChange={(e) => setNumeroAbonne(e.target.value)} required />
      <input value={tel} onChange={(e) => setTel(e.target.value)} required />
      <button type="submit">Enregistrer</button>
      <button type="button" onClick={onClose} style={{ marginLeft: "0.5rem" }}>Annuler</button>
    </form>
  );
}
