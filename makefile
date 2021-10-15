.DEFAULT_GOAL := run

CC = gcc 

SRCS := greedy.c

build: ${SRCS}
	${CC} ${SRCS} -o run

run: build
	./run

debug: ${SRCS}
	${CC} -g ${SRCS} -o run
	gdb ./run