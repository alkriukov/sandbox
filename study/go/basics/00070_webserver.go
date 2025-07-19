package main

import (
	"fmt"
	"net/http"
)

func homePage(w http.ResponseWriter, r *http.Request) {
	fmt.Println(r.Method, r.URL)
	fmt.Fprintf(w, "Hello World")
}

func handleRequests() {
	http.HandleFunc("/", homePage)
	http.ListenAndServe(":9000", nil)
}

func main() {
	handleRequests()
}
