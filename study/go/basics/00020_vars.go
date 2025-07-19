package main

import (
	"fmt"
)

func main() {
	var hello = "Hello"
	world := " world"
	fmt.Println(hello + world)

	var i, j int = 1, 2
	fmt.Println(i + j)

	var my_byte byte = 'a'
	const my_heart rune = '♥'
	fmt.Printf("%c = %d and %c = %U\n", my_byte, my_byte, my_heart, my_heart)

	const d = true
	fmt.Println(d)

	var f int
	var g = '\n'
	fmt.Println(f, g)
}
