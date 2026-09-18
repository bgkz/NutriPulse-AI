import type { Conversation } from "../../../types/conversation";
import "./ConversationCard.css";

type ConversationCardProps = {
  conversation: Conversation;
};

export default function ConversationCard({
  conversation,
}: ConversationCardProps) {
  return (
    <button className="np-conversation-card" type="button">
      <span className="np-conversation-card-icon" aria-hidden="true">
        <svg
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.6"
          strokeLinecap="round"
          strokeLinejoin="round"
          focusable="false"
        >
          <path d="M7 4h10a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3H9l-5 3V7a3 3 0 0 1 3-3Z" />
          <path d="M8 9h8M8 13h5" />
        </svg>
      </span>
      <span className="np-conversation-card-title" title={conversation.title}>
        {conversation.title}
      </span>
    </button>
  );
}
