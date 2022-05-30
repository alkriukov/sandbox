package main

import (
	"fmt"
	"time"
)

func main() {
	i := 7
	if i%2 == 0 {
		fmt.Printf("%v is even\n", i)
	} else {
		fmt.Printf("%v is odd\n", i)
	}

	var start int = -5
	var end int = 10
	for num := start; num <= end; num++ {
		if num < 0 {
			fmt.Printf("%v is negative\n", num)
		} else if num <= 9 {
			fmt.Printf("%v has 1 digit\n", num)
		} else {
			fmt.Printf("%v has multiple digits\n", num)
		}
	}

	currentDayOfWeek := time.Now().Weekday()
	fmt.Printf("Today is %s. ", currentDayOfWeek)
	switch currentDayOfWeek {
	case time.Saturday, time.Sunday:
		fmt.Println("Let's go walk!")
	case time.Friday:
		fmt.Println("Let's work and then weekend")
	default:
		fmt.Println("Let's Work")
	}

}
