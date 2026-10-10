import { useState, useEffect, useRef } from "react";
import "./ChatWindow.css";
import type { Conversation } from "@/types/conversation";
import type { Message } from "@/types/message";
import type { SendMessageResponse } from "@/types/chat";

type ChatWindowProps = {
  activeConversation: Conversation | null;
  token: string;
  onMessageSent: (sent_message: SendMessageResponse) => void;
  onResponseCompleted: () => void;
};

type SendMessageRequest = {
  conversation_id: string | null;
  role: "user" | "assistant";
  content: string;
};

type GoogleSheetImportJob = {
  job_id: string;
  status: string;
};

export default function ChatWindow({
  activeConversation,
  token,
  onMessageSent,
  onResponseCompleted,
}: ChatWindowProps) {
  const [isImportOpen, setIsImportOpen] = useState(false);
  const [isGoogleSheetImportOpen, setIsGoogleSheetImportOpen] = useState(false);
  const [googleSheetUrl, setGoogleSheetUrl] = useState("");
  const [isImporting, setIsImporting] = useState(false);
  const [importStatus, setImportStatus] = useState("");
  const importControllerRef = useRef<AbortController | null>(null);
  const importTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const messagesRef = useRef<HTMLDivElement>(null);
  const [messageHistory, setMessageHistory] = useState<Message[]>([]);
  const [userMessage, setUserMessage] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState("");
  const [pendingJob, setPendingJob] = useState<{
    id: string;
    conversationId: string;
  } | null>(null);

  useEffect(() => {
    return () => {
      importControllerRef.current?.abort();
      if (importTimerRef.current !== null) clearTimeout(importTimerRef.current);
    };
  }, []);

  async function handleGoogleSheetImport(
    googleSheetUrl: string,
    token: string,
    activeConversation: Conversation | null,
  ) {
    if (importControllerRef.current && !importControllerRef.current.signal.aborted) return;
    const cleanedUrl = googleSheetUrl.trim();

    if (cleanedUrl.length == 0) {
      setError("Keine URL angegeben, bitte geben sie eine URL an");
      return;
    }

    const controller = new AbortController();
    importControllerRef.current = controller;
    setIsImporting(true);
    setImportStatus("Google Sheet wird importiert …");
    setError("");

    function handleImportError(error: unknown) {
      if (controller.signal.aborted) return;
      setError(error instanceof Error ? error.message : "Import fehlgeschlagen.");
      setImportStatus("");
      setIsImporting(false);
      importControllerRef.current = null;
    }

    async function checkJob(jobId: string) {
      try {
        const response = await fetch(
          `http://localhost:8000/documents/jobs/${jobId}`,
          {
            signal: controller.signal,
            headers: { Authorization: `Bearer ${token}` },
          },
        );
        if (!response.ok) throw new Error("Der Import-Status konnte nicht geladen werden.");
        const job: { status: string } = await response.json();
        if (controller.signal.aborted) return;

        if (job.status === "finished") {
          setImportStatus("Google-Sheet-Import abgeschlossen.");
          setIsImporting(false);
          setIsGoogleSheetImportOpen(false);
          setGoogleSheetUrl("");
          importControllerRef.current = null;
          return;
        }
        if (["failed", "stopped", "canceled"].includes(job.status)) {
          throw new Error("Import fehlgeschlagen. Bitte versuche es erneut.");
        }
        importTimerRef.current = setTimeout(() => void checkJob(jobId), 1000);
      } catch (error) {
        handleImportError(error);
      }
    }

    try {
      const response = await fetch("http://localhost:8000/documents/import", {
        method: "POST",
        signal: controller.signal,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          url: cleanedUrl,
          conversation_id: activeConversation?.id ?? null,
        }),
      });

      if (!response.ok) {
        throw new Error("Import fehlgeschlagen");
      }
      const job: GoogleSheetImportJob = await response.json();
      if (!controller.signal.aborted) await checkJob(job.job_id);
    } catch (error) {
      handleImportError(error);
    }
  }

  async function handleSendMessage(message: string) {
    if (!message.trim() || isSending || pendingJob) return;
    setIsSending(true);
    setError("");
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
        setPendingJob({
          id: sendMessageResponse.job,
          conversationId: sendMessageResponse.conversation.id,
        });
        onMessageSent(sendMessageResponse);
      }

      if (!response.ok) {
        throw new Error("Die Nachricht konnte nicht gesendet werden.");
      }
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Der Server ist nicht erreichbar.",
      );
      setMessageHistory((prev) =>
        prev.filter((item) => item.id !== tempMessage.id),
      );
    } finally {
      setIsSending(false);
      setUserMessage("");
    }
  }

  useEffect(() => {
    const container = messagesRef.current;
    if (!container) return;

    container.scrollTo({
      top: container.scrollHeight,
      behavior: "smooth",
    });
  }, [messageHistory]);

  useEffect(() => {
    const controller = new AbortController();
    let timer: ReturnType<typeof setTimeout>;
    const options = {
      signal: controller.signal,
      headers: { Authorization: `Bearer ${token}` },
    };

    async function loadMessages() {
      if (!activeConversation) return;
      const response = await fetch(
        `http://localhost:8000/messages/${activeConversation.id}`,
        options,
      );
      if (!response.ok)
        throw new Error("Der Chatverlauf konnte nicht geladen werden.");
      const messages: Message[] = await response.json();
      if (!controller.signal.aborted) setMessageHistory(messages);
    }

    async function updateChat(checkJob: boolean) {
      try {
        if (checkJob && pendingJob) {
          const response = await fetch(
            `http://localhost:8000/chat/jobs/${pendingJob.id}`,
            options,
          );
          if (!response.ok)
            throw new Error("Der Job-Status konnte nicht geladen werden.");
          const job: { status: string } = await response.json();
          if (controller.signal.aborted) return;

          if (["failed", "stopped", "canceled"].includes(job.status)) {
            throw new Error(
              "Die KI-Antwort konnte nicht erstellt werden. Bitte versuche es erneut.",
            );
          }
          if (job.status === "finished") {
            if (activeConversation?.id === pendingJob.conversationId)
              await loadMessages();
            onResponseCompleted();
            if (!controller.signal.aborted) setPendingJob(null);
            return;
          }
        } else {
          await loadMessages();
        }

        if (pendingJob && !controller.signal.aborted) {
          timer = setTimeout(() => void updateChat(true), 1000);
        }
      } catch (error) {
        if (controller.signal.aborted) return;
        setError(
          error instanceof Error
            ? error.message
            : "Der Server ist nicht erreichbar.",
        );
        setPendingJob(null);
      }
    }

    void updateChat(false);
    return () => {
      controller.abort();
      clearTimeout(timer);
    };
  }, [activeConversation, pendingJob, token]);

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
        <div className="chat-window-messages" ref={messagesRef}>
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
        {error && <p role="alert">{error}</p>}
        {importStatus && <p role="status">{importStatus}</p>}
        {pendingJob && <p role="status">Die KI erstellt deine Antwort …</p>}
        <div className="chat-window-input-row">
          <button
            type="button"
            className="chat-window-attach"
            aria-label="Datei anhängen"
            onClick={() => setIsImportOpen((prev) => !prev)}
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
          {isImportOpen && (
            <div className="chat-window-import">
              <button
                type="button"
                onClick={() => {
                  setIsGoogleSheetImportOpen(true);
                  setIsImportOpen(false);
                }}
              >
                + Google Sheets importieren
              </button>
            </div>
          )}

          <input
            type="text"
            aria-label="Nachricht"
            placeholder="Schreibe deine Nachricht..."
            value={userMessage}
            disabled={isSending || pendingJob !== null}
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
            disabled={isSending || pendingJob !== null || !userMessage.trim()}
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
      {isGoogleSheetImportOpen && (
        <dialog
          className="chat-window-import-google-sheet"
          ref={(dialog) => {
            dialog?.showModal();
          }}
          onClose={() => setIsGoogleSheetImportOpen(false)}
          aria-labelledby="sheet-import-title"
        >
          <h3 id="sheet-import-title">Google Sheets importieren</h3>
          <label htmlFor="sheet-url">Google-Sheets-URL</label>
          <input
            id="sheet-url"
            type="url"
            placeholder="https://docs.google.com/spreadsheets/d/…"
            autoFocus
            value={googleSheetUrl}
            disabled={isImporting}
            onChange={(event) => setGoogleSheetUrl(event.target.value)}
          />
          {error && <p role="alert">{error}</p>}
          {isImporting && <p role="status">{importStatus}</p>}
          <div className="chat-window-import-actions">
            <button
              type="button"
              onClick={() => setIsGoogleSheetImportOpen(false)}
            >
              Abbrechen
            </button>
            <button
              type="button"
              disabled={isImporting}
              onClick={() =>
                handleGoogleSheetImport(
                  googleSheetUrl,
                  token,
                  activeConversation,
                )
              }
            >
              {isImporting ? "Import läuft …" : "Importieren"}
            </button>
          </div>
        </dialog>
      )}
    </section>
  );
}
