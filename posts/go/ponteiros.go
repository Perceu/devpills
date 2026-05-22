/*
Ponteiros em Go

Referência direta à memória
*/
package main

import "fmt"

func main() {
	numero := 42
	ptr := &numero

	fmt.Println("Valor:", numero)
	fmt.Println("Endereço:", ptr)
	fmt.Println("Via ponteiro:", *ptr)

	*ptr = 100
	fmt.Println("Novo valor:", numero)

	// Ponteiro nil
	var p *int
	fmt.Println("Ponteiro nil:", p)
}
