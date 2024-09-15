DIR_FONTS = ./Fonts
DIR_OBJ = ./obj
DIR_BIN = ./bin

OBJ_C = $(wildcard ${DIR_FONTS}/*.c ${DIR_OBJ}/*.c)
OBJ_O = $(patsubst %.c,${DIR_BIN}/%.o,$(notdir ${OBJ_C}))

TARGET = main
#BIN_TARGET = ${DIR_BIN}/${TARGET}

CC = gcc

DEBUG = -g -O0 -Wall
CFLAGS += $(DEBUG) 

LIB = 

${TARGET}:${OBJ_O}
	$(CC) $(CFLAGS) $(OBJ_O) -o $@  $(LIB)

${DIR_BIN}/%.o : $(DIR_OBJ)/%.c
	$(CC) $(CFLAGS) -c  $< -o $@  $(LIB)

${DIR_BIN}/%.o:$(DIR_FONTS)/%.c
	$(CC) $(CFLAGS) -c  $< -o $@  $(LIB)
	
clean :
	rm $(DIR_BIN)/*.* 
	rm $(TARGET) 