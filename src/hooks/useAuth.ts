import { useState, useCallback } from 'react';

// Lightweight auth hook that wraps Privy when available,
// falls back to simple wallet connection state.
// Replace with Privy integration at deploy time.

interface AuthState {
  authenticated: boolean;
  ready: boolean;
  walletAddress: string | null;
  login: () => void;
  logout: () => void;
}

export function useAuth(): AuthState {
  const [authenticated, setAuthenticated] = useState(false);
  const [walletAddress, setWalletAddress] = useState<string | null>(null);

  const login = useCallback(async () => {
    // Try Solana wallet adapter
    if (typeof window !== 'undefined' && (window as any).solana) {
      try {
        const resp = await (window as any).solana.connect();
        setWalletAddress(resp.publicKey.toString());
        setAuthenticated(true);
        return;
      } catch {
        // User rejected
      }
    }

    // Fallback: demo mode
    setWalletAddress('demo-wallet');
    setAuthenticated(true);
  }, []);

  const logout = useCallback(() => {
    if (typeof window !== 'undefined' && (window as any).solana) {
      (window as any).solana.disconnect?.();
    }
    setAuthenticated(false);
    setWalletAddress(null);
  }, []);

  return {
    authenticated,
    ready: true,
    walletAddress,
    login,
    logout,
  };
}
