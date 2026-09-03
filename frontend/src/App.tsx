import "./App.css";
import LoginForm from "./components/LoginForm";
import { useState } from "react";
function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return <>{!isLoggedIn && <LoginForm />}</>;
}
export default App;
