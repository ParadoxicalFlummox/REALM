package initializers

import (
	"github.com/joho/godotenv"
)

// LoadEnv loads environment variables from a file (optional).
// It returns an error to the caller so the caller can decide how to handle it.
func LoadEnv(path string) error {
	return godotenv.Load(path)
}
