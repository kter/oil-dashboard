import { Dashboard } from "./components/Dashboard";
import { tokens } from "./styles/tokens";

export function App() {
  return (
    <div
      style={{
        minHeight: "100vh",
        background: tokens.colors.background,
        fontFamily: tokens.font.family,
        padding: tokens.spacing.xl,
        maxWidth: "1024px",
        margin: "0 auto",
      }}
    >
      <Dashboard />
    </div>
  );
}
