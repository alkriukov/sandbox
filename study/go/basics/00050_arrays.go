package main

import "fmt"

func main() {

	const arr1Len = 3
	var arr1 [arr1Len]int
	for index, value := range arr1 {
		arr1[index] = value + index
	}
	fmt.Printf("%v\n\n", arr1)

	const yLen = 5
	const xLen = 4
	var arr2 [yLen][xLen]int
	for i := 0; i < yLen; i++ {
		for j := 0; j < xLen; j++ {
			arr2[i][j] = i + j
			fmt.Printf("%v ", arr2[i][j])
		}
		fmt.Println()
	}

}
