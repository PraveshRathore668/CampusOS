import { useState, useEffect } from "react";
import apiClient from "../api/client";
import Layout from "../components/Layout";
import { Plus, Inbox, MapPin } from "lucide-react";

export default function Tickets() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ title: "", description: "", location: "" });
  const [submitting, setSubmitting] = useState(false);

  async function loadTickets() {
    setLoading(true);
    const res = await apiClient.get("/api/v1/tickets");
    setTickets(res.data);
    setLoading(false);
  }

  useEffect(() => {
    loadTickets();
  }, []);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    try {
      await apiClient.post("/api/v1/tickets", form);
      setForm({ title: "", description: "", location: "" });
      setShowForm(false);
      await loadTickets();
    } catch (err) {
      alert("Failed to create ticket");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Layout
      title="Tickets"
      action={
        <button className="primary-btn" onClick={() => setShowForm(!showForm)}>
          <Plus size={16} /> {showForm ? "Cancel" : "New Ticket"}
        </button>
      }
    >
      {showForm && (
        <form onSubmit={handleSubmit} className="ticket-form">
          <input
            name="title"
            placeholder="Title"
            value={form.title}
            onChange={handleChange}
            required
          />
          <input
            name="location"
            placeholder="Location"
            value={form.location}
            onChange={handleChange}
            required
          />
          <textarea
            name="description"
            placeholder="Describe the issue..."
            value={form.description}
            onChange={handleChange}
            required
          />
          <p className="hint">Category and priority will be predicted automatically by AI.</p>
          <button type="submit" disabled={submitting}>
            {submitting ? "Submitting..." : "Submit Ticket"}
          </button>
        </form>
      )}

      {loading ? (
        <p className="muted">Loading tickets...</p>
      ) : tickets.length === 0 ? (
        <div className="empty-state">
          <Inbox size={28} strokeWidth={1.5} />
          <p>No tickets yet. Create one to get started.</p>
        </div>
      ) : (
        <div className="ticket-list">
          {tickets.map((t) => (
            <div key={t.id} className="ticket-card">
              <div className="ticket-card-header">
                <h3>{t.title}</h3>
                <span className={`status-badge status-${t.status.toLowerCase()}`}>
                  {t.status}
                </span>
              </div>
              <p>{t.description}</p>
              <div className="ticket-meta">
                <span className="tag">{t.category}</span>
                <span className={`tag priority-${t.priority.toLowerCase()}`}>{t.priority}</span>
                <span className="location"><MapPin size={13} /> {t.location}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}
