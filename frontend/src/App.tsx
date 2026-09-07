import "./App.css";
import LoginForm from "./components/LoginForm";
import Dashboard from "./components/dashboard/Dashboard";
import { useState } from "react";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [token, setToken] = useState<string | null>(null);

  return (
    <div className="min-h-screen w-full">
      {!isLoggedIn && (
        <LoginForm
          onSuccess={(token: string) => {
            setToken(token);
            setIsLoggedIn(true);
          }}
        />
      )}

      {isLoggedIn && token && <Dashboard token={token} />}
    </div>
  );
}
export default App;
