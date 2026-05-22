/*
Structs em Go

Tipo composto para agrupar dados
*/
package main

import "fmt"

type Usuario struct {
	Nome  string
	Email string
	Idade int
}

func main() {
	user := Usuario{
		Nome:  "João",
		Email: "joao@email.com",
		Idade: 30,
	}

	fmt.Println("Nome:", user.Nome)
	fmt.Println("Email:", user.Email)

	user.Idade = 31
	fmt.Println("Idade:", user.Idade)
}
