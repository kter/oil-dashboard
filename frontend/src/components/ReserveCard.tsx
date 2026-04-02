import { useTranslation } from "react-i18next";
import { tokens } from "../styles/tokens";

interface ReserveCardProps {
  label: string;
  days: number;
  color: string;
}

export function ReserveCard({ label, days, color }: ReserveCardProps) {
  const { t } = useTranslation();

  return (
    <div
      data-testid="reserve-card"
      style={{
        background: tokens.colors.surface,
        borderRadius: tokens.borderRadius,
        padding: tokens.spacing.xl,
        border: `1px solid ${tokens.colors.border}`,
        borderTop: `4px solid ${color}`,
        flex: "1 1 200px",
        minWidth: "150px",
        textAlign: "center",
      }}
    >
      <div
        style={{
          fontSize: tokens.font.size.cardLabel,
          color: tokens.colors.text.secondary,
          marginBottom: tokens.spacing.sm,
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontSize: tokens.font.size.value,
          fontWeight: "bold",
          color: tokens.colors.text.primary,
        }}
      >
        {t("daysUnit", { count: days })}
      </div>
    </div>
  );
}
