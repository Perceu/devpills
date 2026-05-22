/*
Goroutines e channels em Go

Concorrência nativa da linguagem
*/
package main

import (
	"fmt"
	"time"
)

func saudacao(nome string, ch chan string) {
	time.Sleep(100 * time.Millisecond)
	ch <- "Olá, " + nome
}

func main() {
	ch := make(chan string)

	go saudacao("Alice", ch)
	go saudacao("Bob", ch)

	msg1 := <-ch
	msg2 := <-ch

	fmt.Println(msg1)
	fmt.Println(msg2)
}
