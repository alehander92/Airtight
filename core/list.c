typedef struct %{list_type} {
	%{elem_type}* values;
	size_t length;
	size_t capacity;
} %{list_type};

%{list_type} h_append_%{list_type}_%{elem_type}_%{list_type}(%{list_type} list, %{elem_type} elem) {
	if(list.length + 1 > list.capacity) {
		list.capacity *= 2;
		list.values = (%{elem_type}*)realloc(list.values, sizeof(%{elem_type}) * list.capacity);
	}
	list.values[list.length] = elem;
	list.length++;
	return list;
}

%{list_type} h_pop_%{list_type}_%{elem_type}_%{list_type}(%{list_type} list, %{elem_type} elem) {
	list.length--;
	return list;
}

int h_length_%{list_type}_int(%{list_type} list) {
	return list.length;
}

%{elem_type} h_index_%{list_type}_int_%{elem_type}(%{list_type} list, int index) {
	return list.values[index];
}

%{list_type} h_slice_%{list_type}_int_int_%{list_type}(%{list_type} z, int from, int to) {
	%{list_type} list;
	list.values = (%{elem_type}*)malloc(sizeof(%{elem_type}) * (to - from));
	list.length = to - from;
	list.capacity = to - from;
	for(int j = from;j < to;j ++) {
		list.values[j - from] = z.values[j];
	}
	return list;
}

%{list_type} %{list_type}Of(size_t count, ...) {
	va_list ap;
	%{list_type} list;
	list.values = (%{elem_type}*)(malloc(sizeof(%{elem_type}) * (count + 1)));
	list.length = count;
	list.capacity = count + 1;
	va_start(ap, count);
	for(int j = 0;j < count;j ++) { list.values[j] = va_arg(ap, %{elem_type}); }
	return list;
}

HString h_str_%{list_type}_HString(%{list_type} list) {
	HString z = HStringFrom("[");

	for(int j = 0;j < list.length - 1;j ++) {
		z = h_add_HString_HString(z, h_str_%{elem_type}_HString(list.values[j]));
		z = h_add_HString_HString(z, HStringFrom(" "));
	}
	z = h_add_HString_HString(z, h_str_%{elem_type}_HString(list.values[list.length - 1]));
	z = h_add_HString_HString(z, HStringFrom("]"));
	return z;
}

HString h_print_%{list_type}_HString(%{list_type} list) {
	return h_prints_HString_HString(h_str_%{list_type}_HString(list));
}

int h_count_%{list_type}_%{elem_type}REFbool_int(%{list_type} list, bool(*z)(%{elem_type})) {
	int count = 0;
	for(int j = 0;j < list.length;j ++) {
		if((*z)(list.values[j])) {
			count++;
		}
	}
	return count;
}




