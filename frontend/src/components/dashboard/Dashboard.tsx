import { useEffect, useState } from "react";
import "./Dashboard.css";
import "./sidebar/Sidebar.css";
import ChatTemplate from "./ChatTemplate";
import Sidebar from "./sidebar/Sidebar";
import ChatWindow from "./chat/ChatWindow";
import type { Conversation } from "../../types/conversation";
type DashboardProps = { token: string };

export default function Dashboard({ token }: DashboardProps) {
  const [url, setUrl] = useState("");
  const [jobId, setJobId] = useState<string | null>(null);
  const [result, setResult] = useState<unknown>(null);
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversation, setActiveConversation] =
    useState<Conversation | null>(null);

  async function getJobStatus() {
    if (!jobId || busy) return;
    setBusy(true);
    setError("");
    try {
      const response = await fetch(
        `http://localhost:8000/documents/jobs/${jobId}`,
      );
      if (!response.ok)
        throw new Error(
          "Der Status konnte nicht geladen werden. Versuche es erneut.",
        );
      const data: { status: string; result: unknown } = await response.json();
      setStatus(data.status);
      if (data.status === "finished") setResult(data.result);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Der Server ist nicht erreichbar.",
      );
    } finally {
      setBusy(false);
    }
  }

  async function handleUrlImport() {
    if (busy) return;
    setBusy(true);
    setError("");
    try {
      const response = await fetch("http://localhost:8000/documents/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: url.trim() }),
      });
      if (!response.ok)
        throw new Error(
          "Der Import konnte nicht gestartet werden. Prüfe den Link und die Freigabe deiner Tabelle.",
        );
      const data: { job_id: string; status: string } = await response.json();
      if (!data.job_id)
        throw new Error("Der Server hat keine Import-ID zurückgegeben.");
      setJobId(data.job_id);
      setStatus(data.status);
      setResult(null);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Der Server ist nicht erreichbar.",
      );
    } finally {
      setBusy(false);
    }
  }

  async function loadConversations(token: string) {
    try {
      const response = await fetch("http://localhost:8000/conversations/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data: Conversation[] = await response.json();
      setConversations(data);
    } catch (error) {
      alert("Error occured while fetching conversations: " + error);
    }
  }

  const statusLabel =
    status === "finished"
      ? "Abgeschlossen"
      : ["failed", "stopped", "canceled"].includes(status)
        ? "Nicht abgeschlossen"
        : status === "started"
          ? "Wird analysiert"
          : "In der Warteschlange";

  useEffect(() => {
    void loadConversations(token);
  }, [token]);

  return (
    <div className="np-dashboard">
      <Sidebar conversations={conversations}></Sidebar>
      <ChatWindow />
      {/* <header className="np-header">
        <a className="np-brand" href="#dashboard">
          <span className="np-logo" aria-hidden="true">
            ϟ
          </span>
          <span>
            NutriPulse <small>AI</small>
          </span>
        </a>
        <span className="np-header-label">Dein Ernährungsworkspace</span>
        <span className="np-account">
          <i /> Angemeldet
        </span>
      </header>
      <main id="dashboard" className="np-main">
        <div className="np-intro">
          <span className="np-eyebrow">DEIN DASHBOARD</span>
          <h1>
            Gute Ernährung beginnt
            <br />
            mit einem <span>klaren Überblick.</span>
          </h1>
          <p>
            Bringe deine Ernährungsdaten an einen Ort.
            <br />
            Den nächsten Schritt übernimmt die KI.
          </p>
        </div>
        <div className="np-grid">
          <section
            className="np-card np-import"
            aria-labelledby="import-heading"
          >
            <div className="np-card-top">
              <span className="np-icon" aria-hidden="true">
                ↗
              </span>
              <span className="np-badge">GOOGLE SHEETS</span>
            </div>
            <h2 id="import-heading">Deine Daten. Neue Einblicke.</h2>
            <p>
              Importiere deine Tabelle und lass NutriPulse deine Ernährungsdaten
              aufbereiten.
            </p>
            <form
              onSubmit={(event) => {
                event.preventDefault();
                void handleUrlImport();
              }}
            >
              <label htmlFor="import-url">Link zu deiner Tabelle</label>
              <input
                id="import-url"
                type="url"
                placeholder="https://docs.google.com/spreadsheets/…"
                value={url}
                onChange={(event) => setUrl(event.target.value)}
                required
                disabled={busy}
              />
              <p className="np-hint">
                Deine Tabelle muss für den Zugriff freigegeben sein.
              </p>
              <button
                className="np-primary"
                type="submit"
                disabled={busy || !url.trim()}
              >
                {busy ? "Bitte warten …" : "Tabelle importieren"}
                <span aria-hidden="true">→</span>
              </button>
            </form>
            {error && (
              <p className="np-error" role="alert">
                {error}
              </p>
            )}
            <div className="np-import-footer">
              <span aria-hidden="true">✧</span> KI-gestützte Aufbereitung deiner
              Daten
            </div>
          </section>
          <ChatTemplate token={token} />
        </div>
        <section
          className="np-card np-documents"
          aria-labelledby="documents-heading"
        >
          <h2 id="documents-heading">Aktueller Import</h2>
          <p>Status und Ergebnis deines letzten Imports in dieser Sitzung.</p>
          {!jobId ? (
            <div className="np-empty">
              <span className="np-empty-icon" aria-hidden="true">
                ≡
              </span>
              <h3>Platz für deinen ersten Einblick</h3>
              <p>Füge oben einen Tabellen-Link ein, um loszulegen.</p>
              <a href="#import-url">
                Erste Tabelle importieren <span aria-hidden="true">→</span>
              </a>
            </div>
          ) : (
            <div className="np-job">
              <div className="np-job-row">
                <div aria-live="polite">
                  <span className="np-badge">{statusLabel}</span>
                  <p className="np-job-id">Import-ID: {jobId}</p>
                </div>
                <button
                  className="np-secondary"
                  type="button"
                  onClick={() => void getJobStatus()}
                  disabled={busy}
                >
                  {busy ? "Bitte warten …" : "Status aktualisieren"}
                </button>
              </div>
              {status === "failed" && (
                <p className="np-error" role="alert">
                  Die Analyse ist fehlgeschlagen. Starte den Import oben erneut.
                </p>
              )}
              {status === "finished" && (
                <div className="np-result">
                  <h3>Dein Analyseergebnis</h3>
                  <pre>
                    {result == null
                      ? "Der Import wurde ohne Ergebnis abgeschlossen."
                      : typeof result === "string"
                        ? result
                        : JSON.stringify(result, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          )}
        </section>
        <footer className="np-footer">
          <span>NutriPulse AI</span>
          <span>Mehr verstehen. Bewusster essen.</span>
        </footer>
      </main> */}
    </div>
  );
}
