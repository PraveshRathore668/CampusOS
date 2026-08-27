import { Link, useLocation } from "react-router-dom";
import { Ticket, CalendarClock, Bot, LogOut } from "lucide-react";
import { useAuth } from "../context/AuthContext";

const NAV_ITEMS = [
  { to: "/tickets", label: "Tickets", Icon: Ticket },
  { to: "/bookings", label: "Bookings", Icon: CalendarClock },
  { to: "/assistant", label: "AI Assistant", Icon: Bot },
];

export default function Layout({ title, action, children }) {
  const { user, logout } = useAuth();
  const location = useLocation();
  const initial = user?.full_name?.charAt(0)?.toUpperCase() || "?";

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-logo">
          <div className="logo-mark">C</div>
          <span>CampusOS</span>
        </div>

        <nav className="sidebar-nav">
          {NAV_ITEMS.map(({ to, label, Icon }) => (
            <Link
              key={to}
              to={to}
              className={location.pathname === to ? "sidebar-link active" : "sidebar-link"}
            >
              <Icon size={18} strokeWidth={2} />
              <span>{label}</span>
            </Link>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="avatar">{initial}</div>
          <div className="sidebar-user">
            <span className="sidebar-user-name">{user?.full_name}</span>
            <span className="sidebar-user-role">{user?.role}</span>
          </div>
          <button className="icon-btn" onClick={logout} title="Log out">
            <LogOut size={17} />
          </button>
        </div>
      </aside>

      <main className="main-area">
        <div className="main-header">
          <h1>{title}</h1>
          {action}
        </div>
        {children}
      </main>
    </div>
  );
}
