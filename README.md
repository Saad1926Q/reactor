# Reactor Pattern in Python

Implementing the reactor pattern in Python as a learning exercise, based on [this blog post](https://r4nd0m6uy.ch/event-driven-programming-with-the-reactor-pattern.html).

## Goal

Watch multiple named pipes for incoming data and print whatever arrives to the screen. Exit cleanly on CTRL+C.

## Approach

We use the reactor pattern - a single event loop that registers all pipe file descriptors with `select()` and blocks until the OS signals that one of them has data. At that point the relevant handler is called to read and print the data, then the loop goes back to waiting. This way the program uses no CPU while idle and reacts immediately when data arrives.
