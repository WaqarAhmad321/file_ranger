#include<Python.h>
#include<pybind11/pybind11.h>
#include<pybind11/stl.h>
#include "../backend/include/file_node.h"
#include "../backend/include/history_manager.h"
#include "../backend/src/directory_tree.cpp"

namespace py = pybind11;

PYBIND11_MODULE(backend, m) {
    py::class_<FileNode, std::shared_ptr<FileNode>>(m, "FileNode")
    .def_readonly("name", &FileNode::name)
    .def_readonly("path", &FileNode::path)
    .def_readonly("is_directory", &FileNode::is_directory)
    .def_readonly("size", &FileNode::size)
    .def_readonly("children", &FileNode::children); // vector of shared_ptr<FileNode>

    py::class_<HistoryManager>(m, "HistoryManager")
        .def(py::init<>())
        .def("init", &HistoryManager::init)
        .def("push", &HistoryManager::push)
        .def("go_back", &HistoryManager::go_back)
        .def("go_forward", &HistoryManager::go_forward)
        .def("current", &HistoryManager::current);

    m.def("list_directory", &list_directory, "Builds a directory tree from the given path");
    m.def("make_directory_recursive", &make_directory_recursive, "Create directories recursively");
    m.def("remove_path_recursive", &remove_path_recursive, "Remove file or directory recursively");
    m.def("rename_path", &rename_path, "Rename/move a path");
    m.def("copy_path", &copy_path, "Copy file or directory (recursive)");
    m.def("touch_file", &touch_file, "Create an empty file or update mtime");
}