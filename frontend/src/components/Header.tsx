import { useTranslation } from "react-i18next";
import { LanguageSelector } from "./LanguageSelector";
import { tokens } from "../styles/tokens";

interface HeaderProps {
  lastUpdated: string | null;
}

export function Header({ lastUpdated }: HeaderProps) {
  const { t } = useTranslation();

  return (
    <header
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        flexWrap: "wrap",
        gap: tokens.spacing.md,
        marginBottom: tokens.spacing.xl,
      }}
    >
      <h1
        data-testid="header-title"
        style={{
          fontSize: "20px",
          fontWeight: "bold",
          color: tokens.colors.text.primary,
          margin: 0,
        }}
      >
        {t("title")}
      </h1>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: tokens.spacing.lg,
          flexWrap: "wrap",
        }}
      >
        <LanguageSelector />
        {lastUpdated && (
          <span
            style={{
              fontSize: tokens.font.size.subtitle,
              color: tokens.colors.text.secondary,
            }}
          >
            {t("lastUpdated")}: {lastUpdated}
          </span>
        )}
      </div>
    </header>
  );
}
