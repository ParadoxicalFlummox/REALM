package main

import 

func init() {
	initalizers.ConnectToDB
	initalizers.LoadEnvVariables
}

func main() {
	initalizers.DB.AutoMigrate(&models.post{})
}
