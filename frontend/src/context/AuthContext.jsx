import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for token in URL (OAuth callback)
    const urlParams = new URLSearchParams(window.location.search);
    const urlToken = urlParams.get('token');

    if (urlToken) {
      localStorage.setItem('token', urlToken);
      setToken(urlToken);
      // Clean up URL
      window.history.replaceState({}, document.title, window.location.pathname);
    }

    // Fetch user info if we have a token
    if (token || urlToken) {
      fetchUserInfo(urlToken || token);
    } else {
      setLoading(false);
    }
  }, []);

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

  const fetchUserInfo = async (authToken) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        // Token invalid, clear it
        localStorage.removeItem('token');
        setToken(null);
      }
    } catch (error) {
      console.error('Error fetching user info:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = () => {
    // Redirect to backend Google OAuth
    window.location.href = `${API_BASE_URL}/auth/google/login`;
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
