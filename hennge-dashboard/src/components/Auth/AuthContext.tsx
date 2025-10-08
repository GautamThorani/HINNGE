import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../../services/api';
import type { TokenData, User } from '../../types/auth';

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  login: (token: string, userData: TokenData) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('auth_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      const storedToken = localStorage.getItem('auth_token');
      if (storedToken) {
        try {
          const validation = await authAPI.validateToken(storedToken);
          if (validation.valid) {
            setIsAuthenticated(true);
            setToken(storedToken);
            
            try {
              const userData = await authAPI.getCurrentUser();
              setUser(userData);
            } catch (userError) {
              console.error('Failed to fetch user data:', userError);
              // Even if user data fails, keep the user authenticated with token
              // Set basic user data from token
              setUser({
                id: validation.user.user_id,
                email: validation.user.email,
                full_name: validation.user.email, // Fallback
                created_at: new Date().toISOString(),
                is_active: true
              });
            }
          } else {
            // Token is invalid, clear it
            localStorage.removeItem('auth_token');
            setIsAuthenticated(false);
            setToken(null);
            setUser(null);
          }
        } catch (error) {
          console.error('Token validation error:', error);
          // If token validation fails, clear everything
          localStorage.removeItem('auth_token');
          setIsAuthenticated(false);
          setToken(null);
          setUser(null);
        }
      } else {
        // No token found
        setIsAuthenticated(false);
        setToken(null);
        setUser(null);
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (newToken: string, userData: TokenData) => {
    localStorage.setItem('auth_token', newToken);
    setToken(newToken);
    setIsAuthenticated(true);
    
    try {
      const fullUserData = await authAPI.getCurrentUser();
      setUser(fullUserData);
    } catch (error) {
      console.error('Failed to fetch user data after login:', error);
      setUser({
        id: userData.user_id,
        email: userData.email,
        full_name: userData.email, 
        created_at: new Date().toISOString(),
        is_active: true
      });
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    setToken(null);
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};