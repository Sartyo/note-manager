import { jwtDecode } from "jwt-decode";

export interface JwtPayload {
  exp: number;
  [key: string]: any;
}

export function getTokenExpiration(token: string): number | null {
  try {
    const decoded = jwtDecode<JwtPayload>(token);
    return decoded.exp ? decoded.exp * 1000 : null; // convert to ms
  } catch {
    return null;
  }
}
