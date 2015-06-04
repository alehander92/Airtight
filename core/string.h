


#ifndef H_STRING_H
#define H_STRING_H

#include<string.h>
#include<stddef.h>
#include "int.h"

typedef struct HCoreString {
    char* _value;
    size_t _length;
} HCoreString;

#define HString HCoreString

HInt length(HString* self);

#endif
