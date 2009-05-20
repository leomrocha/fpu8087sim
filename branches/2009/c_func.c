#archivo en C para linkear con python
#include <Python.h>
#include <math.h>

static PyObject *
cos_function(PyObject *self, PyObject *args)
{
    float entrada, res;

    if (!PyArg_ParseTuple(args, "f", &entrada))
        return NULL;
    res = cos(command);
    return Py_BuildValue("f", res);
}

static PyMethodDef C_methods[] = {
    ...
    {"cos",  cos_function, METH_VARARGS,
     "Calcula el coseno del argumento."},
    ...
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
init_c_func(void)
{
    (void) Py_InitModule("cos", C_methods);
}

