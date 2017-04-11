#!/bin/sh
env $(cat variables-dev.env | xargs) $@ 
