import type { Conversation } from "./conversation";
import type { Message } from "./message";

export type SendMessageResponse = {
  conversation: Conversation;
  message: Message;
};
