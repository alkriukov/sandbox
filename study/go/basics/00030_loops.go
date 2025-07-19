package main

import "fmt"

func main() {
	i := 0
	for i < 5 {
		fmt.Printf("%v %T\n", i, i)
		i += 1
	}

	for {
		fmt.Printf("%s\n", "loop")
		break
	}

	for j := 1; j < 10; j += 2 {
		fmt.Printf("%v\n", j)
	}
}
