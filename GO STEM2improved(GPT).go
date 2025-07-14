package main

import (
    "bufio"
    "context"
    "fmt"
    "os"
    "os/signal"
    "strconv"
    "syscall"
    "time"
)

func main() {
    reader := bufio.NewReader(os.Stdin)
    fmt.Print("Enter screen time limit in minutes: ")
    text, _ := reader.ReadString('\n')
    text = text[:len(text)-1]
    limitMin, err := strconv.Atoi(text)
    if err != nil || limitMin <= 0 {
        fmt.Println("Invalid input.")
        return
    }

    totalSec := limitMin * 60
    ctx, cancel := context.WithTimeout(context.Background(), time.Duration(totalSec)*time.Second)
    defer cancel()

    ticker := time.NewTicker(1 * time.Second)
    defer ticker.Stop()

    done := make(chan os.Signal, 1)
    signal.Notify(done, os.Interrupt, syscall.SIGTERM)

    elapsed := 0
    fmt.Printf("Timer started: %d minutes.\n", limitMin)

    for {
        select {
        case <-ctx.Done():
            fmt.Println("\nScreen time limit reached!")
            forceQuit()
            return
        case <-ticker.C:
            elapsed++
            if elapsed%(60) == 0 {
                fmt.Printf("Elapsed: %d min / %d min\n", elapsed/60, limitMin)
            }
        case <-done:
            fmt.Println("\nInterrupted! Exiting early.")
            return
        }
    }
}

// forceQuit attempts to log out or kill the process to enforce stop
func forceQuit() {
    fmt.Println("Exiting now. Goodbye!")
    os.Exit(0)
}
