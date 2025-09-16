package initializers

import (
	"errors"
	"os"
)

// Config holds runtime configuration values for the application.
type Config struct {
	DSN       string
	JWTSecret string
	Port      string
}

// NewConfigFromEnv builds a Config from environment variables and validates required fields.
func NewConfigFromEnv() (*Config, error) {
	cfg := &Config{
		DSN:       os.Getenv("DB_CREDS"),
		JWTSecret: os.Getenv("JWT_SECRET"),
		Port:      os.Getenv("PORT"),
	}
	if cfg.DSN == "" {
		return nil, errors.New("DB_CREDS is required")
	}
	if cfg.JWTSecret == "" {
		// not fatal for local dev, but warn the caller by returning an error
		return nil, errors.New("JWT_SECRET is recommended for token signing")
	}
	if cfg.Port == "" {
		cfg.Port = "8080"
	}
	return cfg, nil
}
