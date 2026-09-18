import { useState } from "react";
import ConversationHistory from "./ConversationHistory";
import type { Conversation } from "../../../types/conversation";

type SidebarProps = {
  conversations: Conversation[];
  onSelect: (conversation: Conversation) => void;
};

export default function Sidebar({ conversations, onSelect }: SidebarProps) {
  const [searchInput, setSearchInput] = useState("");

  return (
    <div className="np-sidebar">
      <div className="np-sidebar-header">
        <span className="np-sidebar-logo" aria-hidden="true">
          ϟ
        </span>
        <div className="np-sidebar-brand">
          <span className="np-sidebar-title">NutriPulse AI</span>
          <span className="np-sidebar-subtitle">
            Dein Ernährungspartner mit KI
          </span>
        </div>
      </div>
      <button type="button" className="np-sidebar-create-chat-button">
        <span className="np-sidebar-create-chat-icon" aria-hidden="true">
          +
        </span>
        Neuer Chat
      </button>
      <div className="np-sidebar-search">
        <svg
          className="np-sidebar-search-icon"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          aria-hidden="true"
          focusable="false"
        >
          <circle cx="10.5" cy="10.5" r="6.5" />
          <path d="m16 16 4.5 4.5" />
        </svg>
        <input
          className="np-sidebar-search-bar"
          type="search"
          aria-label="Chats durchsuchen"
          placeholder="Chats durchsuchen..."
          value={searchInput}
          onChange={(event) => {
            setSearchInput(event.target.value);
          }}
        />
      </div>
      <ConversationHistory
        conversations={conversations}
        onSelect={onSelect}
      ></ConversationHistory>
    </div>
  );
}
