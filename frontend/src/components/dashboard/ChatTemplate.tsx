import { useState } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function ChatTemplate() {
  const [userMessage, setUserMessage] = useState("");

  const [messageHistory, setMessageHistory] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hi! Hier ist Platz für deine Fragen zu deinen Ernährungsdaten. Was möchtest du besser verstehen?",
    },
  ]);
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
        <div className="np-chat-messages">
          {messageHistory.map((message, index) =>
            message.role === "user" ? (
              <div className="np-chat-message np-chat-message-user">
                {message.content}
              </div>
            ) : (
              <div className="np-chat-message">{message.content}</div>
            ),
          )}
        </div>
      </div>

      <div className="np-chat-composer">
        <label htmlFor="chat-message">Deine Nachricht</label>
        <textarea
          id="chat-message"
          rows={2}
          placeholder="Stelle eine Frage …"
          aria-describedby="chat-preview-hint"
          value={userMessage}
          onChange={(event) => setUserMessage(event.target.value)}
        />
        <div className="np-chat-actions">
          <button
            type="button"
            className="np-secondary"
            aria-label="Nachricht senden"
            onClick={() => {
              setMessageHistory((prev) => [
                ...prev,
                {
                  role: "user",
                  content: userMessage,
                },
              ]);
              setUserMessage("");
            }}
          >
            Senden <span aria-hidden="true">↑</span>
          </button>
        </div>
      </div>
    </aside>
  );
}
