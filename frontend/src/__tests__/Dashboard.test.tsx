import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { Dashboard } from "../components/Dashboard";

vi.mock("react-i18next", () => ({
  useTranslation: () => ({
    t: (key: string, opts?: { count?: number }) => {
      const translations: Record<string, string> = {
        title: "日本の石油備蓄量",
        national: "国家備蓄",
        private: "民間備蓄",
        cooperative: "産油国協働備蓄",
        loading: "読み込み中...",
        error: "データの取得に失敗しました",
        lastUpdated: "最終更新",
        chartTitle: "石油備蓄量の推移（日数）",
        days: "日",
        language: "言語",
      };
      if (key === "daysUnit" && opts?.count !== undefined)
        return `${opts.count} 日`;
      return translations[key] ?? key;
    },
    i18n: { language: "ja", changeLanguage: vi.fn() },
  }),
}));

const mockUseReserves = vi.fn();
vi.mock("../hooks/useReserves", () => ({
  useReserves: () => mockUseReserves(),
}));

describe("Dashboard", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows loading state", () => {
    mockUseReserves.mockReturnValue({
      data: [],
      latest: null,
      lastUpdated: null,
      loading: true,
      error: null,
    });

    render(<Dashboard />);
    expect(screen.getByText("読み込み中...")).toBeInTheDocument();
  });

  it("shows error state", () => {
    mockUseReserves.mockReturnValue({
      data: [],
      latest: null,
      lastUpdated: null,
      loading: false,
      error: "Network error",
    });

    render(<Dashboard />);
    expect(screen.getByText("データの取得に失敗しました")).toBeInTheDocument();
  });

  it("renders dashboard with data", () => {
    const mockData = [
      {
        date: "2026-03-01",
        national_days: 133,
        private_days: 85,
        cooperative_days: 5,
        total_days: 223,
      },
    ];

    mockUseReserves.mockReturnValue({
      data: mockData,
      latest: mockData[0],
      lastUpdated: "2026-03-15",
      loading: false,
      error: null,
    });

    render(<Dashboard />);
    expect(screen.getByText("日本の石油備蓄量")).toBeInTheDocument();
    expect(screen.getByText("国家備蓄")).toBeInTheDocument();
    expect(screen.getByText("133 日")).toBeInTheDocument();
    expect(screen.getByText("85 日")).toBeInTheDocument();
    expect(screen.getByText("5 日")).toBeInTheDocument();
  });
});
