import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Ticket, CalendarClock, Bot } from "lucide-react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await login(email, password);
      navigate("/tickets");
    } catch (err) {
      setError("Invalid email or password");
    }
  }

  return (
    <div className="split-auth">
      <div className="brand-panel">
        <div className="brand-mark">
          <div className="logo-mark logo-mark-lg">C</div>
          <span>CampusOS</span>
        </div>
        <h2>AI-powered campus operations, in one place.</h2>
        <div className="brand-features">
          <div className="brand-feature">
            <Ticket size={18} />
            <span>Auto-classified complaint tickets</span>
          </div>
          <div className="brand-feature">
            <CalendarClock size={18} />
            <span>Conflict-free resource booking</span>
          </div>
          <div className="brand-feature">
            <Bot size={18} />
            <span>AI assistant grounded in campus docs</span>
          </div>
        </div>
      </div>

      <div className="form-panel">
        <form onSubmit={handleSubmit} className="auth-form">
          <h1>Welcome back</h1>
          <p className="form-subtitle">Log in to your CampusOS account</p>
          {error && <p className="error">{error}</p>}
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Log In</button>
          <p>
            Don't have an account? <Link to="/register">Register</Link>
          </p>
        </form>
      </div>
    </div>
  );
}
