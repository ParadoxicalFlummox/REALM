package models

import (
	"time"
)
type User struct {
	ID       	uint			`gorm:"primaryKey"`
	Email    	string			`gorm:"unique;not null"`
	Password 	string			`gorm:"not null"`
	Properties 	[]Property 		`gorm:"foreignKey:OwnerID"`
	CreatedAt 	time:Time
	UpdatedAt 	time:Time
}
