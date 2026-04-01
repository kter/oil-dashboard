import { useTranslation } from "react-i18next";
import { tokens } from "../styles/tokens";

const languages = [
  { code: "ja", label: "日本語" },
  { code: "en", label: "English" },
  { code: "ko", label: "한국어" },
  { code: "zh-TW", label: "繁體中文" },
] as const;

export function LanguageSelector() {
  const { i18n, t } = useTranslation();

  return (
    <label
      style={{
        display: "flex",
        alignItems: "center",
        gap: tokens.spacing.sm,
        fontSize: tokens.font.size.label,
        color: tokens.colors.text.secondary,
      }}
    >
      {t("language")}:
      <select
        value={i18n.language}
        onChange={(e) => i18n.changeLanguage(e.target.value)}
        style={{
          padding: `${tokens.spacing.xs} ${tokens.spacing.sm}`,
          borderRadius: "8px",
          border: `1px solid ${tokens.colors.border}`,
          fontSize: tokens.font.size.label,
          background: tokens.colors.surface,
          cursor: "pointer",
        }}
      >
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.label}
          </option>
        ))}
      </select>
    </label>
  );
}
