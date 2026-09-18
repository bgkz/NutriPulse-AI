import "./ChatWindow.css";

export default function ChatWindow() {
  return (
    <section className="chat-window" aria-labelledby="chat-window-title">
      <div className="chat-window-welcome">
        <div className="chat-window-icon" aria-hidden="true">
          ✧
        </div>
        <h2 id="chat-window-title">Stelle deine erste Frage</h2>
        <p>
          NutriPulse analysiert deine Daten, gibt dir individuelle Empfehlungen
          und beantwortet all deine Fragen rund um Ernährung, Fitness und
          Gesundheit.
        </p>
      </div>

      {/* Template: Nachrichten und Event-Handler kannst du hier ergänzen. */}
      <div className="chat-window-composer">
        <div className="chat-window-input-row">
          <button
            type="button"
            className="chat-window-attach"
            aria-label="Datei anhängen"
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="m21 11-8.5 8.5a6 6 0 0 1-8.5-8.5l9-9a4 4 0 0 1 5.7 5.7l-9 9a2 2 0 0 1-2.8-2.8l8.5-8.5" />
            </svg>
          </button>
          <input
            type="text"
            aria-label="Nachricht"
            placeholder="Schreibe deine Nachricht..."
          />
          <button
            type="button"
            className="chat-window-send"
            aria-label="Nachricht senden"
          >
            ➜
          </button>
        </div>
        <p>
          Du kannst auch allgemeine Fragen stellen. Für personalisierte Analysen
          verbinde später deine Daten.
        </p>
      </div>
    </section>
  );
}
