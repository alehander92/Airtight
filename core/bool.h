


#include H_BOOL_H
#define H_BOOL_H
#include<stdbool.h>

typedef struct HCoreBool {
	bool _value;
} HCoreBool;

HCoreBool* HCoreTrue = (HCoreBool*)malloc(sizeof(HCoreBool));
HCoreBool* HCoreFalse = (HCoreBool*)malloc(sizeof(HCoreBool));

HCoreTrue->_value = true;
HCoreFalse->_value = false;

HBool* h_bool(bool value);

#define HBool HCoreBool
#define HTrue HCoreTrue
#define HFalse HCoreFalse;
#endif
