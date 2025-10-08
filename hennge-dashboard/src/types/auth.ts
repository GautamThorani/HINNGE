export interface UserLogin {
  email: string;
  password: string;
}

export interface UserRegistration {
  email: string;
  password: string;
  full_name: string; 
}

export interface Token {
  access_token: string;
  token_type: string;
  expires_in: number;
  requires_mfa: boolean;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  token?: Token;
}

export interface TokenData {
  user_id: string;
  email: string;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  created_at: string;
  is_active: boolean;
}