import "./App.css";
import LoginForm from "./components/LoginForm";
import Dashboard from "./components/dashboard/Dashboard";
import { useState } from "react";

import type { User } from "./types/user";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState<User | null>(null);

  return (
    <div className="min-h-screen w-full">
      {!isLoggedIn && (
        <LoginForm
          onSuccess={(user: User) => {
            setUser(user);
            setIsLoggedIn(true);
          }}
        />
      )}

      {isLoggedIn && user && (
        <Dashboard id={user.id} username={user.username} />
      )}
    </div>
  );
}
export default App;
