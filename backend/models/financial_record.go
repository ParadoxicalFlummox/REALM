package models

import (
	"time"
)

type FinancialRecord struct {
	ID         uint      `gorm:"primaryKey"`
	PropertyID uint      `gorm:"not null"`
	UserID     uint      `gorm:"not null"`
	Type       string    `gorm:"not null"`
	Amount     float64   `gorm:"not null"`
	Date       time.Time `gorm:"not null"`
	Note       string
	Property   Property  `gorm:"foreignKey:PropertyID"`
	User       User      `gorm:"foreignKey:UserID"`
	CreatedAt  time.Time `json:"created_at"`
	UpdatedAt  time.Time `json:"updated_at"`
}
