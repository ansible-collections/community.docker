/*
  Copyright (c) Ansible Project
  GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
  SPDX-License-Identifier: GPL-3.0-or-later
*/

package main

import (
	"fmt"
	"os"
	"strconv"
)

func main() {
	healthy := true
	if len(os.Args) > 2 {
		fmt.Fprintf(os.Stderr, "%s must have 0 or 1 argument, not %d arguments\n", os.Args[0], len(os.Args))
		os.Exit(1)
	} else if len(os.Args) == 2 {
		var err error
		healthy, err = strconv.ParseBool(os.Args[1])
		if err != nil {
			fmt.Fprintf(os.Stderr, "Cannot parse boolean: %s\n", err)
			os.Exit(1)
		}
	}
	var state []byte
	if healthy {
		state = []byte("healthy")
	} else {
		state = []byte("unhealthy")
	}
	os.WriteFile("/health.txt", state, 0644)
}
