#include <Python.h>
#include "json.h"

// Python module definition

static PyObject *loads(PyObject *self, PyObject* args);
static PyObject *dumps(PyObject *self, PyObject* args);

static PyMethodDef methods[] = {
    {"loads", loads, METH_VARARGS, "loads"},
    {"dumps", dumps, METH_VARARGS, "dumps"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT, "cjson", "C JSON Converter", -1, methods
};

PyMODINIT_FUNC PyInit_cjson(void) {
    PyObject* mod = PyModule_Create(&module);

    return mod;
}

static PyObject* loads(PyObject* self, PyObject* args) {
    char* val;
    if (!PyArg_ParseTuple(args, "s", &val)) {
        PyErr_Format(PyExc_TypeError, "Incorrect argument");
        return NULL;
    }
    
    PyObject *dict;
    if (!(dict = PyDict_New())) {
        PyErr_Format(PyExc_RuntimeError, "Can not create new dict");
        return NULL;
    }

    struct kvArray* object = _loads(val);

    if (!object) {
        PyErr_Format(PyExc_ValueError, "Incorrect json string");
        return NULL;
    }

    for (unsigned i = 0u; i < object->size;) {
        struct kv* kv = object->data[i++];
        PyObject* key;
        if (!(key = Py_BuildValue("s", kv->key->data))) {
            PyErr_Format(PyExc_ValueError, "Incorrect key");
        }
        PyObject* value = NULL;
        int* int_value = kv_number_value(kv);
        if (int_value) {
            if (!(value = Py_BuildValue("i", *int_value))) {
                PyErr_Format(PyExc_ValueError, "Incorrect key");
            }
        } else {
            if (!(value = Py_BuildValue("s", *kv_string_value(kv)))) {
                PyErr_Format(PyExc_ValueError, "Incorrect key");
            }
        }
        PyDict_SetItem(dict, key, value);
    }
    kvarray_destructor(object);

    return dict;
}


static PyObject* dumps(PyObject* self, PyObject* args) {
    PyObject* dict;
    if (!PyArg_ParseTuple(args, "O", &dict)) {
        PyErr_Format(PyExc_TypeError, "Incorrect argument");
        return NULL;
    }
    PyObject* dict_key;
    PyObject* dict_value;

    struct kvArray* object = kvarray_constructor(1);
    for (Py_ssize_t i = 0; PyDict_Next(dict, &i, &dict_key, &dict_value);) {
        void* value;
        if (!PyUnicode_CheckExact(dict_key)) {
            PyErr_Format(PyExc_TypeError, "Invalid key");
            return NULL;
        }
        const char* key_data = PyUnicode_AsUTF8(dict_key);
        struct String* key = string_constructor(5);
        for(unsigned i = 0u; key_data[i] != '\0';) {
            string_push(key, key_data[i++]);
        }
        string_push(key, '\0');
        VALUE_TYPE value_type = STRING;
        if (PyLong_Check(dict_value)) {
            value_type = NUMBER;
            int* number_value = malloc(sizeof(int));
            *number_value = PyLong_AsLong(dict_value);
            value = (void*)(number_value);
        } else if (PyUnicode_CheckExact(dict_value)) {
            const char* string_value_data = PyUnicode_AsUTF8(dict_value);
            struct String* string_value = string_constructor(5);
            for(unsigned i = 0u; string_value_data[i] != '\0';) {
                string_push(string_value, string_value_data[i++]);
            }
            string_push(string_value, '\0');
            value = (void*)(string_value);
        } else {
            PyErr_Format(PyExc_TypeError, "Invalid value");
            return NULL;
        }

        struct kv* kv = kv_constructor(key, value, value_type);
        kvarray_push(object, kv);
    }

    char* stringified = _dumps(object);
    kvarray_destructor(object);
    return Py_BuildValue("s", stringified);
}