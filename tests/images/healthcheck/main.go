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
	if len(os.Args) > 3 || len(os.Args) < 2 {
		fmt.Fprintf(os.Stderr, "%s must have 1 or 2 arguments, not %d arguments\n", os.Args[0], len(os.Args))
		os.Exit(1)
	}
	runtimeDelay, err := time.ParseDuration(os.Args[1])
	if err != nil {
		fmt.Fprintf(os.Stderr, "Cannot parse runtime duration: %s\n", err)
		os.Exit(1)
	}
	if runtimeDelay.Microseconds() <= 0 {
		fmt.Fprintf(os.Stderr, "Delay must be positive!\n")
		os.Exit(1)
	}
	var healthyDelay time.Duration
	if len(os.Args) == 3 {
		healthyDelay, err = time.ParseDuration(os.Args[2])
		if err != nil {
			fmt.Fprintf(os.Stderr, "Cannot parse healthy delay: %s\n", err)
			os.Exit(1)
		}
		if healthyDelay.Microseconds() <= 0 {
			fmt.Fprintf(os.Stderr, "Healthy delay must not be negative!\n")
			os.Exit(1)
		}
	}
	if healthyDelay.Microseconds() > 0 {
		fmt.Fprintf(os.Stderr, "Waiting %s until setting to healthy...\n", healthyDelay)
		time.Sleep(healthyDelay)
		os.WriteFile("/health.txt", []byte("healthy"), 0644)
		fmt.Fprintf(os.Stderr, "Set state to healthy.\n")
	}
	fmt.Fprintf(os.Stderr, "Waiting %s until quitting...\n", runtimeDelay)
	time.Sleep(runtimeDelay)
	fmt.Fprintf(os.Stderr, "Goodbye.\n")
}
