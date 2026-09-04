import { useState } from "react";

type RegisterFormProps = {
  onSuccess: () => void;
  onClose: () => void;
};

export default function RegistrationForm({ onSuccess }: RegisterFormProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  async function handleRegistration(
    event: React.FormEvent,
    username: string,
    password: string,
  ) {
    event.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/users/", {
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
        alert("User: " + username + " erfolgriech registriert");
        onSuccess();
      } else {
        const data = await response.json();
        alert("Response was not ok: " + data.detail);
      }
    } catch (error) {
      alert("ERROR: " + error);
    }
  }

  return (
    <div
      id="registerModal"
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 p-4 backdrop-blur-sm"
    >
      <div className="w-full max-w-md rounded-3xl border border-white/10 bg-white p-8 text-left shadow-2xl dark:bg-slate-900">
        <div className="mb-7">
          <span className="mb-3 inline-flex rounded-full bg-violet-100 px-3 py-1 text-xs font-semibold tracking-wide text-violet-700 uppercase dark:bg-violet-500/15 dark:text-violet-300">
            NutriPulse AI
          </span>
          <h2 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
            Konto erstellen
          </h2>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
            Registriere dich und starte deine persönliche Ernährungsreise.
          </p>
        </div>

        <form className="flex flex-col gap-5">
          <label className="flex flex-col gap-2 text-sm font-medium text-slate-700 dark:text-slate-200">
            Benutzername
            <input
              type="text"
              className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-violet-500 focus:bg-white focus:ring-4 focus:ring-violet-500/10 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:focus:border-violet-400"
              onChange={(event) => setUsername(event.target.value)}
              placeholder="Dein Benutzername"
            />
          </label>

          <label className="flex flex-col gap-2 text-sm font-medium text-slate-700 dark:text-slate-200">
            Passwort
            <input
              type="password"
              className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-violet-500 focus:bg-white focus:ring-4 focus:ring-violet-500/10 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:focus:border-violet-400"
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Mindestens 8 Zeichen"
            />
          </label>

          <div className="mt-2 flex flex-col-reverse gap-3 sm:flex-row">
            <button
              style={{ cursor: "pointer" }}
              className="flex-1 rounded-xl border border-slate-200 px-4 py-3 font-semibold text-slate-600 transition hover:border-slate-300 hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
            >
              Schließen
            </button>
            <button
              type="submit"
              className="flex-1 rounded-xl bg-violet-600 px-4 py-3 font-semibold text-white shadow-lg shadow-violet-600/20 transition hover:-translate-y-0.5 hover:bg-violet-700 focus:ring-4 focus:ring-violet-500/25 focus:outline-none"
              onClick={(event) => handleRegistration(event, username, password)}
            >
              Konto erstellen
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
