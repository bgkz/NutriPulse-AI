import type { User } from "../../types/user";

export default function Dashboard({ id, username }: User) {
  return (
    <div>
      Hello {username} --- ID: {id}
    </div>
  );
}
