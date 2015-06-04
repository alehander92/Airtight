#ifndef H_FILE_H
#define H_FILE_H

#include<stdio.h>
#include "string.h"
#include "bool.h"

typedef struct HCoreFileMode {
	char[4] _file_mode;
} HCoreFileMode;

typedef struct HCoreFile {
	File* _handler;
} HCoreFile;

HCoreFileMode* HCoreREAD = (HCoreFileMode*)malloc(sizeof(HCoreFileMode));
HCoreREAD->_file_mode = "r";
HCoreFileMode* HCoreREAD_AND_WRITE = (HCoreFileMode*)malloc(sizeof(HCoreFileMode));
HCoreREAD_AND_WRITE->_file_mode = "r+";
HCoreFileMode* HCoreWRITE = (HCoreFileMode*)malloc(sizeof(HCoreFileMode));
HCoreWRITE->_file_mode = "w";

HCoreFile* open(HString* filename, HCoreFileMode* mode);
HBool* close(HCoreFile* self);

#endif
