import type { Conversation } from "../../../types/conversation";
import "./ConversationCard.css";

type ConversationCardProps = {
  conversation: Conversation;
};

export default function ConversationCard({
  conversation,
}: ConversationCardProps) {
  return <div>{conversation.title}</div>;
}
