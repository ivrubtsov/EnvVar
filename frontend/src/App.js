import React, { useEffect, useState } from 'react';
import axios from 'axios';

// React environment variables must be prefixed with REACT_APP_
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000';
const API_TIMEOUT = parseInt(process.env.REACT_APP_API_TIMEOUT || '30000');
const ENVIRONMENT = process.env.REACT_APP_ENVIRONMENT || 'development';

// Feature flags
const ENABLE_ANALYTICS = process.env.REACT_APP_ENABLE_ANALYTICS === 'true';
const ENABLE_DARK_MODE = process.env.REACT_APP_ENABLE_DARK_MODE === 'true';
const ENABLE_BETA_FEATURES = process.env.REACT_APP_ENABLE_BETA_FEATURES === 'true';

// External services
const GOOGLE_MAPS_API_KEY = process.env.REACT_APP_GOOGLE_MAPS_API_KEY;
const STRIPE_PUBLISHABLE_KEY = process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY;
const SENTRY_DSN = process.env.REACT_APP_SENTRY_DSN;
const GA_TRACKING_ID = process.env.REACT_APP_GA_TRACKING_ID;

// App configuration
const APP_VERSION = process.env.REACT_APP_VERSION || '1.0.0';
const BUILD_NUMBER = process.env.REACT_APP_BUILD_NUMBER;
const MAX_FILE_UPLOAD_SIZE = parseInt(process.env.REACT_APP_MAX_UPLOAD_SIZE || '10485760');

// API client configuration
const apiClient = axios.create({
  baseURL: API_URL,
  timeout: API_TIMEOUT,
  headers: {
    'X-Client-Version': APP_VERSION,
    'X-Environment': ENVIRONMENT
  }
});

// Add auth token from environment if available (for development)
const DEV_AUTH_TOKEN = process.env.REACT_APP_DEV_AUTH_TOKEN;
if (DEV_AUTH_TOKEN && ENVIRONMENT === 'development') {
  apiClient.defaults.headers.common['Authorization'] = `Bearer ${DEV_AUTH_TOKEN}`;
}

function App() {
  const [config, setConfig] = useState({
    apiUrl: API_URL,
    environment: ENVIRONMENT,
    version: APP_VERSION,
    features: {
      analytics: ENABLE_ANALYTICS,
      darkMode: ENABLE_DARK_MODE,
      betaFeatures: ENABLE_BETA_FEATURES
    }
  });

  useEffect(() => {
    // Initialize analytics if enabled
    if (ENABLE_ANALYTICS && GA_TRACKING_ID) {
      // Google Analytics initialization
      window.gtag('config', GA_TRACKING_ID);
    }

    // Initialize Sentry if configured
    if (SENTRY_DSN) {
      // Sentry initialization would go here
      console.log('Sentry initialized');
    }

    // Log build info in development
    if (ENVIRONMENT === 'development') {
      console.log('App Version:', APP_VERSION);
      console.log('Build Number:', BUILD_NUMBER);
      console.log('API URL:', API_URL);
    }
  }, []);

  const handleFileUpload = (file) => {
    if (file.size > MAX_FILE_UPLOAD_SIZE) {
      alert(`File size exceeds maximum allowed size of ${MAX_FILE_UPLOAD_SIZE / 1024 / 1024}MB`);
      return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    apiClient.post('/upload', formData)
      .then(response => {
        console.log('Upload successful:', response.data);
      })
      .catch(error => {
        console.error('Upload failed:', error);
      });
  };

  return (
    <div className="App">
      <h1>Environment Configuration Test</h1>
      <div>
        <h2>Configuration</h2>
        <pre>{JSON.stringify(config, null, 2)}</pre>
      </div>
      
      {STRIPE_PUBLISHABLE_KEY && (
        <div>
          <h3>Stripe Integration Available</h3>
          <button>Process Payment</button>
        </div>
      )}
      
      {GOOGLE_MAPS_API_KEY && (
        <div>
          <h3>Google Maps Available</h3>
          {/* Google Maps component would go here */}
        </div>
      )}
    </div>
  );
}

export default App;
