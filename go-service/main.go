package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/gorilla/mux"
	"github.com/joho/godotenv"
)

type Config struct {
	Port           string
	Host           string
	Environment    string
	
	// Database
	DatabaseURL    string
	DatabaseDriver string
	MaxConnections int
	
	// Redis
	RedisHost      string
	RedisPort      string
	RedisPassword  string
	RedisDB        int
	
	// API Keys
	StripeAPIKey   string
	TwilioSID      string
	TwilioToken    string
	
	// Monitoring
	DatadogAPIKey  string
	DatadogAppKey  string
	
	// Feature Flags
	EnableMetrics  bool
	EnableTracing  bool
	
	// Timeouts
	ReadTimeout    time.Duration
	WriteTimeout   time.Duration
}

func loadConfig() *Config {
	// Load .env file if exists
	godotenv.Load()
	
	// Parse integer values
	maxConn, _ := strconv.Atoi(getEnv("MAX_DB_CONNECTIONS", "25"))
	redisDB, _ := strconv.Atoi(getEnv("REDIS_DB", "0"))
	
	// Parse durations
	readTimeout, _ := strconv.Atoi(getEnv("READ_TIMEOUT_SECONDS", "30"))
	writeTimeout, _ := strconv.Atoi(getEnv("WRITE_TIMEOUT_SECONDS", "30"))
	
	// Parse booleans
	enableMetrics := getEnv("ENABLE_METRICS", "true") == "true"
	enableTracing := getEnv("ENABLE_TRACING", "false") == "true"
	
	return &Config{
		Port:           getEnv("GO_SERVICE_PORT", "8080"),
		Host:           getEnv("GO_SERVICE_HOST", "0.0.0.0"),
		Environment:    getEnv("GO_ENV", "development"),
		
		DatabaseURL:    os.Getenv("DATABASE_URL"),
		DatabaseDriver: getEnv("DATABASE_DRIVER", "postgres"),
		MaxConnections: maxConn,
		
		RedisHost:     getEnv("REDIS_HOST", "localhost"),
		RedisPort:     getEnv("REDIS_PORT", "6379"),
		RedisPassword: os.Getenv("REDIS_PASSWORD"),
		RedisDB:       redisDB,
		
		StripeAPIKey:  os.Getenv("STRIPE_API_KEY"),
		TwilioSID:     os.Getenv("TWILIO_ACCOUNT_SID"),
		TwilioToken:   os.Getenv("TWILIO_AUTH_TOKEN"),
		
		DatadogAPIKey: os.Getenv("DATADOG_API_KEY"),
		DatadogAppKey: os.Getenv("DATADOG_APP_KEY"),
		
		EnableMetrics: enableMetrics,
		EnableTracing: enableTracing,
		
		ReadTimeout:  time.Duration(readTimeout) * time.Second,
		WriteTimeout: time.Duration(writeTimeout) * time.Second,
	}
}

func getEnv(key, defaultValue string) string {
	value := os.Getenv(key)
	if value == "" {
		return defaultValue
	}
	return value
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	env := os.Getenv("GO_ENV")
	version := getEnv("APP_VERSION", "1.0.0")
	
	response := fmt.Sprintf(`{"status":"ok","environment":"%s","version":"%s"}`, env, version)
	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(response))
}

func main() {
	config := loadConfig()
	
	// Validate required variables
	if config.DatabaseURL == "" {
		log.Fatal("DATABASE_URL is required")
	}
	
	router := mux.NewRouter()
	router.HandleFunc("/health", healthHandler).Methods("GET")
	
	// Configure server
	addr := fmt.Sprintf("%s:%s", config.Host, config.Port)
	server := &http.Server{
		Addr:         addr,
		Handler:      router,
		ReadTimeout:  config.ReadTimeout,
		WriteTimeout: config.WriteTimeout,
	}
	
	log.Printf("Starting server on %s in %s mode", addr, config.Environment)
	
	// TLS configuration
	tlsCertFile := os.Getenv("TLS_CERT_FILE")
	tlsKeyFile := os.Getenv("TLS_KEY_FILE")
	
	if tlsCertFile != "" && tlsKeyFile != "" {
		log.Fatal(server.ListenAndServeTLS(tlsCertFile, tlsKeyFile))
	} else {
		log.Fatal(server.ListenAndServe())
	}
}
