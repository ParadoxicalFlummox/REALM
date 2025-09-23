package middleware

import (
    "net/http"
    "strings"

    "github.com/gin-gonic/gin"
    "github.com/dgrijalva/jwt-go"
)

func AuthMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        tokenString := c.Request.Header.Get("Authorization")
        if tokenString == "" {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "Authorization header is required"})
            c.Abort()
            return
        }

        // Remove "Bearer " prefix
        tokenString = strings.TrimPrefix(tokenString, "Bearer ")

        claims := &jwt.StandardClaims{}
        token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
            return []byte("your_jwt_secret"), nil // Replace with your JWT secret
        })

        if err != nil || !token.Valid {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid token"})
            c.Abort()
            return
        }

        // Token is valid, proceed to the next handler
        c.Set("userID", claims.Subject)
        c.Next()
    }
}