/*
  Copyright (c) Ansible Project
  GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
  SPDX-License-Identifier: GPL-3.0-or-later
*/

package main

import (
	"bytes"
	"fmt"
	"os"
)

func main() {
	data, err := os.ReadFile("/health.txt")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error while reading health status: %s\n", err)
		os.Exit(1)
	}
	if bytes.Equal(data, []byte("healthy")) {
		fmt.Fprintf(os.Stdout, "Healthy.\n")
		os.Exit(0)
	}
	if bytes.Equal(data, []byte("unhealthy")) {
		fmt.Fprintf(os.Stdout, "Unhealthy!\n")
		os.Exit(1)
	}
	if bytes.Equal(data, []byte("starting")) {
		fmt.Fprintf(os.Stdout, "Starting...\n")
		os.Exit(1)
	}
	fmt.Fprintf(os.Stderr, "Unknown health status: %s\n", data)
	os.Exit(1)
}
