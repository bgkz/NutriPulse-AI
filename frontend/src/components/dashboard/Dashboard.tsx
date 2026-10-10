import { useEffect, useState, useCallback } from "react";
import "./Dashboard.css";
import "./sidebar/Sidebar.css";
import Sidebar from "./sidebar/Sidebar";
import ChatWindow from "./chat/ChatWindow";
import type { Conversation } from "../../types/conversation";
type DashboardProps = { token: string };

export default function Dashboard({ token }: DashboardProps) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversation, setActiveConversation] =
    useState<Conversation | null>(null);

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

  const handleResponseCompleted = useCallback(async () => {
    try {
      const response = await fetch("http://localhost:8000/conversations/", {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.ok) {
        throw new Error("Chats konnten nicht geladen werden.");
      }

      const data: Conversation[] = await response.json();
      setConversations(data);
    } catch (error) {
      alert("Fehler beim Laden der Chats: " + error);
    }
  }, [token]);

  useEffect(() => {
    const controller = new AbortController();

    async function loadInitialConversations() {
      try {
        const response = await fetch("http://localhost:8000/conversations/", {
          signal: controller.signal,
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
          throw new Error("Chats konnten nicht geladen werden.");
        }

        const data: Conversation[] = await response.json();
        if (!controller.signal.aborted) {
          setConversations(data);
        }
      } catch (error) {
        if (controller.signal.aborted) return;
        alert("Fehler beim Laden der Chats: " + error);
      }
    }

    void loadInitialConversations();

    return () => controller.abort();
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
        onResponseCompleted={handleResponseCompleted}
      />
    </div>
  );
}
