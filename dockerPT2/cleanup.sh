#!/bin/bash
# Cleanup script to delete directories older than 2 hours in /tmp
find /tmp -mindepth 1 -mmin +120 -type d -exec rm -rf {} +
