import { useState, useEffect } from "react";
import "./ChatWindow.css";
import type { Conversation } from "@/types/conversation";
import type { Message } from "@/types/message";
import type { SendMessageResponse } from "@/types/chat";

type ChatWindowProps = {
  activeConversation: Conversation | null;
  token: string;
  onMessageSent: (sent_message: SendMessageResponse) => void;
};

type SendMessageRequest = {
  conversation_id: string | null;
  role: "user" | "assistant";
  content: string;
};

export default function ChatWindow({
  activeConversation,
  token,
  onMessageSent,
}: ChatWindowProps) {
  const [messageHistory, setMessageHistory] = useState<Message[]>([]);
  const [userMessage, setUserMessage] = useState("");

  async function handleSendMessage(message: string) {
    const tempMessage: Message = {
      id: crypto.randomUUID(),
      conversation_id: activeConversation?.id ?? null,
      role: "user",
      content: message,
      created_at: new Date().toISOString(),
    };

    setMessageHistory((prev) => [...prev, tempMessage]);

    // Das geht tatsächlich ans Backend
    const request: SendMessageRequest = {
      conversation_id: activeConversation?.id ?? null,
      role: "user",
      content: message,
    };

    try {
      const response = await fetch("http://localhost:8000/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(request),
      });

      if (response.ok) {
        const sendMessageResponse: SendMessageResponse = await response.json();
        onMessageSent(sendMessageResponse);
      }

      if (!response.ok) {
        alert("Response not ok: " + response.json());
      }
    } catch (error) {
      alert("ERROR: " + error);
    } finally {
      setUserMessage("");
    }
  }

  async function loadMessageHistory(activeConversation: Conversation | null) {
    if (activeConversation === null) return;
    try {
      const response = await fetch(
        `http://localhost:8000/messages/${activeConversation.id}`,
      );

      const data: Message[] = await response.json();
      setMessageHistory(data);
    } catch (error) {
      alert("Error occured while fetching conversations: " + error);
    }
  }

  useEffect(() => {
    void loadMessageHistory(activeConversation);
  }, [activeConversation]);

  return (
    <section className="chat-window" aria-label="Chatverlauf">
      {messageHistory.length === 0 && (
        <div className="chat-window-welcome">
          <div className="chat-window-icon" aria-hidden="true">
            ✧
          </div>

          <h2 id="chat-window-title">Stelle deine erste Frage</h2>

          <p>
            NutriPulse analysiert deine Daten, gibt dir individuelle
            Empfehlungen und beantwortet all deine Fragen rund um Ernährung,
            Fitness und Gesundheit.
          </p>
        </div>
      )}

      {messageHistory.length > 0 && (
        <div className="chat-window-messages">
          {messageHistory.map((message) => (
            <article
              key={message.id}
              className={`chat-message${message.role === "user" ? " chat-message-user" : ""}`}
              aria-label={message.role === "user" ? "Du" : "NutriPulse AI"}
            >
              <div className="chat-message-sender">
                <span className="chat-message-avatar" aria-hidden="true">
                  {message.role === "user" ? "Du" : "✧"}
                </span>
                {message.role === "user" ? "Du" : "NutriPulse AI"}
              </div>
              <p>{message.content}</p>
            </article>
          ))}
        </div>
      )}

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
            value={userMessage}
            onChange={(event) => setUserMessage(event.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage(userMessage);
                setUserMessage("");
              }
            }}
          />
          <button
            type="button"
            className="chat-window-send"
            aria-label="Nachricht senden"
            onClick={() => {
              handleSendMessage(userMessage);
            }}
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
