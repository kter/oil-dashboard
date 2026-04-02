import { useTranslation } from "react-i18next";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import type { ReserveRecord } from "../types/reserves";
import { tokens } from "../styles/tokens";

interface ReservesChartProps {
  data: ReserveRecord[];
}

export function ReservesChart({ data }: ReservesChartProps) {
  const { t } = useTranslation();

  const chartData = data.map((record) => ({
    date: record.date,
    [t("national")]: record.national_days,
    [t("private")]: record.private_days,
    [t("cooperative")]: record.cooperative_days,
  }));

  return (
    <div
      data-testid="reserves-chart"
      style={{
        background: tokens.colors.surface,
        borderRadius: tokens.borderRadius,
        padding: tokens.spacing.lg,
        border: `1px solid ${tokens.colors.border}`,
      }}
    >
      <h2
        style={{
          fontSize: tokens.font.size.title,
          fontWeight: "bold",
          margin: `0 0 ${tokens.spacing.md} 0`,
          color: tokens.colors.text.primary,
        }}
      >
        {t("chartTitle")}
      </h2>
      <ResponsiveContainer width="100%" height={350}>
        <AreaChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke={tokens.colors.border} />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 10, fill: tokens.colors.text.secondary }}
            tickFormatter={(value: string) => {
              const d = new Date(value);
              return `${d.getFullYear()}/${String(d.getMonth() + 1).padStart(2, "0")}`;
            }}
          />
          <YAxis
            tick={{ fontSize: 10, fill: tokens.colors.text.secondary }}
            label={{
              value: t("days"),
              angle: -90,
              position: "insideLeft",
              style: {
                fontSize: 10,
                fill: tokens.colors.text.secondary,
              },
            }}
          />
          <Tooltip />
          <Legend />
          <Area
            type="monotone"
            dataKey={t("cooperative")}
            stackId="1"
            stroke={tokens.colors.chart.cooperative}
            fill={tokens.colors.chart.cooperative}
            fillOpacity={0.8}
          />
          <Area
            type="monotone"
            dataKey={t("private")}
            stackId="1"
            stroke={tokens.colors.chart.private}
            fill={tokens.colors.chart.private}
            fillOpacity={0.8}
          />
          <Area
            type="monotone"
            dataKey={t("national")}
            stackId="1"
            stroke={tokens.colors.chart.national}
            fill={tokens.colors.chart.national}
            fillOpacity={0.8}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
