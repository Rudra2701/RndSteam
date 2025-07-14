//go:build windows

package main

import (
	"fmt"
	"os"
	"syscall"
	"unicode/utf16"
	"unsafe"
)

var (
	user32                   = syscall.NewLazyDLL("user32.dll")
	kernel32                 = syscall.NewLazyDLL("kernel32.dll")
	psapi                    = syscall.NewLazyDLL("psapi.dll")
	getForegroundWindow      = user32.NewProc("GetForegroundWindow")
	getWindowThreadProcessId = user32.NewProc("GetWindowThreadProcessId")
	openProcess              = kernel32.NewProc("OpenProcess")
	closeHandle              = kernel32.NewProc("CloseHandle")
	getModuleBaseNameW       = psapi.NewProc("GetModuleBaseNameW")
)

func getActiveApp() string {
	hwnd, _, _ := getForegroundWindow.Call()
	if hwnd == 0 {
		return "Unknown"
	}
	var pid uint32
	getWindowThreadProcessId.Call(hwnd, uintptr(unsafe.Pointer(&pid)))

	const PROCESS_QUERY_INFORMATION = 0x0400
	const PROCESS_VM_READ = 0x0010
	hProcess, _, _ := openProcess.Call(PROCESS_QUERY_INFORMATION|PROCESS_VM_READ, 0, uintptr(pid))
	if hProcess == 0 {
		return "Unknown"
	}
	defer closeHandle.Call(hProcess)

	var exeName [260]uint16
	getModuleBaseNameW.Call(hProcess, 0, uintptr(unsafe.Pointer(&exeName[0])), uintptr(len(exeName)))
	return UTF16ToString(exeName[:])
}

func UTF16ToString(s []uint16) string {
	n := 0
	for n < len(s) && s[n] != 0 {
		n++
	}
	return string(utf16.Decode(s[:n]))
}

func main() {
	activeApp := getActiveApp()
	usageFile := "usage.txt"
	usage := make(map[string]int)

	// Read existing usage
	data, _ := os.ReadFile(usageFile)
	lines := string(data)
	for _, line := range splitLines(lines) {
		var name string
		var minutes int
		fmt.Sscanf(line, "%s %d", &name, &minutes)
		usage[name] = minutes
	}

	// Add 1 minute to current app
	usage[activeApp] += 1

	// Write updated usage
	file, _ := os.Create(usageFile)
	defer file.Close()
	for app, mins := range usage {
		fmt.Fprintf(file, "%s %d\n", app, mins)
	}
}

func splitLines(text string) []string {
	var lines []string
	current := ""
	for _, r := range text {
		if r == '\n' || r == '\r' {
			if current != "" {
				lines = append(lines, current)
				current = ""
			}
		} else {
			current += string(r)
		}
	}
	if current != "" {
		lines = append(lines, current)
	}
	return lines
}
