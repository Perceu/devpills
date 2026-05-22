/*
Condicionais em Go

if/else sem parênteses no bool
*/
package main

import "fmt"

func main() {
	idade := 18

	if idade >= 18 {
		fmt.Println("Maior de idade")
	} else {
		fmt.Println("Menor de idade")
	}

	nota := 85
	if nota >= 90 {
		fmt.Println("A")
	} else if nota >= 80 {
		fmt.Println("B")
	} else {
		fmt.Println("C")
	}
}
