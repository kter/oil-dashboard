import { useTranslation } from "react-i18next";
import { useReserves } from "../hooks/useReserves";
import { Header } from "./Header";
import { ReservesChart } from "./ReservesChart";
import { ReserveCard } from "./ReserveCard";
import { tokens } from "../styles/tokens";

export function Dashboard() {
  const { t } = useTranslation();
  const { data, latest, lastUpdated, loading, error } = useReserves();

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: tokens.spacing.xxl }}>
        {t("loading")}
      </div>
    );
  }

  if (error) {
    return (
      <div
        style={{
          textAlign: "center",
          padding: tokens.spacing.xxl,
          color: tokens.colors.alert,
        }}
      >
        {t("error")}
      </div>
    );
  }

  return (
    <div>
      <Header lastUpdated={lastUpdated} />
      <ReservesChart data={data} />
      <div
        style={{
          display: "flex",
          gap: tokens.spacing.lg,
          marginTop: tokens.spacing.lg,
          flexWrap: "wrap",
        }}
      >
        {latest && (
          <>
            <ReserveCard
              label={t("national")}
              days={latest.national_days}
              color={tokens.colors.chart.national}
            />
            <ReserveCard
              label={t("private")}
              days={latest.private_days}
              color={tokens.colors.chart.private}
            />
            <ReserveCard
              label={t("cooperative")}
              days={latest.cooperative_days}
              color={tokens.colors.chart.cooperative}
            />
          </>
        )}
      </div>
    </div>
  );
}
