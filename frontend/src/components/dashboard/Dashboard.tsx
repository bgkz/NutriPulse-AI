import { useEffect, useState } from "react";
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
