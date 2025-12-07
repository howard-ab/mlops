#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "src/GrayScale.h"

namespace py = pybind11;

PYBIND11_MODULE(myalgo, m) {
    m.doc() = R"pbdoc(
        Simple image processing algorithms with Python bindings
        
        This module provides:
        - RGB to Grayscale conversion
        
        Author: MLOps Course Student
    )pbdoc";
    py::class_<GrayScale>(m, "GrayScale")
        .def_static("convert_to_gray", &GrayScale::convertToGray,
                   R"pbdoc(
                   Convert RGB image to grayscale
                   
                   Args:
                       rgb_image: 3D list [height][width][3] with RGB values (0-255 or 0-1)
                   
                   Returns:
                       2D list [height][width] with grayscale values
                   
                   Formula: Gray = 0.299*R + 0.587*G + 0.114*B
                   )pbdoc");
    m.def("to_gray", &GrayScale::convertToGray, "Convert RGB to grayscale");
    
#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "0.1.0";
#endif
}