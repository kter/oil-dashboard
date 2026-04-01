export interface ReserveRecord {
  date: string;
  national_days: number;
  private_days: number;
  cooperative_days: number;
  total_days: number;
}

export interface ReservesResponse {
  data: ReserveRecord[];
  last_updated: string;
}

export interface LatestReservesResponse {
  data: ReserveRecord;
  last_updated: string;
}
