#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

typedef enum {
    STRING,
	NUMBER
} VALUE_TYPE;

struct String {
	char* data;
	unsigned size, capacity;
};

void string_resize(struct String* array, unsigned size) {
	char* new_data = (char*)malloc(sizeof(char) * size);
	for (unsigned i = 0u; i < array->size; i++) {
		i[new_data] = i[array->data];
	}

	free(array->data);
	array->data = new_data;
	array->capacity = size;
}

struct String* string_constructor(unsigned size) {
	struct String* array = (struct String*)malloc(sizeof(struct String));
	array->data = NULL;
	array->size = 0u;
	string_resize(array, size);
	return array;
}

void string_destructor(struct String* array) {
	free(array->data);
	free(array);
}

void string_push(struct String* array, char value) {
	unsigned new_capacity = (array->capacity ? array->capacity * 2 : 1);
	if (array->capacity == array->size) {
		string_resize(array, new_capacity);
	}
	array->data[array->size++] = value;
}

struct kv {
    struct String* key;
    void* value;
    VALUE_TYPE value_type;
};

struct kv* kv_constructor(struct String* key, void* value, VALUE_TYPE value_type) {
    struct kv* new_kv = (struct kv*)malloc(sizeof(struct kv));

    new_kv->key = string_constructor(key->size);
    strcpy(new_kv->key->data, key->data);

    if (value_type == NUMBER) {
        int* new_int_value = (int*)malloc(sizeof(int));
        *new_int_value = *((int*)(value));
        new_kv->value = (void*)(new_int_value);
    } else {
        struct String* given_string_value = (struct String*)value;
        struct String* new_string_value = string_constructor(given_string_value->size);
        strcpy(new_string_value->data, given_string_value->data);
	new_string_value->size = given_string_value->size;
	new_string_value->capacity = given_string_value->capacity;
        new_kv->value = (void*)(new_string_value);
    }

    new_kv->value_type = value_type;
    return new_kv;
}

void kv_destructor(struct kv* kv) {
    string_destructor(kv->key);
    if (kv->value_type == NUMBER) {
        free((int*)(kv->value));
    } else {
        string_destructor((struct String*)(kv->value));
    }
    free(kv);
}

int* kv_number_value(struct kv* kv) {
    if (kv->value_type != NUMBER) return NULL;
    return (int*)(kv->value);
}

char** kv_string_value(struct kv* kv) {
    if (kv->value_type != STRING) return NULL;
    struct String* string_value = (struct String*)(kv->value);
    return &(string_value->data);
}

void kv_print(struct kv* kv) {
    printf("%s: ", kv->key->data);
    if (kv->value_type == STRING) {
        printf("%s\n", *kv_string_value(kv));
    } else {
        printf("%d\n", *kv_number_value(kv));
    }
}

struct kvArray {
	struct kv** data;
	unsigned size, capacity;
};

void kvarray_resize(struct kvArray* array, unsigned size) {
	struct kv** new_data = (struct kv**)malloc(sizeof(struct kv*) * size);
	for (unsigned i = 0u; i < array->size; i++) {
		i[new_data] = i[array->data];
	}
	free(array->data);
	array->data = new_data;
	array->capacity = size;
}

struct kvArray* kvarray_constructor(unsigned size) {
	struct kvArray* array = (struct kvArray*)malloc(sizeof(struct kvArray));
	array->size = 0u;
	array->data = NULL;
	kvarray_resize(array, size);
	return array;
}

void kvarray_destructor(struct kvArray* array) {
    for (unsigned i = 0u; i < array->size; i++) {
        kv_destructor(array->data[i]);
    }
	free(array->data);
	free(array);
}

void kvarray_push(struct kvArray* array, struct kv* value) {
	unsigned new_capacity = (array->capacity ? array->capacity * 2 : 1);
	if (array->capacity == array->size) {
		kvarray_resize(array, new_capacity);
	}
	array->data[array->size++] = value;
}

struct kvArray* _loads(const char* input_string) {
	enum JsonStatus {
	    BEFORE_OBJECT,
	    INSIDE_OBJECT,
	    INSIDE_KEY,
	    AFTER_KEY,
	    BEFORE_VALUE,
	    INSIDE_STRING_VALUE,
	    INSIDE_NUMBER_VALUE,
	    AFTER_VALUE,
	    AFTER_OBJECT,
	    BROKEN
	} status = BEFORE_OBJECT;
	struct kvArray* retval = kvarray_constructor(5);

	struct String* key_arr = string_constructor(5);
	struct String* val_arr = string_constructor(5);
	VALUE_TYPE value_type;

    unsigned i = 0u;
    char token = input_string[i];

	for(; token != '\0'; token=input_string[++i]) {
		switch (status) {
		    case BROKEN:
		    break;

		    case BEFORE_OBJECT:
		    if (token == '{') {
		        status = INSIDE_OBJECT;
		    } else if (!isspace(token)){
		        status = BROKEN;
		    }
		    break;

		    case INSIDE_OBJECT:
		    if (token == '"') {
		        status = INSIDE_KEY;
		    } else if (token == '}') {
		        status = AFTER_OBJECT;
		    } else if (!isspace(token)){
		        status = BROKEN;
		    }
		    break;

		    case INSIDE_KEY:
		    if (token == '"') {
		        status = AFTER_KEY;
		    } else {
		        string_push(key_arr, token);
		    }
		    break;

		    case AFTER_KEY:
		    if (token == ':') {
		        string_push(key_arr, '\0');
		        status = BEFORE_VALUE;
		    } else {
		        status = BROKEN;
		    }
		    break;

		    case BEFORE_VALUE:
		    if (token == '"') {
		        value_type = STRING;
		        status = INSIDE_STRING_VALUE;
		    } else if (isdigit(token)) {
		        value_type = NUMBER;
		        status = INSIDE_NUMBER_VALUE;
		        i--;
		    } else if (token == '-') {
		        value_type = NUMBER;
		        status = INSIDE_NUMBER_VALUE;
		        string_push(val_arr, token);
		    } else if (!isspace(token)) {
		        status = BROKEN;
		    }
		    break;

		    case INSIDE_NUMBER_VALUE:
		    if (token == ',' || token == '}') {
		        status = AFTER_VALUE;
		        i--;
		    } else if (isdigit(token)) {
		        string_push(val_arr, token);
		    } else {
		        status = BROKEN;
		    }
		    break;

		    case INSIDE_STRING_VALUE:
		    if (token == '"') {
		        status = AFTER_VALUE;
		    } else {
		        string_push(val_arr, token);
		    }
		    break;

		    case AFTER_VALUE:
		    if (token == ',' || token == '}') {
		        string_push(val_arr, '\0');

		        int* number_ptr = (int*)malloc(sizeof(int));
		        void* value_ptr;
		        if (value_type == NUMBER) {
		            *number_ptr = atoi(val_arr->data);
		            value_ptr = (void*)number_ptr;
		        } else {
		            value_ptr = (void*)val_arr;
		        }

		        struct kv* new_kv = kv_constructor(key_arr, value_ptr, value_type);

		        kvarray_push(retval, new_kv);

		        free(number_ptr);

		        key_arr->size = 0;
		        val_arr->size = 0;
		        status = INSIDE_OBJECT;

		        if (token == '}') i--;
		    } else {
		        status = BROKEN;
		    }
		    break;

		    case AFTER_OBJECT:
		    if (!isspace(token)) {
		        status = BROKEN;
		    }
		    break;

		    default:
		    status = BROKEN;
		    break;
		}
	}
	string_destructor(key_arr);
	string_destructor(val_arr);

    if (status == BROKEN) return NULL;
	return retval;
}

char* _dumps(struct kvArray* object) {
    struct String* retval = string_constructor(6);
    string_push(retval, '{');

    for (unsigned i = 0u; i < object->size;) {
        struct kv* kv = object->data[i++];

        struct String* key = kv->key;
        string_push(retval, '"');
        for (unsigned j = 0u; key->data[j] != '\0';) {
            string_push(retval, key->data[j++]);
        }
        string_push(retval, '"');

        string_push(retval, ':');

        char* value;
        if (kv->value_type == NUMBER) {
            value = (char*)malloc(64);
            sprintf(value, "%d", *((int*)(kv->value)));
        } else {
            value = ((struct String*)(kv->value))->data;
            string_push(retval, '"');
        }

        for (unsigned j = 0u; value[j] != '\0';) {
            string_push(retval, value[j++]);
        }

        if (kv->value_type == NUMBER) {
            free(value);
        } else {
            string_push(retval, '"');
        }
        if (i != object->size) string_push(retval, ',');
    }
    string_push(retval, '}');
    string_push(retval, '\0');

    char* stringified = retval->data;
    free(retval);
    return stringified;
}