/*
Laços de repetição em Go

Go só tem for (nada de while/do)
*/
package main

import "fmt"

func main() {
	for i := 1; i <= 5; i++ {
		fmt.Println("Contagem:", i)
	}

	nomes := []string{"Alice", "Bob", "Carlos"}
	for index, nome := range nomes {
		fmt.Printf("%d - %s\n", index, nome)
	}

	numero := 1
	for numero <= 3 {
		fmt.Println("Loop:", numero)
		numero++
	}
}
