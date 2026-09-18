import type { Conversation } from "../../../types/conversation";
import "./ConversationHistory.css";
import ConversationCard from "./ConversationCard";
type ConversationHistoryProps = {
  conversations: Conversation[];
  onSelect: (conversation: Conversation) => void;
};

export default function ConversationHistory({
  conversations,
  onSelect,
}: ConversationHistoryProps) {
  return (
    <div className="np-conversation-history">
      {conversations.length === 0 && (
        <div className="np-conversation-history-empty">
          <svg
            className="np-conversation-history-empty-icon"
            width="64"
            height="64"
            viewBox="0 0 64 64"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
            focusable="false"
          >
            <path d="M36 18H14a6 6 0 0 0-6 6v22a6 6 0 0 0 6 6v6l9-6h17a6 6 0 0 0 6-6V32" />
            <path d="m45 3 2.5 7.5L55 13l-7.5 2.5L45 23l-2.5-7.5L35 13l7.5-2.5L45 3Z" />
            <path d="M55 24v10m-5-5h10" />
            <path d="M19 35h2m6 0h2m6 0h2" />
          </svg>
          <h2>Noch keine Unterhaltungen</h2>
          <p>
            Starte deinen ersten Chat und erhalte persönliche Einblicke in deine
            Ernährung, Fitness und mehr.
          </p>
        </div>
      )}
      <div className="np-conversation-history-card">
        {conversations.map((conversation) => (
          <ConversationCard
            key={conversation.id}
            conversation={conversation}
            onSelect={onSelect}
          />
        ))}
      </div>
    </div>
  );
}
