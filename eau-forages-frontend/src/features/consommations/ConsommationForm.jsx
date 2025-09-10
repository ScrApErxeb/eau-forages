import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import api from "../../api/axios";
import "./ConsommationForm.css";

export default function ConsommationForm() {
  const queryClient = useQueryClient();
  const [abonneId, setAbonneId] = useState("");
  const [numeroRD, setNumeroRD] = useState("");
  const [moisAnnee, setMoisAnnee] = useState(() => {
    const now = new Date();
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;
  });
  const [volume, setVolume] = useState("");

  // Charger les abonnés
  const { data: abonnes } = useQuery({
    queryKey: ["abonnes"],
    queryFn: async () => (await api.get("/abonnes/abonnes/?skip=0&limit=100")).data,
  });

  // Mettre à jour le numéro RD quand l'abonné change
  const handleAbonneChange = (e) => {
    const selectedId = e.target.value;
    setAbonneId(selectedId);
    const abonne = abonnes.find(a => a.id === parseInt(selectedId));
    setNumeroRD(abonne?.numero_abonne || "");
  };

  const mutation = useMutation({
    mutationFn: async (newConso) =>
      (await api.post("/consommations/consommations/", newConso)).data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["consommations"] });
      setAbonneId("");
      setNumeroRD("");
      setMoisAnnee(() => {
        const now = new Date();
        return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;
      });
      setVolume("");
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate({
      abonne_id: parseInt(abonneId),
      numero_rd: numeroRD,
      mois_annee: moisAnnee,
      volume: parseFloat(volume),
      montant: 0,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="consommation-form">
      <select
        value={abonneId}
        onChange={handleAbonneChange}
        required
      >
        <option value="">Sélectionner Abonné</option>
        {abonnes?.map((a) => (
          <option key={a.id} value={a.id}>{a.nom} {a.prenom}</option>
        ))}
      </select>

      <input
        type="text"
        value={numeroRD}
        onChange={(e) => setNumeroRD(e.target.value)}
        required
        placeholder="Numéro RD"
      />

      <input
        type="month"
        value={moisAnnee}
        onChange={(e) => setMoisAnnee(e.target.value)}
        required
      />

      <input
        type="number"
        placeholder="Volume consommé"
        value={volume}
        onChange={(e) => setVolume(e.target.value)}
        required
        min="0"
      />

      <button type="submit">Enregistrer</button>

      {mutation.isLoading && <span>Envoi…</span>}
      {mutation.isError && <span style={{ color: "red" }}>Erreur : {mutation.error.message}</span>}
      {mutation.isSuccess && <span style={{ color: "green" }}>Consommation ajoutée ✅</span>}
    </form>
  );
}
