/*
Funções em Go

Múltiplos retornos e tipos definidos
*/
package main

import "fmt"

func somar(a int, b int) int {
	return a + b
}

func dividir(a, b float64) (float64, error) {
	if b == 0 {
		return 0, fmt.Errorf("divisão por zero")
	}
	return a / b, nil
}

func main() {
	fmt.Println("Soma:", somar(10, 5))

	resultado, err := dividir(10, 3)
	if err == nil {
		fmt.Printf("Divisão: %.2f\n", resultado)
	}
}
