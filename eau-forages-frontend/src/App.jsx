import { useState } from "react";
import AbonneForm from "./features/abonnes/AbonneForm";
import AbonneList from "./features/abonnes/AbonneList";
import SiteForm from "./features/sites/SiteForm";
import SiteList from "./features/sites/SiteList";
import ConsommationForm from "./features/consommations/ConsommationForm";
import ConsommationList from "./features/consommations/ConsommationList";



function App() {
  const [view, setView] = useState("abonnes");

  return (
    <div className="App">
      <h1>Gestion Eau Forages</h1>

      <nav>
        <button onClick={() => setView("abonnes")}>Abonnés</button>
        <button onClick={() => setView("sites")}>Sites</button>
        <button onClick={() => setView("consommations")}>Consommations</button>
      </nav>

      {view === "abonnes" && (
        <section>
          <h2>Abonnés</h2>
          <AbonneForm />
          <AbonneList />
        </section>
      )}

      {view === "sites" && (
        <section>
          <h2>Sites</h2>
          <SiteForm />
          <SiteList />
        </section>
      )}

        {view === "consommations" && (
          <section>
          <h2>Consommations</h2>
          <ConsommationForm />
          <ConsommationList />
        </section>
        )}
    </div>
  );
}

export default App;
