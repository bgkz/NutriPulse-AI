import { useState } from "react";

// Reine UI-Vorlage: noch kein State, kein Nachrichtenversand und keine API.
export default function ChatTemplate() {
  const [userMessage, setUserMessage] = useState("");
  return (
    <aside className="np-card np-chat" aria-labelledby="chat-heading">
      <header className="np-chat-header">
        <span className="np-icon" aria-hidden="true">
          ✧
        </span>
        <div>
          <h2 id="chat-heading">Dein KI-Assistent</h2>
          <p>Raum für deine Ernährungsfragen</p>
        </div>
        <span className="np-badge">VORSCHAU</span>
      </header>

      <div className="np-chat-messages" aria-label="Beispielunterhaltung">
        {/* TODO: Später deine Nachrichten mit messages.map(...) anzeigen.
            Für eigene Nachrichten: className="np-chat-message np-chat-message-user" */}
        <div className="np-chat-message">
          <span className="np-chat-author">NutriPulse AI</span>
          <p>
            Hi! Hier ist Platz für deine Fragen zu deinen Ernährungsdaten. Was
            möchtest du besser verstehen?
          </p>
        </div>
        {/* <div className="np-chat-message np-chat-message-user">
          <span className="np-chat-author">Du · Beispiel</span>
          <p>Kannst du meine Tabelle zusammenfassen?</p>
        </div> */}
      </div>

      <div className="np-chat-composer">
        <label htmlFor="chat-message">Deine Nachricht</label>
        {/* TODO: textarea über value und onChange mit deinem State verbinden. */}
        <textarea
          id="chat-message"
          rows={2}
          placeholder="Stelle eine Frage …"
          aria-describedby="chat-preview-hint"
          onChange={(event) => setUserMessage(event.target.value)}
        />
        <div className="np-chat-actions">
          <p id="chat-preview-hint">Vorschau – Senden noch nicht verfügbar.</p>
          {/* TODO: disabled entfernen und onClick mit handleSend verbinden. */}
          <button
            type="button"
            className="np-secondary"
            aria-label="Nachricht senden"
            onClick={() => alert(userMessage)}
          >
            Senden <span aria-hidden="true">↑</span>
          </button>
        </div>
      </div>
    </aside>
  );
}
