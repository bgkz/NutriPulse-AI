import { useState } from "react";

type RegisterFormProps = {
  onSuccess: () => void;
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
        alert(data.detail);
      }
    } catch (error) {
      alert("ERROR: " + error);
    }
  }

  return (
    <div id="registerModal" className="modal">
      <div className="modal-content">
        <span className="close-btn">&times;</span>
        <h2>Registrieren</h2>
        <form>
          <input
            type="text"
            onChange={(event) => setUsername(event.target.value)}
            placeholder="Benutzername"
            required
          />
          <br />
          <br />
          <br />
          <input
            type="password"
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Passwort"
            required
          />
          <br />
          <br />
          <button
            type="submit"
            onClick={(event) => handleRegistration(event, username, password)}
          >
            Konto erstellen
          </button>
        </form>
      </div>
    </div>
  );
}
