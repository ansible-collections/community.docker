/*
  Copyright (c) Ansible Project
  GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
  SPDX-License-Identifier: GPL-3.0-or-later
*/

package main

import (
	"fmt"
	"os"
	"time"
)

func main() {
	os.WriteFile("health.txt", []byte("starting"), 0644)
	if len(os.Args) != 2 {
		fmt.Fprintf(os.Stderr, "%s must have 1 argument, not %d arguments\n", os.Args[0], len(os.Args))
		os.Exit(1)
	}
	delay, err := time.ParseDuration(os.Args[1])
	if err != nil {
		fmt.Fprintf(os.Stderr, "Cannot parse delay duration: %s\n", err)
		os.Exit(1)
	}
	if delay.Microseconds() <= 0 {
		fmt.Fprintf(os.Stderr, "Delay must be positive!\n")
		os.Exit(1)
	}
	time.Sleep(delay)
}
