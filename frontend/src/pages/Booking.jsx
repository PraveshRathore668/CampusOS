import { useState, useEffect } from "react";
import apiClient from "../api/client";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";

export default function Booking() {
  const [resources, setResources] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [form, setForm] = useState({ resource_id: "", start_time: "", end_time: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const { user, logout } = useAuth();

  async function loadData() {
    const [resRes, bookRes] = await Promise.all([
      apiClient.get("/api/v1/bookings/resources"),
      apiClient.get("/api/v1/bookings"),
    ]);
    setResources(resRes.data);
    setBookings(bookRes.data);
  }

  useEffect(() => {
    loadData();
  }, []);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");
    setSubmitting(true);
    try {
      await apiClient.post("/api/v1/bookings", {
        resource_id: parseInt(form.resource_id),
        start_time: new Date(form.start_time).toISOString(),
        end_time: new Date(form.end_time).toISOString(),
      });
      setSuccess("Booking confirmed!");
      setForm({ resource_id: "", start_time: "", end_time: "" });
      await loadData();
    } catch (err) {
      if (err.response?.status === 409) {
        setError("This resource is already booked for the selected time slot.");
      } else {
        setError("Failed to create booking.");
      }
    } finally {
      setSubmitting(false);
    }
  }

  function resourceName(id) {
    const r = resources.find((r) => r.id === id);
    return r ? r.name : `Resource #${id}`;
  }

  return (
    <div className="page">
      <header className="page-header">
        <h1>CampusOS — Bookings</h1>
        <div>
          <span className="user-badge">{user?.full_name} ({user?.role})</span>
          <button className="logout-btn" onClick={logout}>Log Out</button>
        </div>
      </header>

      <nav className="page-nav">
        <Link to="/tickets">Tickets</Link>
        <Link to="/bookings" className="active">Bookings</Link>
        <Link to="/assistant">AI Assistant</Link>
      </nav>

      <form onSubmit={handleSubmit} className="ticket-form">
        <select name="resource_id" value={form.resource_id} onChange={handleChange} required>
          <option value="">Select a resource...</option>
          {resources.map((r) => (
            <option key={r.id} value={r.id}>
              {r.name} ({r.resource_type})
            </option>
          ))}
        </select>
        <label>
          Start time
          <input
            type="datetime-local"
            name="start_time"
            value={form.start_time}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          End time
          <input
            type="datetime-local"
            name="end_time"
            value={form.end_time}
            onChange={handleChange}
            required
          />
        </label>
        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}
        <button type="submit" disabled={submitting}>
          {submitting ? "Booking..." : "Book Resource"}
        </button>
      </form>

      <h2>Your Bookings</h2>
      {bookings.length === 0 ? (
        <p>No bookings yet.</p>
      ) : (
        <div className="ticket-list">
          {bookings.map((b) => (
            <div key={b.id} className="ticket-card">
              <h3>{resourceName(b.resource_id)}</h3>
              <p>
                {new Date(b.start_time).toLocaleString()} —{" "}
                {new Date(b.end_time).toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
