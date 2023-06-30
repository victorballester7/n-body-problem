# Description: Makefile for the project

# Compiler and flags
CC := gcc
CFLAGS := -Wall -Wextra -pedantic -std=c11 -fPIC

# Libraries
LIBS := -lm

# Folders
SRC := src
INCLUDE := include
BIN := bin
LIB_FOLDER := libs

# Executable name
TARGET := n-body_field

# We create a list of all the sources by looking for all the .c files
SOURCES := $(wildcard $(SRC)/*.c)

# We create a list of object files by replacing the .c extension with .o in the list of sources
OBJECTS := $(patsubst $(SRC)/%.c,$(BIN)/%.o,$(SOURCES))

# We need to tell the compiler where to find the headers
HEADERS := $(wildcard $(INCLUDE)/*.h)

# .PHONY target specifies that all and clean are not real files, but are just targets that don't produce output files.
.PHONY: all clean

# Default target
all: $(LIB_FOLDER)/lib_$(TARGET).so

# We compile the .c files into object files
$(BIN)/%.o: $(SRC)/%.c 
	@$(CC) $(CFLAGS) -I$(INCLUDE) -c $< -o $@ $(LIBS)

# We create the shared library by linking all the object files
$(LIB_FOLDER)/lib_$(TARGET).so: $(OBJECTS)
	@$(CC) $(CFLAGS) -shared $^ -o $@ $(LIBS)

clean:
	@rm -f $(BIN)/*.o $(LIB_FOLDER)/lib$(TARGET).so
