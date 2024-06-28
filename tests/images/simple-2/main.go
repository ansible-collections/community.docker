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
	var delay time.Duration
	if len(os.Args) > 2 {
		fmt.Fprintf(os.Stderr, "%s must have 0 or 1 argument, not %d arguments\n", os.Args[0], len(os.Args))
		os.Exit(1)
	} else if len(os.Args) == 2 {
		var err error
		delay, err = time.ParseDuration(os.Args[1])
		if err != nil {
			fmt.Fprintf(os.Stderr, "Cannot parse delay duration: %s\n", err)
			os.Exit(1)
		}
		if delay.Microseconds() < 0 {
			fmt.Fprintf(os.Stderr, "Delay must not be negative!\n")
			os.Exit(1)
		}
	}
	fmt.Println("World!")
	time.Sleep(delay)
}
