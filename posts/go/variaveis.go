/*
Declarando variáveis em Go

Go tem tipagem estática com inferência
*/
package main

import "fmt"

func main() {
	var nome string = "DevPills"
	linguagem := "Go"
	ano := 2025
	ativo := true

	fmt.Println("Nome:", nome)
	fmt.Println("Linguagem:", linguagem)
	fmt.Println("Ano:", ano)
	fmt.Println("Ativo:", ativo)
}
