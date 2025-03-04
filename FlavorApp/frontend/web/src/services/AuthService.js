import axios from 'axios';
import { firebaseConfig } from '../firebaseConfig';
import firebase from 'firebase/app';
import 'firebase/auth';

// Initialize Firebase
if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}

class AuthService {
  constructor() {
    this.apiBaseUrl = 'http://localhost:8000/api/auth/';  // Backend API URL
  }

  // Email/Password Registration
  async registerWithEmail(username, email, password) {
    try {
      const response = await axios.post(`${this.apiBaseUrl}register/`, {
        username,
        email,
        password
      });
      
      // Store token and user info
      this.setUserSession(response.data);
      return response.data;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  }

  // Email/Password Login
  async loginWithEmail(email, password) {
    try {
      const response = await axios.post(`${this.apiBaseUrl}login/`, {
        email,
        password
      });
      
      // Store token and user info
      this.setUserSession(response.data);
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  // Google Login
  async loginWithGoogle() {
    try {
      const provider = new firebase.auth.GoogleAuthProvider();
      const result = await firebase.auth().signInWithPopup(provider);
      
      // Get Firebase ID token
      const idToken = await result.user.getIdToken();
      
      // Send token to backend
      const response = await axios.post(`${this.apiBaseUrl}social-login/`, {
        provider: 'google',
        id_token: idToken
      });
      
      // Store token and user info
      this.setUserSession(response.data);
      return response.data;
    } catch (error) {
      console.error('Google login error:', error);
      throw error;
    }
  }

  // Facebook Login
  async loginWithFacebook() {
    try {
      const provider = new firebase.auth.FacebookAuthProvider();
      const result = await firebase.auth().signInWithPopup(provider);
      
      // Get Firebase ID token
      const idToken = await result.user.getIdToken();
      
      // Send token to backend
      const response = await axios.post(`${this.apiBaseUrl}social-login/`, {
        provider: 'facebook',
        id_token: idToken
      });
      
      // Store token and user info
      this.setUserSession(response.data);
      return response.data;
    } catch (error) {
      console.error('Facebook login error:', error);
      throw error;
    }
  }

  // Logout
  async logout() {
    try {
      // Logout from Firebase
      await firebase.auth().signOut();
      
      // Clear local storage
      this.clearUserSession();
    } catch (error) {
      console.error('Logout error:', error);
    }
  }

  // Store user session
  setUserSession(userData) {
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('token', userData.token);
  }

  // Clear user session
  clearUserSession() {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
  }

  // Check if user is authenticated
  isAuthenticated() {
    return !!localStorage.getItem('token');
  }

  // Get current user
  getCurrentUser() {
    return JSON.parse(localStorage.getItem('user'));
  }

  // Refresh user token
  async refreshToken() {
    try {
      const currentUser = firebase.auth().currentUser;
      if (currentUser) {
        const idToken = await currentUser.getIdToken(true);
        
        // Send new token to backend if needed
        const response = await axios.post(`${this.apiBaseUrl}refresh-token/`, {
          token: idToken
        });
        
        // Update local storage
        this.setUserSession(response.data);
        return response.data;
      }
    } catch (error) {
      console.error('Token refresh error:', error);
      throw error;
    }
  }
}

export default new AuthService();
