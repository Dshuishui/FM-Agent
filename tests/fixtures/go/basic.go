package basic

import "fmt"

// Add returns the sum of two integers.
func Add(a, b int) int {
	return a + b
}

// subtract is unexported.
func subtract(a, b int) int {
	return a - b
}

// MultiReturn returns two values.
func MultiReturn(x int) (int, error) {
	if x < 0 {
		return 0, fmt.Errorf("negative")
	}
	return x * 2, nil
}

// Counter is a struct with methods.
type Counter struct {
	count int
}

// Increment is a method with a value receiver.
func (c Counter) Increment() Counter {
	c.count++
	return c
}

// Reset is a method with a pointer receiver.
func (c *Counter) Reset() {
	c.count = 0
}

// noParams takes no arguments.
func noParams() {
	fmt.Println("hello")
}

// funcInComment is NOT a function — only appears in a comment:
// func fakeInComment() {}
