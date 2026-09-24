export type Message = {
  id: string;
  conversation_id: string | null;
  role: string;
  content: string;
  created_at: string;
};
