import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import apiClient from "../api/client";
import { Ticket, CalendarClock, Bot } from "lucide-react";

export default function Register() {
  const [form, setForm] = useState({
    email: "",
    password: "",
    full_name: "",
    role: "STUDENT",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await apiClient.post("/api/v1/auth/register", form);
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    }
  }

  return (
    <div className="split-auth">
      <div className="brand-panel">
        <div className="brand-mark">
          <div className="logo-mark logo-mark-lg">C</div>
          <span>CampusOS</span>
        </div>
        <h2>Join your campus, digitally.</h2>
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
          <h1>Create your account</h1>
          <p className="form-subtitle">Get started with CampusOS</p>
          {error && <p className="error">{error}</p>}
          <input
            name="full_name"
            placeholder="Full Name"
            value={form.full_name}
            onChange={handleChange}
            required
          />
          <input
            name="email"
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            required
          />
          <input
            name="password"
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            required
          />
          <select name="role" value={form.role} onChange={handleChange}>
            <option value="STUDENT">Student</option>
            <option value="FACULTY">Faculty</option>
            <option value="ADMIN">Admin</option>
          </select>
          <button type="submit">Register</button>
          <p>
            Already have an account? <Link to="/login">Log In</Link>
          </p>
        </form>
      </div>
    </div>
  );
}
