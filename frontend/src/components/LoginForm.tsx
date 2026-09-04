import { useState } from "react";
import RegistrationForm from "./RegistrationForm";

type LoginFormProps = {
  onSuccess: () => void;
};

export default function LoginForm({ onSuccess }: LoginFormProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showRegisterForm, setShowRegisterForm] = useState(false);

  async function handleLogin(
    event: React.FormEvent,
    username: string,
    password: string,
  ) {
    event.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });

      if (response.ok) {
        alert("User: " + username + " erfolgriech angemeldet");
        onSuccess();
      } else {
        const data = await response.json();
        alert("Response not ok: " + data.detail);
      }
    } catch (error) {
      alert("ERROR: " + error);
    }
  }

  return (
    <div className="flex min-h-screen w-full items-center justify-center bg-gradient-to-br from-slate-50 via-white to-violet-100 p-4 dark:from-slate-950 dark:via-slate-900 dark:to-violet-950">
      <form className="w-full max-w-md rounded-3xl border border-white/60 bg-white/90 p-8 text-left shadow-2xl shadow-violet-900/10 backdrop-blur-xl dark:border-white/10 dark:bg-slate-900/90">
        <div className="mb-8">
          <span className="mb-3 inline-flex rounded-full bg-violet-100 px-3 py-1 text-xs font-semibold tracking-wide text-violet-700 uppercase dark:bg-violet-500/15 dark:text-violet-300">
            NutriPulse AI
          </span>
          <h1 className="m-0 text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
            Willkommen zurück
          </h1>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
            Melde dich an, um deine Ernährungsreise fortzusetzen.
          </p>
        </div>

        <div className="flex flex-col gap-5">
          <label className="flex flex-col gap-2 text-sm font-medium text-slate-700 dark:text-slate-200">
            Benutzername
            <input
              type="text"
              className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-violet-500 focus:bg-white focus:ring-4 focus:ring-violet-500/10 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:focus:border-violet-400"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              placeholder="Dein Benutzername"
              required
            />
          </label>

          <label className="flex flex-col gap-2 text-sm font-medium text-slate-700 dark:text-slate-200">
            Passwort
            <input
              type="password"
              className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-violet-500 focus:bg-white focus:ring-4 focus:ring-violet-500/10 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:focus:border-violet-400"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Dein Passwort"
              required
            />
          </label>

          <div className="mt-2 flex flex-col gap-3">
            <button
              type="button"
              className="w-full rounded-xl bg-violet-600 px-4 py-3 font-semibold text-white shadow-lg shadow-violet-600/20 transition hover:-translate-y-0.5 hover:bg-violet-700 focus:ring-4 focus:ring-violet-500/25 focus:outline-none"
              onClick={(event) => {
                handleLogin(event, username, password);
              }}
            >
              Login
            </button>
            <button
              type="button"
              className="w-full rounded-xl border border-slate-200 px-4 py-3 font-semibold text-slate-600 transition hover:border-violet-300 hover:bg-violet-50 hover:text-violet-700 focus:ring-4 focus:ring-violet-500/10 focus:outline-none dark:border-slate-700 dark:text-slate-300 dark:hover:border-violet-500/50 dark:hover:bg-violet-500/10 dark:hover:text-violet-300"
              onClick={() => {
                setShowRegisterForm(true);
              }}
            >
              Registrieren
            </button>
            <>
              {showRegisterForm && (
                <RegistrationForm
                  onSuccess={() => setShowRegisterForm(false)}
                  onClose={() => setShowRegisterForm(false)}
                />
              )}
            </>
          </div>
        </div>
      </form>
    </div>
  );
}
