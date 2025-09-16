package models

import (
	"time"
)

type User struct {
	ID         uint       `gorm:"primaryKey" json:"id"`
	Email      string     `gorm:"unique;not null" json:"email"`
	Password   string     `gorm:"not null" json:"password"`
	Properties []Property `gorm:"foreignKey:OwnerID" json:"properties"`
	CreatedAt  time.Time  `json:"created_at"`
	UpdatedAt  time.Time  `json:"updated_at"`
}
