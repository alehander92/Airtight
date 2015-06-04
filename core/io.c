#include "io.h"
#include "bool.h"
#include "string.h"
#include "stdbool.h"



/* Core file operations
*/
HCoreFile* open(HString* filename, HCoreFileMode* mode) {
	char file_mode[4];

	File* handler = fopen(filename->_value, mode->_file_mode);
	HCoreFile* file = (HCoreFile*)malloc(sizeof(HCoreFile));
	file->_handler = handler;
	file->mode = mode;
	return file;
}

HBool* close(HCoreFile* self) {
	return h_bool(fclose(self->_handler) == 0);
}
