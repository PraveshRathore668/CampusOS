import { useState, useRef, useEffect } from "react";
import apiClient from "../api/client";
import Layout from "../components/Layout";
import { FileText, Send } from "lucide-react";

export default function Assistant() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!input.trim()) return;

    const question = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", text: question }]);
    setLoading(true);

    try {
      const res = await apiClient.post("/api/v1/ai/chat", { question });
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: res.data.answer, sources: res.data.sources },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "Something went wrong. Please try again.", sources: [] },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Layout title="AI Assistant">
      <div className="chat-window">
        {messages.length === 0 && (
          <p className="chat-empty">
            Ask a question about campus policies, procedures, or documents.
            <br />
            e.g. "How do I apply for a hostel room?"
          </p>
        )}

        {messages.map((m, i) => (
          <div key={i} className={`chat-bubble chat-${m.role}`}>
            <p>{m.text}</p>
            {m.sources && m.sources.length > 0 && (
              <div className="chat-sources">
                {m.sources.map((s, j) => (
                  <div key={j} className="source-chip">
                    <FileText size={12} /> {s.document_filename} (part {s.chunk_index + 1})
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="chat-bubble chat-assistant">
            <p className="thinking">Thinking...</p>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          placeholder="Ask the campus assistant..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          <Send size={16} />
        </button>
      </form>
    </Layout>
  );
}
