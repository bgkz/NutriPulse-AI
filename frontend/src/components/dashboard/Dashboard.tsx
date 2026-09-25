import { useEffect, useState } from "react";
import "./Dashboard.css";
import "./sidebar/Sidebar.css";
import ChatTemplate from "./ChatTemplate";
import Sidebar from "./sidebar/Sidebar";
import ChatWindow from "./chat/ChatWindow";
import type { Conversation } from "../../types/conversation";
import type { Message } from "@/types/message";
import type { SendMessageResponse } from "@/types/chat";
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
      <Sidebar
        conversations={conversations}
        onSelect={setActiveConversation}
      ></Sidebar>
      <ChatWindow
        activeConversation={activeConversation}
        token={token}
        onMessageSent={(sendMessageResponse) => {
          loadConversations(token);
          setActiveConversation(sendMessageResponse.conversation);
        }}
      />
    </div>
  );
}
