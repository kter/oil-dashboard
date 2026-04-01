import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { ReserveCard } from "../components/ReserveCard";

vi.mock("react-i18next", () => ({
  useTranslation: () => ({
    t: (key: string, opts?: { count?: number }) => {
      if (key === "daysUnit" && opts?.count !== undefined)
        return `${opts.count} 日`;
      return key;
    },
    i18n: { language: "ja", changeLanguage: vi.fn() },
  }),
}));

describe("ReserveCard", () => {
  it("renders label and days", () => {
    render(<ReserveCard label="国家備蓄" days={133} color="#0017C1" />);
    expect(screen.getByText("国家備蓄")).toBeInTheDocument();
    expect(screen.getByText("133 日")).toBeInTheDocument();
  });

  it("renders with different values", () => {
    render(<ReserveCard label="民間備蓄" days={85} color="#3460FB" />);
    expect(screen.getByText("民間備蓄")).toBeInTheDocument();
    expect(screen.getByText("85 日")).toBeInTheDocument();
  });
});
