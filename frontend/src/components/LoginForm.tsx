import { useState } from "react";
import RegistrationForm from "@/components/RegistrationForm";
export default function LoginForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showRegisterForm, setShowRegisterForm] = useState(false);

  function handleLogin(username: string, password: string) {
    alert(`Username: ${username}\nPassword: ${password}`);
  }

  return (
    <form className="w-full h-full flex flex-col gap-6">
      <span>Welcome to NutriPulse AI</span>
      <div className="flex flex-col gap-6">
        {/* Gruppe 1: Username */}
        <div className="flex flex-col gap-2">
          <span>Username</span>
          <input
            type="text"
            className="border p-2 rounded"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          />
        </div>

        {/* Gruppe 2: Password */}
        <div className="flex flex-col gap-2">
          <span>Password</span>
          <input
            type="password"
            className="border p-2 rounded"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </div>

        {/* Gruppe 3: Login/Registrieren */}
        <div className="flex flex-col gap-2">
          <button
            type="button"
            onClick={() => {
              handleLogin(username, password);
            }}
          >
            Login
          </button>
          <button
            type="button"
            onClick={() => {
              setShowRegisterForm(true);
            }}
          >
            Registrieren
          </button>
          <>
            {showRegisterForm && (
              <RegistrationForm onSuccess={() => setShowRegisterForm(false)} />
            )}
          </>
          ;
        </div>
      </div>
    </form>
  );
}
