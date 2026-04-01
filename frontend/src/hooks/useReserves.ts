import { useEffect, useState } from "react";
import type { ReserveRecord } from "../types/reserves";

const API_URL = import.meta.env.VITE_API_URL || "";

interface UseReservesResult {
  data: ReserveRecord[];
  latest: ReserveRecord | null;
  lastUpdated: string | null;
  loading: boolean;
  error: string | null;
}

export function useReserves(): UseReservesResult {
  const [data, setData] = useState<ReserveRecord[]>([]);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function fetchData() {
      try {
        const response = await fetch(`${API_URL}/v1/reserves`, {
          signal: controller.signal,
        });
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        const json = (await response.json()) as {
          data: ReserveRecord[];
          last_updated: string;
        };
        const sorted = json.data.sort(
          (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime(),
        );
        setData(sorted);
        setLastUpdated(json.last_updated);
      } catch (e) {
        if (e instanceof DOMException && e.name === "AbortError") return;
        setError(e instanceof Error ? e.message : "Unknown error");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
    return () => controller.abort();
  }, []);

  const latest = data.length > 0 ? data[data.length - 1]! : null;

  return { data, latest, lastUpdated, loading, error };
}
