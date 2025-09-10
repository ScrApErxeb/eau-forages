import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../../api/axios";
import "./AbonneForm.css";



export default function AbonneForm() {
  const queryClient = useQueryClient();
  const [nom, setNom] = useState("");
  const [prenom, setPrenom] = useState("");
  const [numCnib, setNumCnib] = useState("");
  const [numeroAbonne, setNumeroAbonne] = useState("");
  const [tel, setTel] = useState("");

  const mutation = useMutation({
    mutationFn: async (newAbonne) => {
      const { data } = await api.post("/abonnes/abonnes/", newAbonne);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["abonnes"] });
      setNom(""); setPrenom(""); setNumCnib(""); setNumeroAbonne(""); setTel("");
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate({ nom, prenom, num_cnib: numCnib, numero_abonne: numeroAbonne, tel });
  };

  return (
    <form onSubmit={handleSubmit} className="abonne-form">
  <input placeholder="Nom" value={nom} onChange={(e) => setNom(e.target.value)} required />
  <input placeholder="Prénom" value={prenom} onChange={(e) => setPrenom(e.target.value)} required />
  <input placeholder="Num CNIB" value={numCnib} onChange={(e) => setNumCnib(e.target.value)} required />
  <input placeholder="Numéro Abonné" value={numeroAbonne} onChange={(e) => setNumeroAbonne(e.target.value)} required />
  <input placeholder="Téléphone" value={tel} onChange={(e) => setTel(e.target.value)} required />
  <button type="submit">Ajouter</button>
</form>
  );
}
