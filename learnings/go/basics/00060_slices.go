package main

import (
	"fmt"
	"strings"
)

func main() {
	var slices1 []string
	fmt.Printf("%v %v %v %T\n", slices1, len(slices1), cap(slices1), slices1)
	slices1 = append(slices1, "a")
	slices1 = append(slices1, "bb")
	slices1 = append(slices1, "ccc")
	slices1 = append(slices1, "dddd")
	fmt.Printf("%v\n", slices1)

	var slices2 = make([]string, len(slices1))
	copy(slices2, slices1)
	fmt.Printf("%v\n", slices2)

	s3 := slices2[:2]
	fmt.Printf("%v\n", s3)
	s4 := slices2[1:3]
	fmt.Printf("%v\n", s4)
	s5 := slices2[2:]
	fmt.Printf("%v\n", s5)

	lines := strings.Split("a b\nc\nd", "\n")
	fmt.Printf("Lines: %v %v %T\n", len(lines), cap(lines), lines)

	slice2d := make([][]int, 3)
	for i := 0; i < len(slice2d); i++ {
		slice2d[i] = make([]int, i)
	}

}
