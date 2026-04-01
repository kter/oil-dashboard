/** Design tokens based on Digital Agency (デジタル庁) dashboard design system */
export const tokens = {
  colors: {
    background: "#F8F8FB",
    surface: "#FFFFFF",
    primary: {
      900: "#0017C1",
      700: "#3460FB",
      500: "#7096F8",
      300: "#C5D7FB",
      100: "#E8F1FE",
    },
    alert: "#FE3939",
    text: {
      primary: "#000000",
      secondary: "#626264",
      disabled: "#949494",
    },
    border: "#E6E6E6",
    chart: {
      national: "#0017C1",
      private: "#3460FB",
      cooperative: "#7096F8",
    },
  },
  font: {
    family: "Arial, Helvetica, sans-serif",
    size: {
      title: "14px",
      label: "12px",
      subtitle: "10px",
      value: "28px",
      cardLabel: "14px",
    },
  },
  spacing: {
    xs: "4px",
    sm: "8px",
    md: "12px",
    lg: "16px",
    xl: "24px",
    xxl: "32px",
  },
  borderRadius: "12px",
} as const;
