package models

import (
	"time"
)

type financialRecord struct {
	ID          uint		`gorm:"primaryKey"`
	PropertyID	uint		`gorm:"not null"`
	UserID		uint		`gorm:"not null"`
	Type		string		`gorm:"not null"`
	Amount		float64		`gorm:"not null"`
	Date		time.Time	`gorm:"not null"`
	Note		string
	Property	Property	`gorm:"foreignKey:PropertyID"`
	User		User		`gorm:"foreignKey:UserID"`
	CreatedAt	time.Time
	UpdatedAt	time.Time
}
